import json

import requests

from src.AbstractHh import AbstractHh


class Vacancy(AbstractHh):

    def __init__(self, name_vacancy):
        self.name_vacancy = name_vacancy

    def get_vacancy_from_api(self):
        keys_response = {'professional_roles': {'name': self.name_vacancy}, 'area': 113}
        info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
        return json.loads(info.text)


vacancy = Vacancy('python')
print(vacancy.get_vacancy_from_api())
