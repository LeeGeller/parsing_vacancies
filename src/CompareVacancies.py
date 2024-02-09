from src.GetVacancies import GetVacancies
from collections import defaultdict


class CompareVacancies(GetVacancies):
    def __init__(self, name_vacancy: str):
        super().__init__(name_vacancy)
        self.salary_all: dict = defaultdict(list)
        self.all = self.save_info()

    def generate_salary_dict(self, list_all: list, salary: int) -> dict:
        """
           Generate dict with necessary salary
           with vacancies' list
        """
        salary_dict = defaultdict(list)

        for vacancy in list_all:
            if vacancy["salary"] is not None and vacancy["salary"]["from"] is not None:
                salary_dict[vacancy["salary"]['from']].append(vacancy)

        for key, vacancy in salary_dict.items():
            if key == int(salary):
                self.salary_all[salary].extend(vacancy)

        return self.salary_all

    def get_top_vacancies(self, necessary_salary) -> list:
        """
        Get top vacancies.
        :return: list with vacancies.
        """
        salary_top = defaultdict(list)

        for top, vacancy in necessary_salary.items():
            for value in vacancy:
                if value["salary"] is not None and value["salary"]["to"] is not None:
                    salary_top[value["salary"]["to"]].extend(vacancy)

        salary_top = dict(sorted(salary_top.items(), reverse=True))

        if len(salary_top) < 1:
            self.message = "Vacancy not found"
            return self.message

        return salary_top
