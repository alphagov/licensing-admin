from operator import attrgetter


def map_objects_to_dicts(objects: list, field_map: dict[str, str]) -> list[dict[str, str]]:
    """Converts a list of Python objects into dicts keyed by the given mapping."""
    getters = {header: attrgetter(attr_path) for header, attr_path in field_map.items()}
    return [{header: str(getter(item)) for header, getter in getters.items()} for item in objects]


def filter_and_sort_dicts(rows: list[dict[str, str]], keys: list[str], sort_by: str = "") -> list[dict[str, str]]:
    """Keeps only the specified keys (ignoring extra UI columns) and sorts the rows."""
    if not rows or not keys:
        return []

    if not sort_by:
        sort_by = keys[0]

    filtered = [{key: row[key] for key in keys} for row in rows]
    return sorted(filtered, key=lambda row: row[sort_by])
