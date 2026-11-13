from helpers.list_helpers import filter_and_sort_dicts, map_objects_to_dicts
from models.admin_app import AdminApp


def assert_table_matches(
    admin_app: AdminApp,
    table_test_id: str,
    expected_objects: list,
    field_map: dict[str, str],
    sort_by: str = "",
) -> None:
    __tracebackhide__ = True

    columns = list(field_map.keys())
    table_rows = admin_app.convert_html_table_to_pythonic_data_structure(table_test_id)

    actual = filter_and_sort_dicts(table_rows, columns, sort_by)
    expected = filter_and_sort_dicts(map_objects_to_dicts(expected_objects, field_map), columns, sort_by)
    assert actual == expected
