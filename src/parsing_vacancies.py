from abc import ABC, abstractmethod

from src.utils import ParsingManager, clean_salary_from_habr


class AbstractGetApi(ABC):
    @abstractmethod
    def __init__(self):
        self.all_vacancy: list = []

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_vacancy_from_api(self, name_vacancy: str) -> list:
        """Get valid info about vacancies for user"""
        pass


class ApiHh(AbstractGetApi):

    def __init__(self):
        self.all_vacancy: list = []
        self.employer_info: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, query_vacancies_list: list, pages_limit: int = 2) -> list:
        hh_url = f"https://api.hh.ru/vacancies"
        keys_response = {
            "text": " ".join(query_vacancies_list),
            "area": 113,
            "per_page": 100,
        }

        with ParsingManager(hh_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy

    @staticmethod
    def clean_vacancies_list(vacancies_list: list[dict]
                             ) -> list:
        """
        Clean list with info about vacancies.
        :param vacancies_list: list with vacancies dict.
        :return: list with info about vacancies.
        """
        sorted_vacancies_list = list()

        for vacancy in vacancies_list:
            temp_dict = {
                'Вакансия': vacancy.get('name', 'No title'),
                'Компания': vacancy.get('employer', {}).get('name', 'No company'),
                'Локация': vacancy.get('area', {}).get('name', 'No location'),
                'Описание': vacancy.get('snippet', {}).get('responsibility', 'No description'),
                'Ссылка': vacancy.get('alternate_url', 'No link'),
                'Опыт работы': vacancy.get('experience', {}).get('name', 'Not specified'),
            }

            if vacancy.get('salary', {}) is None:
                salary_from = salary_to = 0
            else:
                salary_from = vacancy.get('salary', {}).get('from', None)
                salary_to = vacancy.get('salary', {}).get('to', None)

            if salary_from and not salary_to:
                salary_to = salary_from
            elif not salary_from and salary_to:
                salary_from = 0

            temp_dict['Зарплата от'] = salary_from
            temp_dict['Зарплата до'] = salary_to
            sorted_vacancies_list.append(temp_dict)

        return sorted_vacancies_list


class ApiHabr(AbstractGetApi):
    def __init__(self):
        self.all_vacancy: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, query_vacancies_list: list, pages_limit: int = 2) -> list:
        querry = " ".join(query_vacancies_list)
        habr_url = "https://career.habr.com/vacancies?q=" + querry
        keys_response = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        with ParsingManager(habr_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy

    @staticmethod
    def clean_vacancies_list(vacancies_list: list[dict]
                             ) -> list:
        """
        Clean list with info about vacancies.
        :param vacancies_list: list with vacancies dict.
        :return: list with info about vacancies.
        """
        sorted_vacancies_list = list()

        for vacancy in vacancies_list:
            salary_from, salary_to = clean_salary_from_habr(vacancy['Зарплата'])
            temp_dict = {'Вакансия': vacancy['Вакансия'], 'Компания': vacancy['Компания'],
                         'Локация': vacancy['Локация'], 'Описание': vacancy['Описание'], 'Ссылка': vacancy['Ссылка'],
                         'Опыт работы': vacancy['Опыт работы'], 'Зарплата от': salary_from,
                         'Зарплата до': salary_to}

            sorted_vacancies_list.append(temp_dict)

        return sorted_vacancies_list


query_vacancies_list = ["python", "junior", "Python"]

hh = ApiHh()
habr = ApiHabr()

dirty_list_hh = hh.get_vacancy_from_api(query_vacancies_list, pages_limit=2)
clean_list_hh = hh.clean_vacancies_list(dirty_list_hh)

dirty_list_habr = habr.get_vacancy_from_api(query_vacancies_list, pages_limit=2)
clean_list_habr = habr.clean_vacancies_list(dirty_list_habr)

print(clean_list_habr)
print()
print(clean_list_hh)
