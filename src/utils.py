import json
import time

import requests
from bs4 import BeautifulSoup


def check_len_vacancies_list(vacancies: list) -> list or None:
    """
    Check vacancies list is None.
    :param vacancies: list with info about vacancies.
    :return: list with info about vacancies.
    """
    return vacancies if vacancies is not None else 'I dont found vacancies for you'


def check_url(url: str, keys_response: dict):
    """
    Check url and created request to HH.ru or career.habr.com/vacancies.
    :param url: url
    :param keys_response: dict with keys
    :return: response
    """
    vacancies_response = list()
    if 'habr' in url:
        try:
            response = requests.get(url, headers=keys_response)
            vacancies = BeautifulSoup(response.content, 'html.parser')
            vacancy_items = vacancies.find_all('div', class_='vacancy-card__inner')

            for item in vacancy_items:
                title_elem = item.find('a', class_='vacancy-card__title-link')
                company_elem = item.find('a', class_='link-comp link-comp--inherit vacancy-card__company-title')
                location_elem = item.find('span', class_='link-comp link-comp--appearance-dark')
                description_elem = item.find('div', class_='vacancy-card__description')

                title = title_elem.text.strip() if title_elem else 'No title'
                company = company_elem.text.strip() if company_elem else 'No company'
                location = location_elem.text.strip() if location_elem else 'No location'
                description = description_elem.text.strip() if description_elem else 'No description'

                vacancy = {
                    'title': title,
                    'company': company,
                    'location': location,
                    'description': description
                }
                vacancies_response.append(vacancy)

        except requests.exceptions.RequestException:
            print('Connection error')

    else:
        response = requests.get(url, params=keys_response)
        if response.status_code == 200:
            vacancies_response = json.loads(response.text)['items']
        else:
            print(f'Failed to retrieve vacancies from {url}. Status code: {response.status_code}')

    return vacancies_response


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
                vacancies_response = check_url(self.url, self.keys_response)

                if isinstance(vacancies_response, requests.models.Response):
                    self.vacancies_list.extend(json.loads(vacancies_response.text)['items'])
                elif isinstance(vacancies_response, list):
                    self.vacancies_list.extend(vacancies_response)

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
