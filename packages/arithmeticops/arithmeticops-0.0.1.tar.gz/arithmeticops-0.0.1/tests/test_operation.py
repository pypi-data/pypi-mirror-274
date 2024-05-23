import pytest
from app_explorer.operation import add, subtract,multiply



def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0

def test_subtract():
    assert subtract(2, 1) == 1
    assert subtract(2, 2) == 0

def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1
    
    
if __name__ == "__main__":
    pytest.main()