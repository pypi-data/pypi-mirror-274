import pytest

from src.obfsc8.get_filetype import get_filetype

filename = "new_data/file1.csv"


def test_that_string_returned():
    result = get_filetype(filename)

    assert isinstance(result, str)


def test_that_csv_returned_with_csv_file_input():
    result = get_filetype(filename)

    assert result == "csv"


def test_that_type_error_raised_if_input_filename_not_a_string():
    with pytest.raises(TypeError, match="must be a string"):
        get_filetype(674)


def test_that_value_error_raised_if_period_not_present_in_filename():
    with pytest.raises(ValueError, match="must contain a period"):
        get_filetype("new_data/file1")


def test_that_value_error_raised_if_filetype_not_CSV():
    with pytest.raises(ValueError, match="Filetype must be CSV"):
        get_filetype("new_data/file1.jpg")
