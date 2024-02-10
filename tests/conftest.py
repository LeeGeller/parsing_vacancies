import json

import pytest

from config import DATA_TEST
from src.Vacancy import CompareVacancies


@pytest.fixture
def fixture_class_valid():
    return CompareVacancies('python')


@pytest.fixture
def fixture_class_number():
    return CompareVacancies(1)


@pytest.fixture
def fixture_class_some_str():
    return CompareVacancies('666999')


@pytest.fixture
def fixture_data():
    with open(DATA_TEST, encoding='utf-8') as file:
        return json.loads(file.read())

