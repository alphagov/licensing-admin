import re
from collections.abc import Callable
from dataclasses import dataclass
from operator import attrgetter
from typing import Any


@dataclass
class Column:
    table_header: str
    db_field_name: str
    ui_data_mapping_function: Callable[[str], str] | None = None
    db_data_mapping_function: Callable[[Any], str] | None = None


def normalize_ui_rows(
    ui_rows: list[dict[str, str]],
    columns: list[Column],
) -> list[dict[str, str]]:
    """Keeps mapped columns (dropping extra UI-only columns) and applies UI transforms."""
    results = []
    for row in ui_rows:
        clean_row = {}
        for col in columns:
            raw_value = row[col.table_header]
            clean_row[col.table_header] = (
                col.ui_data_mapping_function(raw_value) if col.ui_data_mapping_function else raw_value
            )
        results.append(clean_row)
    return results


def extract_db_rows(
    objects: list[Any],
    columns: list[Column],
) -> list[dict[str, str]]:
    """Extracts attributes from DB objects and formats them into strings."""
    results = []
    for item in objects:
        clean_row = {}
        for col in columns:
            raw_value = attrgetter(col.db_field_name)(item)
            if col.db_data_mapping_function:
                clean_row[col.table_header] = col.db_data_mapping_function(raw_value)
            elif raw_value is None:
                clean_row[col.table_header] = ""
            else:
                clean_row[col.table_header] = str(raw_value)
        results.append(clean_row)
    return results


def extract_img_base64(html: str) -> str:
    """Extracts the base64 payload from an <img src='data:...;base64,...'> tag."""
    if not html:
        return ""
    match = re.search(r"base64,([^\"']+)", html)
    return match.group(1) if match else html
