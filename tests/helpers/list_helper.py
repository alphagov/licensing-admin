def extract_values_and_sort_result(input_list: list[dict[str, str]], key_to_extract: str):
    return list.sort([item[key_to_extract] for item in input_list])
