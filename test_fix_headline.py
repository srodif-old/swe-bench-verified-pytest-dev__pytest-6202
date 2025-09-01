"""Test to verify the fix for test headline display issue."""
import pytest


def test_getmodpath_preserves_brackets_in_parameters():
    """Test that getmodpath doesn't corrupt parameter values containing '.['"""
    from _pytest.python import PyobjMixin
    
    # This test will verify that the problematic line doesn't corrupt
    # parameter values that contain "..[" patterns
    # We'll create a mock scenario to test the getmodpath method
    
    class MockNode:
        def __init__(self, name):
            self.name = name
    
    class MockPyobj(PyobjMixin):
        def __init__(self, parts):
            self._parts = parts
            
        def listchain(self):
            return [MockNode(part) for part in self._parts]
    
    # Test case that would be affected by the bug
    mock_pyobj = MockPyobj(['test_boo', '..['])
    result = mock_pyobj.getmodpath(stopatmodule=False)
    
    # This should NOT have "..[" replaced with ".["
    assert result == 'test_boo..['
    # But currently it would return 'test_boo.['


@pytest.mark.parametrize("a", ["..["])  
def test_parametrized_with_bracket_pattern(a):
    """This test will help us verify the headline display is correct."""
    # This test will fail, which is expected
    # We use this to examine the test report headline
    assert a == "..[", f"Parameter value should be preserved as '..[' but got {a!r}"