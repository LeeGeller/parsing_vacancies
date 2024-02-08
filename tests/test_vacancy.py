from abc import ABC

import pytest

from config import DATA
from src.GetVacancies import GetVacancies
from src.AbstractHh import AbstractHh


def test_issubclass():
    assert issubclass(AbstractHh, ABC)
    assert issubclass(GetVacancies, AbstractHh)


def test_get_vacancy_from_api():
    vacancy1 = GetVacancies('tttttt')
    vacancy2 = GetVacancies(1)
    vacancy3 = GetVacancies('python')

    vacancy1.get_vacancy_from_api(vacancy1.name_vacancy)
    vacancy2.get_vacancy_from_api(vacancy2.name_vacancy)
    vacancy3.get_vacancy_from_api(vacancy3.name_vacancy)

    assert vacancy1.message == "Vacancies found"
    assert vacancy2.message == "Vacancy not found"
    assert vacancy3.message == "Vacancies found"


def test_save_info_valid():
    vacancy1 = GetVacancies('python')
    list_info1 = vacancy1.get_vacancy_from_api(vacancy1.name_vacancy)
    vacancy1.save_info(list_info1, DATA)

    assert isinstance(vacancy1.all, list)
    assert len(vacancy1.all) > 0


def test_save_info_zero_len():
    vacancy1 = GetVacancies(1)
    list_info1 = vacancy1.get_vacancy_from_api(vacancy1.name_vacancy)

    vacancy1.save_info(list_info1, DATA)
    assert vacancy1.message == "Vacancy not found"


def test_save_info_with_broke_path():
    vacancy2 = GetVacancies('python')
    list_info2 = vacancy2.get_vacancy_from_api(vacancy2.name_vacancy)
    with pytest.raises(AttributeError):
        vacancy2.save_info(list_info2, "src/data")

    with pytest.raises(AttributeError):
        vacancy2.save_info(list_info2, "")
