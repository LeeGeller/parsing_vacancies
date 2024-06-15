from abc import ABC, abstractmethod

from src.utils import ParsingManager


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

    def get_vacancy_from_api(self, name_vacancy: list, pages_limit: int = 2) -> list:
        hh_url = f"https://api.hh.ru/vacancies"
        keys_response = {
            "text": " ".join(name_vacancy),
            "area": 113,
            "per_page": 100,
        }

        with ParsingManager(hh_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy


class ApiHabr(AbstractGetApi):
    def __init__(self):
        self.all_vacancy: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, pages_limit: int = 2) -> list:
        habr_url = "https://career.habr.com/vacancies"
        keys_response = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        with ParsingManager(habr_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy

    @staticmethod
    def clean_vacancies_list(
            name_vacancy: list, vacancies_list: list[dict]
    ) -> list:
        """
        Clean list with info about vacancies.
        :param vacancies_list: list with vacancies dict.
        :param name_vacancy: list with info about vacancies.
        :return: list with info about vacancies.
        """
        sort_vacancies_list = list()
        vacancy_name_lower_word = list(map(lambda word: word.lower(), name_vacancy))
        vacancy_names_words = vacancy_name_lower_word + list(map(lambda word: word.capitalize(), name_vacancy))

        for vacancy_dict in vacancies_list:
            if any(word in vacancy_dict.get('Вакансия') for word in vacancy_names_words):
                sort_vacancies_list.append(vacancy_dict)

        return sort_vacancies_list


vacancies_fetcher = ApiHh()
name_vacancy_hh = ["python", "junior"]
print("Vacancies from HH.ru API:")
print(vacancies_fetcher.get_vacancy_from_api(name_vacancy_hh, pages_limit=2))

# Пример использования ApiHabr
v = ApiHabr()
name_vacancy_habr = ["python", "junior", "Python"]
print("\nVacancies from Habr Career:")
dirty_list = v.get_vacancy_from_api(pages_limit=2)
clean_list = v.clean_vacancies_list(name_vacancy_habr, dirty_list)
print(clean_list)
