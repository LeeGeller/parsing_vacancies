from abc import ABC

from src.Vacancy import Vacancy
from src.AbstractHh import AbstractHh


def test_issubclass():
    assert issubclass(AbstractHh, ABC)
    assert issubclass(Vacancy, AbstractHh)


def test_get_vacancy_from_api():
    vacancy = Vacancy('python')
    assert isinstance(vacancy.get_vacancy_from_api(), dict)
    assert len(vacancy.get_vacancy_from_api()) != 0

#     assert vacancy
