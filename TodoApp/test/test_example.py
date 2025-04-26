import pytest

def test_equal_number():
    assert 1 == 1

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance('10', int)

def test_boolean():
    assert True == True
    assert ('hello' == 'world') is not True

def test_type():
    assert type('hello' is str)
    assert type('hello' is not int)

def test_greater_and_lesser_than():
    assert 6 > 5
    assert 2 < 7

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student("Jhon", "Doe", "Computer Science", 3)

def test_person_initialization(default_employee):
    assert default_employee.first_name == "Jhon", "first_name should be Jhon"
    assert default_employee.last_name == "Doe", "last_name should be Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3
