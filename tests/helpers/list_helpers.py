import re
from collections.abc import Callable
from dataclasses import dataclass
from operator import attrgetter
from typing import Any


@dataclass
class Column:
    header: str
    db_attr: str
    ui: Callable[[str], str] | None = None
    db: Callable[[Any], str] | None = None


def normalize_ui_rows(
    ui_rows: list[dict[str, str]],
    columns: list[Column],
) -> list[dict[str, str]]:
    """Keeps mapped columns (dropping extra UI-only columns) and applies UI transforms."""
    results = []
    for row in ui_rows:
        clean_row = {}
        for col in columns:
            raw_value = row[col.header]
            clean_row[col.header] = col.ui(raw_value) if col.ui else raw_value
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
            raw_value = attrgetter(col.db_attr)(item)
            if col.db:
                clean_row[col.header] = col.db(raw_value)
            elif raw_value is None:
                clean_row[col.header] = ""
            else:
                clean_row[col.header] = str(raw_value)
        results.append(clean_row)
    return results


def extract_img_base64(html: str) -> str:
    """Extracts the base64 payload from an <img src='data:...;base64,...'> tag."""
    if not html:
        return ""
    match = re.search(r"base64,([^\"']+)", html)
    return match.group(1) if match else html
