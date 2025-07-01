import pytest

from pyemmo.functions.clean_name import clean_name, is_valid_filename


@pytest.mark.parametrize(
    "test_name,corrected_name",
    [
        ("test#name", "test_name"),
        ("0testname", "_0testname"),
    ],
)
def test_clean_name(test_name, corrected_name):

    assert corrected_name == clean_name(
        test_name
    ), "Variable name is invalid for GetDP/Gmsh script. Name could not be resolved. Variable names must have valid C or C# syntax."


@pytest.mark.parametrize(
    "test_filename,testbool",
    [
        ("file#name", False),
        ("filename!", False),
        ("filename", True),
    ],
)
def test_is_valid_filename(test_filename, testbool):

    assert testbool == is_valid_filename(
        test_filename
    ), "filename is a not a valid Windows filename to use"
