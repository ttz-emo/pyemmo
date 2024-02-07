import pytest
from math import pi, isclose

from pyleecan.Classes.Segment import Segment
from pyleecan.Classes.Arc1 import Arc1
from pyleecan.Classes.Arc2 import Arc2
from pyleecan.Classes.Arc3 import Arc3

from pyemmo.script.geometry.line import Line
from pyemmo.script.geometry.circleArc import CircleArc

from pyemmo.api.pyleecan.build_pyemmo_line_list import build_pyemmo_line_list


# =======================
# Declaration of fixtures
# =======================
@pytest.fixture
def sample_segment():
    """Fixture providing a sample Segment for testing."""
    return Segment(begin=0 + 0j, end=1 + 1j)


@pytest.fixture
def sample_arc1_under_180_deg():
    """Fixture providing a sample Arc1 for testing."""
    return Arc1(begin=0 + 0j, end=1 + 1j, radius=2)


@pytest.fixture
def sample_arc1_is_180_deg():
    """Fixture providing a sample Arc1 for testing."""
    return Arc1(begin=0 + 0j, end=2 + 0j, radius=1)


@pytest.fixture
def sample_arc2_under_180_deg():
    """Fixture providing a sample Arc2 for testing."""
    return Arc2(begin=0 + 0j, center=1 + 0j, angle=pi / 2)


@pytest.fixture
def sample_arc2_is_180_deg():
    """Fixture providing a sample Arc2 for testing."""
    return Arc2(begin=0 + 0j, center=1 + 0j, angle=pi)


@pytest.fixture
def sample_arc3():
    """Fixture providing a sample Arc3 for testing."""
    return Arc3(begin=0 + 0j, end=1 + 1j)


# =================
# Testing functions
# =================
def test_build_pyemmo_line_list_empty_list() -> None:
    """
    Test case to verify the behavior of build_pyemmo_line_list function when provided an empty list.

    Raises:
        IndexError: If the function fails to handle an empty list input correctly.
    """
    with pytest.raises(IndexError):
        build_pyemmo_line_list([])


def test_build_pyemmo_line_list_segment_error() -> None:
    """
    Test case to verify the behavior of build_pyemmo_line_list function when provided a list containing a Segment
    object with invalid parameters.

    Raises:
        ValueError: If the function fails to handle the provided Segment object correctly.
    """
    with pytest.raises(ValueError):
        build_pyemmo_line_list([Segment(begin=0 + 0j, end=0 + 0j)])


def test_build_pyemmo_line_list_wrong_imput_type() -> None:
    """
    Test case to verify the behavior of build_pyemmo_line_list function when provided an invalid input type.

    Raises:
        TypeError: If the function fails to handle the provided input type correctly.
    """
    with pytest.raises(TypeError):
        build_pyemmo_line_list(Segment(begin=0 + 0j, end=0 + 0j))


def test_build_pyemmo_line_list_with_segment(sample_segment: Segment) -> None:
    """Test function for the build_pyemmo_line_list with a single Segment.

    This function verifies that the build_pyemmo_line_list correctly translates
    a list containing a sample Segment into a list of Line objects from the pyemmo
    module. It checks if the result is a list and if all items in the list are
    instances of the Line class.

    Args:
        sample_segment: A sample Segment object to be used for testing.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_segment])

    assert pyemmo_line_list[0].startPoint.coordinate == (0, 0, 0)
    assert pyemmo_line_list[0].endPoint.coordinate == (1, 1, 0)
    assert len(pyemmo_line_list) == 1
    assert isinstance(pyemmo_line_list, list)
    assert isinstance(pyemmo_line_list[0], Line)


def test_build_pyemmo_line_list_arc1_under_180(
    sample_arc1_under_180_deg: Arc1,
) -> None:
    """Test function for build_pyemmo_line_list with an Arc1 angle under 180 degrees.

    This function tests the translation of an Arc1 object with an angle under 180 degrees
    into a pyemmo_line_list using build_pyemmo_line_list. It checks if the resulting
    pyemmo_line_list contains a single Line object with the expected start and end points.
    Additionally, it ensures that the length of the pyemmo_line_list is 1, and the types
    of the list and its elements are as expected.

    Args:
        sample_arc1_under_180_deg (Arc1): A sample Arc1 object with an angle under 180 degrees.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_arc1_under_180_deg])

    assert pyemmo_line_list[0].startPoint.coordinate == (0, 0, 0)
    assert pyemmo_line_list[0].endPoint.coordinate == (1, 1, 0)
    assert len(pyemmo_line_list) == 1
    assert isinstance(pyemmo_line_list, list)
    assert isinstance(pyemmo_line_list[0], Line)


def test_build_pyemmo_line_list_arc1_is_180(
    sample_arc1_is_180_deg: Arc1,
) -> None:
    """Test function for build_pyemmo_line_list with an Arc1 angle equal to 180 degrees.

    This function tests the translation of an Arc1 object with an angle of 180 degrees
    into a pyemmo_line_list using build_pyemmo_line_list. It checks if the resulting
    pyemmo_line_list contains two CircleArc objects, representing the split of the
    original Arc1. Additionally, it ensures that the length of the pyemmo_line_list is 2,
    and the types of the list and its elements are as expected.

    Args:
        sample_arc1_is_180_deg (Arc1): A sample Arc1 object with an angle equal to 180 degrees.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_arc1_is_180_deg])
    assert len(pyemmo_line_list) == 2
    assert isinstance(pyemmo_line_list, list)
    assert all(isinstance(item, CircleArc) for item in pyemmo_line_list)


def test_build_pyemmo_line_list_arc2_under_180(
    sample_arc2_under_180_deg: Arc2,
) -> None:
    """Test function for build_pyemmo_line_list with an Arc2 angle under 180 degrees.

    This function tests the translation of an Arc2 object with an angle under 180 degrees
    into a pyemmo_line_list using build_pyemmo_line_list. It checks if the resulting
    pyemmo_line_list contains a single Line object with the expected start, end, and
    center points, as well as the correct angle. Additionally, it ensures that the length
    of the pyemmo_line_list is 1, and the types of the list and its elements are as expected.

    Args:
        sample_arc2_under_180_deg (Arc2): A sample Arc2 object with an angle under 180 degrees.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_arc2_under_180_deg])

    assert pyemmo_line_list[0].startPoint.coordinate == (0, 0, 0)
    assert pyemmo_line_list[0].center.coordinate == (1, 0, 0)
    assert isclose(pyemmo_line_list[0].endPoint.coordinate[0], 1, abs_tol=1e-6)
    assert isclose(
        pyemmo_line_list[0].endPoint.coordinate[1], -1, abs_tol=1e-6
    )
    assert pyemmo_line_list[0].getAngle(inDeg=90) == 90
    assert len(pyemmo_line_list) == 1
    assert isinstance(pyemmo_line_list, list)
    assert isinstance(pyemmo_line_list[0], Line)


def test_build_pyemmo_line_list_arc2_is_180(
    sample_arc2_is_180_deg: Arc2,
) -> None:
    """Test function for build_pyemmo_line_list with an Arc2 angle equal to 180 degrees.

    This function tests the translation of an Arc2 object with an angle of 180 degrees
    into a pyemmo_line_list using build_pyemmo_line_list. It checks if the resulting
    pyemmo_line_list contains two CircleArc objects, representing the split of the
    original Arc2. Additionally, it ensures that the length of the pyemmo_line_list is 2,
    and the types of the list and its elements are as expected.

    Args:
        sample_arc2_is_180_deg (Arc2): A sample Arc2 object with an angle equal to 180 degrees.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_arc2_is_180_deg])
    assert len(pyemmo_line_list) == 2
    assert isinstance(pyemmo_line_list, list)
    assert all(isinstance(item, CircleArc) for item in pyemmo_line_list)


def test_build_pyemmo_line_list_with_arc3(sample_arc3):
    """Test function for build_pyemmo_line_list with an Arc3.

    This function tests the translation of an Arc3 object into a pyemmo_line_list
    using build_pyemmo_line_list. It checks if the resulting pyemmo_line_list
    contains two CircleArc objects, representing the split of the original Arc3.
    Additionally, it ensures that the length of the pyemmo_line_list is 2, and the
    types of the list and its elements are as expected.

    Args:
        sample_arc3: A sample Arc3 object to be used for testing.

    Returns:
        None: The function asserts the test conditions and raises an exception
        if any of the conditions are not met.
    """
    pyemmo_line_list = build_pyemmo_line_list([sample_arc3])
    assert len(pyemmo_line_list) == 2
    assert isinstance(pyemmo_line_list, list)
    assert all(isinstance(item, CircleArc) for item in pyemmo_line_list)


def test_build_pyemmo_line_list_with_mixed_elements(
    sample_segment,
    sample_arc1_under_180_deg,
    sample_arc1_is_180_deg,
    sample_arc2_under_180_deg,
    sample_arc2_is_180_deg,
    sample_arc3,
):
    pyemmo_line_list = build_pyemmo_line_list(
        [
            sample_segment,
            sample_arc1_under_180_deg,
            sample_arc1_is_180_deg,
            sample_arc2_under_180_deg,
            sample_arc2_is_180_deg,
            sample_arc3,
        ]
    )
    assert len(pyemmo_line_list) == 9
    assert isinstance(pyemmo_line_list, list)
    assert all(
        isinstance(item, (Line, CircleArc)) for item in pyemmo_line_list
    )
