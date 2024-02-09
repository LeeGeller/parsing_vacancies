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
        self.save_info()

    def get_vacancy_from_api(self) -> list:
        """Get valid info about vacancies for user"""
        self.all.clear()

        if isinstance(self.name_vacancy, str):
            keys_response = {'text': f'NAME:{self.name_vacancy}', 'area': 113, 'per_page': 100, }
            info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
            self.all.extend(json.loads(info.text)['items'])
            return self.all
        else:
            self.message = "Vacancy not found"
            return self.message

    def save_info(self) -> str or list:
        """Created json file with info about vacancies"""
        self.get_vacancy_from_api()

        if len(self.all) == 0:
            self.message = "Vacancy not found"
            return self.message
        else:
            with open(DATA, 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.all, ensure_ascii=False))
            return self.all
