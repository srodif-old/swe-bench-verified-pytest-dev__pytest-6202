"""
Direct test of the getmodpath functionality to verify the fix
"""
import sys
sys.path.insert(0, 'src')

# Import the relevant classes
from _pytest.python import PyobjMixin
from _pytest.nodes import Node
import pytest

# Create a minimal test to verify our fix works
class MockNode:
    def __init__(self, name):
        self.name = name

class TestableGetmodpath:
    """Test class to verify getmodpath behavior"""
    
    def create_mock_pyobj(self, parts):
        """Create a mock PyobjMixin with given parts"""
        class MockPyobj(PyobjMixin):
            def __init__(self, parts):
                self._parts = parts
                
            def listchain(self):
                return [MockNode(part) for part in self._parts]
        
        return MockPyobj(parts)
    
    def test_getmodpath_with_bracket_in_parameter(self):
        """Test that getmodpath preserves parameter values with brackets"""
        # Test case with the problematic pattern
        mock_pyobj = self.create_mock_pyobj(['test_boo', '..['])
        result = mock_pyobj.getmodpath(stopatmodule=False)
        expected = 'test_boo..['
        
        print(f"Input parts: ['test_boo', '..[']")
        print(f"Expected result: {expected}")
        print(f"Actual result: {result}")
        print(f"Test {'PASSED' if result == expected else 'FAILED'}")
        
        return result == expected
    
    def test_getmodpath_normal_case(self):
        """Test that getmodpath still works for normal cases"""
        # Test case without problematic pattern
        mock_pyobj = self.create_mock_pyobj(['test_module', 'test_func'])
        result = mock_pyobj.getmodpath(stopatmodule=False)
        expected = 'test_module.test_func'
        
        print(f"Input parts: ['test_module', 'test_func']")
        print(f"Expected result: {expected}")
        print(f"Actual result: {result}")
        print(f"Test {'PASSED' if result == expected else 'FAILED'}")
        
        return result == expected

# Run the tests
if __name__ == "__main__":
    tester = TestableGetmodpath()
    
    print("=== Testing getmodpath fix ===")
    print()
    print("Test 1: Parameter with problematic pattern")
    test1_passed = tester.test_getmodpath_with_bracket_in_parameter()
    
    print()
    print("Test 2: Normal case")
    test2_passed = tester.test_getmodpath_normal_case()
    
    print()
    print("=== Summary ===")
    print(f"Test 1 (bracket pattern): {'PASSED' if test1_passed else 'FAILED'}")
    print(f"Test 2 (normal case): {'PASSED' if test2_passed else 'FAILED'}")
    
    if test1_passed and test2_passed:
        print("✅ All tests passed! The fix is working correctly.")
        exit(0)
    else:
        print("❌ Some tests failed!")
        exit(1)