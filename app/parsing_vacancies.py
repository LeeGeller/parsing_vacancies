from abc import ABC, abstractmethod

from app.utils import ParsingManager, clean_salary_from_habr


class AbstractGetApi(ABC):
    @abstractmethod
    def __init__(self):
        self.all_vacancy: list = []

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    async def get_vacancy_from_api(self, name_vacancy: str) -> list:
        """Get valid info about vacancies for user"""
        pass


class ApiHh(AbstractGetApi):

    def __init__(self):
        self.all_vacancy: list = []
        self.employer_info: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    async def get_vacancy_from_api(self, query_vacancies_list: list, pages_limit: int = 2) -> list:
        hh_url = f"https://api.hh.ru/vacancies"
        keys_response = {
            "text": " ".join(query_vacancies_list),
            "area": 113,
            "per_page": 100,
        }

        async with ParsingManager(hh_url, keys_response, pages_limit) as vacancies:
            self.all_vacancy = vacancies
        return self.all_vacancy

    @staticmethod
    def clean_vacancies_list(vacancies_list: list[dict]) -> list:
        """
        Clean list with info about vacancies.
        :param vacancies_list: list with vacancies dict.
        :return: list with info about vacancies.
        """
        sorted_vacancies_list = list()

        # Отладочный вывод
        print("Полученные вакансии:", vacancies_list)

        for vacancy in vacancies_list:
            temp_dict = {
                'name_vacancy': vacancy.get('name', 'No title'),
                'company': vacancy.get('employer', {}).get('name', 'No company'),
                'location': vacancy.get('area', {}).get('name', 'No location'),
                'description': vacancy.get('snippet', {}).get('responsibility', 'No description'),
                'url': vacancy.get('alternate_url', 'No link'),
                'experience': vacancy.get('experience', {}).get('name', 'Not specified'),
            }

            if not vacancy.get('salary'):
                salary_from = salary_to = 0
            else:
                salary_from = vacancy.get('salary', {}).get('from', None)
                salary_to = vacancy.get('salary', {}).get('to', None)

            if salary_from is None:
                salary_from = 0
            if salary_to is None:
                salary_to = 0

            if salary_from and not salary_to:
                salary_to = salary_from
            elif not salary_from and salary_to:
                salary_from = 0

            temp_dict['salary_from'] = salary_from
            temp_dict['salary_to'] = salary_to
            sorted_vacancies_list.append(temp_dict)

        return sorted_vacancies_list


class ApiHabr(AbstractGetApi):
    def __init__(self):
        self.all_vacancy: list = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    async def get_vacancy_from_api(self, query_vacancies_list: list, pages_limit: int = 2) -> list:
        querry = " ".join(query_vacancies_list)
        habr_url = "https://career.habr.com/vacancies?q=" + querry
        keys_response = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        async with ParsingManager(habr_url, keys_response, pages_limit) as vacancies:
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
        sorted_vacancies_list = []

        for vacancy in vacancies_list:
            salary_from, salary_to = clean_salary_from_habr(vacancy['Зарплата'])
            temp_dict = {'name_vacancy': vacancy['Вакансия'], 'company': vacancy['Компания'],
                         'location': vacancy['Локация'], 'description': vacancy['Описание'], 'url': vacancy['Ссылка'],
                         'experience': vacancy['Опыт работы'], 'salary_from': salary_from,
                         'salary_to': salary_to}

            sorted_vacancies_list.append(temp_dict)

        return sorted_vacancies_list

# a = ApiHh()
# b = ApiHabr()
#
# async def main():
#     result_a = await a.get_vacancy_from_api(['Python'])
#     result_b = await b.get_vacancy_from_api(['Python'])
#
#     print(result_a)
#     print(result_b)
#
# asyncio.run(main())
