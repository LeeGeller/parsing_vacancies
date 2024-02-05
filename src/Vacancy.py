import json

import requests

from config import DATA
from src.AbstractHh import AbstractHh


class Vacancy(AbstractHh):
    all = []

    def __init__(self, name_vacancy, salary_min):
        self.name_vacancy = name_vacancy
        self.salary_min = int(salary_min)
        self.save_info()

    def get_vacancy_from_api(self):
        """Get valid info about vacancies for user"""
        self.all.clear()
        keys_response = {'text': f'NAME:{self.name_vacancy}', 'area': 113, 'per_page': 100,
                         "salary": self.salary_min}
        info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
        self.all.extend(json.loads(info.text)['items'])
        return self.all

    def save_info(self):
        """Created json file with info about vacancies"""
        self.sorted_all()

        with open(DATA, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.all, ensure_ascii=False))

    def sorted_all(self):
        """Sorted list to salary"""
        self.get_vacancy_from_api()
        new_list = []

        for item in self.all:
            try:
                if item.get("salary")["from"] == self.salary_min:
                    new_list.append(item)
            self.all = new_list
        return self.all



vacancy = Vacancy('python', 50000)

print(vacancy.all)
