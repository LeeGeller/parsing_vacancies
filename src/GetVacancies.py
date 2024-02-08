import json
import pathlib

import requests

from config import DATA
from src.AbstractHh import AbstractHh


class GetVacancies(AbstractHh):
    all = []

    def __init__(self, name_vacancy: str):
        self.name_vacancy: str = name_vacancy
        self.message = "Vacancies found"

    def get_vacancy_from_api(self, vacancy_name: str) -> list:
        """Get valid info about vacancies for user"""
        self.all.clear()

        if isinstance(vacancy_name, str):
            keys_response = {'text': f'NAME:{vacancy_name}', 'area': 113, 'per_page': 100, }
            info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
            self.all.extend(json.loads(info.text)['items'])
            return self.all
        else:
            self.message = "Vacancy not found"
            return self.message

    def save_info(self, list_info: list, data: str) -> str or list:
        """Created json file with info about vacancies"""

        if len(list_info) == 0:
            self.message = "Vacancy not found"
            return self.message
        else:
            if pathlib.Path.exists(data) is not None:
                with open(data, 'w', encoding='utf-8') as file:
                    file.write(json.dumps(list_info, ensure_ascii=False))
                return self.all
            raise AttributeError
