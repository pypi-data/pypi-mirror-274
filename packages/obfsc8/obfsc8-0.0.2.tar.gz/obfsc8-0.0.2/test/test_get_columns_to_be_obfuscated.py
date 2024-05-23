from src.obfsc8.get_columns_to_be_obfuscated \
    import get_columns_to_be_obfuscated
from test_data.test_json import test_json


def test_that_list_returned():
    result = get_columns_to_be_obfuscated(test_json)

    assert isinstance(result, list)


def test_that_list_contains_correct_column_names():
    result = get_columns_to_be_obfuscated(test_json)

    assert result == ["name", "email_address"]
