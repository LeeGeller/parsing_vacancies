from abc import ABC

from src.GetVacancies import GetVacancies
from src.AbstractHh import AbstractHh


def test_issubclass():
    assert issubclass(AbstractHh, ABC)
    assert issubclass(GetVacancies, AbstractHh)


def test_save_info_and_get_vacancy_from_api():

    assert GetVacancies('sfsf').message == "Vacancy not found"
    assert GetVacancies('python').message == "Vacancies found"
