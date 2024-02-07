from abc import ABC

from src.Vacancy import Vacancy
from src.AbstractHh import AbstractHh


def test_issubclass():
    assert issubclass(AbstractHh, ABC)
    assert issubclass(Vacancy, AbstractHh)


def test_save_info_and_get_vacancy_from_api():

    assert Vacancy('sfsf').message == "Vacancy not found"
    assert Vacancy('python').message == "Vacancies found"
