from pdm_pypi.test_class import TestClass

def test_test_class():
    test = TestClass("Hello, World!")
    assert test.get_message() == "Hello, World!"
