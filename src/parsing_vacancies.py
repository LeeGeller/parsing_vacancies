import json
from abc import ABC, abstractmethod
import time

import requests

from src.utils import get_vacancies_list, ParsingManager


class AbstractGetApi(ABC):
    @abstractmethod
    def __init__(self):
        self.all_vacancy: list = []

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_vacancy_from_api(self, name_vacancy: str) -> list:
        pass


class ApiHh(AbstractGetApi):

    def __init__(self):
        self.all_vacancy: list = []
        self.employer_info: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, name_vacancy: list, pages_limit: int = 3) -> list:
        """Get valid info about vacancies for user"""

        hh_url = f'https://api.hh.ru/vacancies'
        keys_response = {'text': ' '.join(name_vacancy), 'area': 113, 'per_page': 100, }

        with ParsingManager(hh_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy


class ApiHabr(AbstractGetApi):
    def __init__(self):
        self.all_vacancy: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, name_vacancy: list, pages_limit: int = 3) -> list:
        url = 'https://career.habr.com/vacancies'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }


vacancies_fetcher = ApiHh()
name_vacancy = ['python', 'junior']
print(vacancies_fetcher.get_vacancy_from_api(name_vacancy, pages_limit=3))
