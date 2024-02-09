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

        for index, value in enumerate(self.all):
            if value['area']['name'] == city:
                self.vacancies.append(value)
        self.generate_salary_dict(self.vacancies)
        self.vacancies = self.get_top_vacancies()
        return self.vacancies


