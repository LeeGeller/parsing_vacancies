from collections import defaultdict
from copy import deepcopy

from src.CompareVacancies import CompareVacancies


class UserInteraction(CompareVacancies):
    def __init__(self, name_vacancy):
        super().__init__(name_vacancy)
        self.save_info()
        self.vacancies = []


    def __str__(self):
        self.message = "Vacancy not found" if len(self.vacancies) == 0 else self.message
        return (f"Name of vacancy for search: {self.name_vacancy}\n"
                f"Count vacancies: {len(self.vacancies)}\n"
                f"Status: {self.message}")

    def choose_city(self, city: str) -> dict:
        """
        Func for dort list with vacancies for city.
        :param city: user's city.
        :return: dict with vacancies for user.
        """

        vacancies = []

        if city == '1':
            return self.generate_salary_dict(self.all)
        else:
            for value in self.all:
                if value['area']['name'] == city:
                    vacancies.extend(value)
        return self.generate_salary_dict(vacancies)

    def make_info(self, count_vacancies: int) -> list:
        """
        Created list with vacancies for user.
        :param count_vacancies: how many vacancies
        user wants to see
        :return: list with vacancies.
        """
        count_vacancies = count_vacancies
        self.get_top_vacancies()
        while count_vacancies > 0:
            for top_salary, vacancies in self.salary_all.items():
                for vacancy in vacancies:
                    title = vacancy['name']
                    area = vacancy['area']['name']
                    salary_from = vacancy['salary']['from']
                    salary_to = vacancy['salary']['to']
                    url = vacancy['alternate_url']
                    description = vacancy['snippet']['requirement']
                    experience = vacancy['experience']['name']
                    self.vacancies.append(
                        {title: [area, salary_from, salary_to, description, experience, url]})
                    count_vacancies -= 1
        return self.vacancies
