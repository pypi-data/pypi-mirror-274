# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for the LazyLoader class.

"""
import sys

import pytest

from qbraid_core._import import LazyLoader


def test_lazy_loading():
    """Test that the module is not loaded until an attribute is accessed."""
    # Remove the module from sys.modules if it's already loaded
    if "calendar" in sys.modules:
        del sys.modules["calendar"]

    calendar_loader = LazyLoader("calendar", globals(), "calendar")
    assert "calendar" not in sys.modules, "Module 'calendar' should not be loaded yet"

    # Access an attribute to trigger loading
    _ = calendar_loader.month_name
    assert (
        "calendar" in sys.modules
    ), "Module 'calendar' should be loaded after accessing an attribute"


def test_parent_globals_update():
    """Test that the parent's globals are updated after loading."""
    if "math" in sys.modules:
        del sys.modules["math"]

    math_loader = LazyLoader("math", globals(), "math")
    assert "math" not in globals(), "Global namespace should not initially contain 'math'"

    _ = math_loader.pi
    assert "math" in globals(), "Global namespace should contain 'math' after loading"


def test_attribute_access():
    """Test that attributes of the loaded module can be accessed."""
    math_loader = LazyLoader("math", globals(), "math")
    assert math_loader.pi == pytest.approx(
        3.141592653589793
    ), "Attribute 'pi' should match the math module's 'pi'"


def test_invalid_attribute():
    """Test accessing an invalid attribute."""
    math_loader = LazyLoader("math", globals(), "math")
    with pytest.raises(AttributeError):
        _ = math_loader.invalid_attribute
