import json
from abc import ABC, abstractmethod

import requests

from src.utils import get_vacancies_list


class AbstractGetApiHh(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_vacancy_from_api(self, name_vacancy: str) -> list:
        pass


class GetApiHh(AbstractGetApiHh):

    def __init__(self):
        self.all_vacancy: list = []
        self.employer_info: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, name_vacancy: list) -> list:
        """Get valid info about vacancies for user"""
        name_vacancy: str = ' '.join(name_vacancy)
        keys_response = {'text': name_vacancy, 'area': 113, 'per_page': 100, }
        try:
            info: json = requests.get(f'https://api.hh.ru/vacancies', params=keys_response)
            self.all_vacancy: list = json.loads(info.text)['items']
        except requests.exceptions.RequestException:
            print('Connection error')
        return get_vacancies_list(self.all_vacancy)


vac = ['python', 'junior']
parsing_info = GetApiHh()
print(parsing_info.get_vacancy_from_api(vac))
