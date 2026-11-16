from operator import itemgetter

from helpers.list_helpers import Column, extract_db_rows, normalize_ui_rows
from models.admin_app import AdminApp


def assert_table_matches(
    admin_app: AdminApp,
    table_test_id: str,
    expected_objects: list,
    columns: list[Column],
    sort_by: str = "",
) -> None:
    __tracebackhide__ = True

    if not columns:
        raise ValueError("columns cannot be empty")

    sort_key = sort_by or columns[0].header

    raw_ui_rows = admin_app.convert_html_table_to_pythonic_data_structure(table_test_id)
    normalized_ui_rows = normalize_ui_rows(raw_ui_rows, columns)
    actual = sorted(normalized_ui_rows, key=itemgetter(sort_key))

    extracted_db_rows = extract_db_rows(expected_objects, columns)
    expected = sorted(extracted_db_rows, key=itemgetter(sort_key))

    assert actual == expected
