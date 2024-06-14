import json
import time

import requests


def check_len_vacancies_list(vacancies: list) -> list or None:
    """ Check vacancies list is None"""
    return vacancies if vacancies is not None else 'I dont found vacancies for you'


class ParsingManager:
    def __init__(self, url, keys_response, pages_limit=3):
        self.pages_limit = pages_limit
        self.url = url
        self.keys_response = keys_response
        self.vacancies_list = list()

    def __enter__(self):

        current_page = 0
        while current_page <= self.pages_limit:
            try:
                info: json = requests.get(self.url, params=self.keys_response)
                self.vacancies_list.extend(json.loads(info.text)['items'])
                current_page += 1
                time.sleep(1)
            except requests.exceptions.RequestException:
                print('Connection error')
        return check_len_vacancies_list(self.vacancies_list)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f'Exception occurred: {exc_type}, {exc_val}')
        else:
            print(f'Parsed {len(self.vacancies_list)} vacancies')
