import json
import re
import time

import aiohttp
from bs4 import BeautifulSoup


def check_len_vacancies_list(vacancies: list) -> list or None:
    """
    Check vacancies list is None.
    :param vacancies: list with info about vacancies.
    :return: list with info about vacancies.
    """
    return vacancies if vacancies is not None else "I dont found vacancies for you"


async def check_url(url: str, keys_response: dict):
    """
    Check url and created request to HH.ru or career.habr.com/vacancies.
    :param url: url
    :param keys_response: dict with keys
    :return: response
    """
    vacancies_response = []
    async with aiohttp.ClientSession() as session:
        if "habr" in url:
            try:
                async with session.get(url, headers=keys_response) as response:
                    if response.status == 200:
                        vacancies = BeautifulSoup(await response.text(), "html.parser")
                        vacancy_items = vacancies.find_all("div", class_="vacancy-card__inner")

                        for item in vacancy_items:
                            title_elem = item.find("a", class_="vacancy-card__title-link")
                            company_elem = item.find(
                                "a",
                                class_="link-comp link-comp--inherit vacancy-card__company-title",
                            )
                            location_elem = item.find(
                                "span", class_="link-comp link-comp--appearance-dark"
                            )
                            description_elem = item.find("div", class_="vacancy-card__description")
                            link_elem = item.find("a", class_="vacancy-card__title-link")

                            title = title_elem.text.strip() if title_elem else "No title"
                            company = company_elem.text.strip() if company_elem else "No company"
                            location = (
                                location_elem.text.strip() if location_elem else "No location"
                            )
                            description = (
                                description_elem.text.strip()
                                if description_elem
                                else "No description"
                            )
                            link = "https://career.habr.com" + link_elem['href'] if link_elem else "No link"

                            # Извлечение информации о зарплате
                            salary_elem = item.find('div', class_='basic-salary')
                            salary = salary_elem.text.strip() if salary_elem else "Не указана"

                            vacancy = {
                                "Вакансия": title,
                                "Компания": company,
                                "Локация": location,
                                "Описание": description,
                                "Ссылка": link,
                                'Опыт работы': 'На хабре не указано',
                                'Зарплата': salary,
                            }

                            vacancies_response.append(vacancy)

            except aiohttp.ClientError:
                print("Connection error")
        else:
            async with session.get(url, params=keys_response) as response:
                if response.status == 200:
                    vacancies_response = await response.json()["items"]
                else:
                    print(
                        f"Failed to retrieve vacancies from {url}. Status code: {response.status}"
                    )

    return vacancies_response


class ParsingManager:
    def __init__(self, url, keys_response, pages_limit=3):
        self.pages_limit = pages_limit
        self.url = url
        self.keys_response = keys_response
        self.vacancies_list = list()

    async def __aenter__(self):

        current_page = 0
        while current_page <= self.pages_limit:
            try:
                vacancies_response = await check_url(self.url, self.keys_response)

                if isinstance(vacancies_response, aiohttp.models.Response):
                    self.vacancies_list.extend(
                        json.loads(vacancies_response.text)["items"]
                    )
                elif isinstance(vacancies_response, list):
                    self.vacancies_list.extend(vacancies_response)

                current_page += 1
                time.sleep(2)
            except aiohttp.ClientError:
                print("Connection error")
        return check_len_vacancies_list(self.vacancies_list)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception occurred: {exc_type}, {exc_val}")
        else:
            print(f"Parsed {len(self.vacancies_list)} vacancies")


def clean_salary_from_habr(salary: str):
    salary_from = 0
    salary_to = 0

    salary_numbers = re.findall(r'\d+', salary.replace(' ', ''))

    if 'до' in salary and salary_numbers:
        salary_to = int(salary_numbers[-1])
    if 'от' in salary and salary_numbers:
        salary_from = int(salary_numbers[0])

    salary_to = salary_from if salary_to < salary_from else salary_to

    return salary_from, salary_to
