import json


def get_columns_to_be_obfuscated(input_json):
    """
    Extracts names of columns to be obfuscated
    from "pii_fields" field in input JSON string

    Args:
        input_json: target JSON string

    Returns:
        List of column names
    """
    try:
        input_params = json.loads(input_json)

        columns_for_obfuscation = input_params["pii_fields"]

        return columns_for_obfuscation

    except Exception as e:
        print(
            f"Could not extract columns to be obfuscated from JSON input: {e}")
