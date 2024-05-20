import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from dvcx.client import Client
from dvcx.client.local import FileClient
from tests.utils import uppercase_scheme


def test_bad_url():
    bucket = "whatever"
    path = "my/path"
    with pytest.raises(RuntimeError):
        Client.parse_url(bucket + "/" + path + "/", None, None)


non_null_text = st.text(
    alphabet=st.characters(blacklist_categories=["Cc", "Cs"]), min_size=1
)


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(rel_path=non_null_text)
def test_parse_url(cloud_test_catalog, rel_path, cloud_type):
    if cloud_type == "file":
        assume(not rel_path.startswith("/"))
    bucket_uri = cloud_test_catalog.src_uri
    url = f"{bucket_uri}/{rel_path}"
    catalog = cloud_test_catalog.catalog
    client, rel_part = catalog.parse_url(url)
    if cloud_type == "file":
        root_uri = FileClient.root_path().as_uri()
        assert client.uri == root_uri
        assert rel_part == url[len(root_uri) :]
    else:
        assert client.uri == bucket_uri
        assert rel_part == rel_path


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
@given(rel_path=non_null_text)
def test_parse_url_uppercase_scheme(cloud_test_catalog, rel_path, cloud_type):
    if cloud_type == "file":
        assume(not rel_path.startswith("/"))
    bucket_uri = cloud_test_catalog.src_uri
    bucket_uri_upper = uppercase_scheme(bucket_uri)
    url = f"{bucket_uri_upper}/{rel_path}"
    catalog = cloud_test_catalog.catalog
    client, rel_part = catalog.parse_url(url)
    if cloud_type == "file":
        root_uri = FileClient.root_path().as_uri()
        assert client.uri == root_uri
        assert rel_part == url[len(root_uri) :]
    else:
        assert client.uri == bucket_uri
        assert rel_part == rel_path
