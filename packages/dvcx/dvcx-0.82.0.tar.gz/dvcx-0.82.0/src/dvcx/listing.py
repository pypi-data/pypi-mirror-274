import os
import posixpath
from collections.abc import Iterable
from itertools import zip_longest
from typing import TYPE_CHECKING, Optional

from fsspec.asyn import get_loop, sync
from sqlalchemy.sql import func
from tqdm import tqdm

from dvcx.node import DirType, Entry, Node, NodeWithPath
from dvcx.utils import TIME_ZERO, suffix_to_number

if TYPE_CHECKING:
    from dvcx.catalog.datasource import DataSource
    from dvcx.client import Client
    from dvcx.data_storage import AbstractMetastore, AbstractWarehouse
    from dvcx.storage import Storage


class Listing:
    def __init__(
        self,
        storage: "Storage",
        metastore: "AbstractMetastore",
        warehouse: "AbstractWarehouse",
        client: "Client",
    ):
        if not warehouse.uri:
            raise ValueError("warehouse.uri cannot be empty in Listing")
        self.storage = storage
        self.metastore = metastore
        self.warehouse = warehouse
        self.client = client

    def clone(self) -> "Listing":
        return self.__class__(
            self.storage, self.metastore.clone(), self.warehouse.clone(), self.client
        )

    @property
    def id(self):
        return self.storage.id

    def fetch(self, start_prefix="") -> None:
        sync(get_loop(), self._fetch, start_prefix)

    async def _fetch(self, start_prefix) -> None:
        self = self.clone()
        if start_prefix:
            start_prefix = start_prefix.rstrip("/")
            base_node = Entry.from_dir(
                posixpath.dirname(start_prefix),
                posixpath.basename(start_prefix),
                last_modified=TIME_ZERO,
            )
        else:
            base_node = Entry.root()
        try:
            self.insert_node(base_node)
            async for entries in self.client.scandir(start_prefix):
                self.warehouse.insert_nodes(entries)
                if len(entries) > 1:
                    self.metastore.update_last_inserted_at()
        finally:
            self.warehouse.insert_nodes_done()

    def insert_node(self, entry: Entry) -> None:
        self.warehouse.insert_node(entry)

    def insert_nodes(self, entries: Iterable[Entry]) -> None:
        self.warehouse.insert_nodes(entries)

    def expand_path(self, path) -> list[Node]:
        return self.warehouse.expand_path(path)

    def resolve_path(self, path) -> Node:
        return self.warehouse.get_node_by_path(path)

    def ls_path(self, node, fields):
        if node.vtype == "tar" or node.dir_type == DirType.TAR_ARCHIVE:
            return self.warehouse.select_node_fields_by_parent_path_tar(
                node.path, fields
            )
        return self.warehouse.select_node_fields_by_parent_path(node.path, fields)

    def collect_nodes_to_instantiate(
        self,
        sources: Iterable["DataSource"],
        copy_to_filename: Optional[str],
        recursive=False,
        copy_dir_contents=False,
        relative_path=None,
        from_edvcx=False,
        from_dataset=False,
    ) -> list[NodeWithPath]:
        rel_path_elements = relative_path.split("/") if relative_path else []
        all_nodes: list[NodeWithPath] = []
        for src in sources:
            node = src.node
            if recursive and src.is_container():
                dir_path = []
                if not copy_dir_contents:
                    dir_path.append(node.name)
                subtree_nodes = src.find(sort=["parent", "name"])
                all_nodes.extend(
                    NodeWithPath(n.n, path=dir_path + n.path) for n in subtree_nodes
                )
            else:
                node_path = []
                if from_edvcx:
                    for rpe, npe in zip_longest(
                        rel_path_elements, node.path.split("/")
                    ):
                        if rpe == npe:
                            continue
                        if npe:
                            node_path.append(npe)
                elif copy_to_filename:
                    node_path = [os.path.basename(copy_to_filename)]
                elif from_dataset:
                    node_path = [
                        src.listing.client.name,
                        node.parent,
                        node.name,
                    ]
                else:
                    node_path = [node.name]
                all_nodes.append(NodeWithPath(node, path=node_path))
        return all_nodes

    def instantiate_nodes(
        self,
        all_nodes,
        output,
        total_files=None,
        force=False,
        shared_progress_bar=None,
    ):
        progress_bar = shared_progress_bar or tqdm(
            desc=f"Instantiating '{output}'",
            unit=" files",
            unit_scale=True,
            unit_divisor=1000,
            total=total_files,
        )

        counter = 0
        for node in all_nodes:
            dst = os.path.join(output, *node.path)
            dst_dir = os.path.dirname(dst)
            os.makedirs(dst_dir, exist_ok=True)
            uid = node.n.as_uid(self.client.uri)
            self.client.instantiate_object(uid, dst, progress_bar, force)
            counter += 1
            if counter > 1000:
                progress_bar.update(counter)
                counter = 0

        progress_bar.update(counter)

    def find(
        self,
        node,
        fields,
        names=None,
        inames=None,
        paths=None,
        ipaths=None,
        size=None,
        type=None,
        order_by=None,
    ):
        n = self.warehouse.nodes
        conds = []
        if names:
            for name in names:
                conds.append(n.c.name.op("GLOB")(name))
        if inames:
            for iname in inames:
                conds.append(func.lower(n.c.name).op("GLOB")(iname.lower()))
        if paths:
            node_path = self.warehouse.path_expr(n)
            for path in paths:
                conds.append(node_path.op("GLOB")(path))
        if ipaths:
            node_path = self.warehouse.path_expr(n)
            for ipath in ipaths:
                conds.append(func.lower(node_path).op("GLOB")(ipath.lower()))

        if size is not None:
            size_limit = suffix_to_number(size)
            if size_limit >= 0:
                conds.append(n.c.size >= size_limit)
            else:
                conds.append(n.c.size <= -size_limit)

        return self.warehouse.find(
            node,
            fields,
            type=type,
            conds=conds,
            order_by=order_by,
        )

    def du(self, node: Node, count_files: bool = False):
        return self.warehouse.size(node, count_files)
