import requests

from src.AbstractHh import AbstractHh


class Vacancy(AbstractHh):

    def __init__(self, name_vacancy):
        self.name_vacancy = name_vacancy

    def get_vacancy_from_api(self):
        info = requests.get(f'https://api.hh.ru/vacancies?text=NAME:{self.name_vacancy}')
        return info.text

vacancy = Vacancy('python')
print(vacancy.get_vacancy_from_api())