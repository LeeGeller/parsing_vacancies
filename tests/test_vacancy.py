from abc import ABC

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
