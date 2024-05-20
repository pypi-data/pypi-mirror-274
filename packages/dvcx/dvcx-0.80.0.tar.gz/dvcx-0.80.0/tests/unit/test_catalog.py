from textwrap import dedent
from typing import TYPE_CHECKING

from dvcx.catalog import Catalog

if TYPE_CHECKING:
    from dvcx.data_storage import AbstractWarehouse


def test_compile_query_script(catalog):
    script = dedent(
        """
        from dvcx.query import C, DatasetQuery, asUDF
        DatasetQuery("s3://bkt/dir1")
        """
    ).strip()
    result = catalog.compile_query_script(script)
    expected = dedent(
        """
        from dvcx.query import C, DatasetQuery, asUDF
        import dvcx.query.dataset
        dvcx.query.dataset.query_wrapper(
        DatasetQuery('s3://bkt/dir1'))
        """
    ).strip()
    assert result == expected


def test_catalog_warehouse_ready_callback(mocker, warehouse, id_generator, metastore):
    spy = mocker.spy(warehouse, "is_ready")

    def callback(warehouse: "AbstractWarehouse"):
        assert warehouse.is_ready()

    catalog = Catalog(
        id_generator, metastore, warehouse, warehouse_ready_callback=callback
    )

    spy.assert_not_called()

    _ = catalog.warehouse

    spy.assert_called_once()
    spy.reset_mock()

    _ = catalog.warehouse

    spy.assert_not_called()
