import pytest

from src.CompareVacancies import CompareVacancies


@pytest.fixture
def fixture_class_valid():
    return CompareVacancies('python')
