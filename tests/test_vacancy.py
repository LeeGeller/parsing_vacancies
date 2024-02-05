from abc import ABC

from src.Vacancy import Vacancy
from src.AbstractHh import AbstractHh


def test_issubclass():
    assert issubclass(AbstractHh, ABC)
    assert issubclass(Vacancy, AbstractHh)


def test_save_info_and_get_vacancy_from_api():
    vacancy = Vacancy('python')
    vacancy.save_info()

    assert len(vacancy.all) != 0
