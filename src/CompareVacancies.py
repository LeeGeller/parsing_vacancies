from src.GetVacancies import GetVacancies
from collections import defaultdict


class CompareVacancies(GetVacancies):
    def __init__(self, name_vacancy: str):
        super().__init__(name_vacancy)
        self.salary_all: dict = {}
        self.all = self.save_info()

    def generate_salary_dict(self, list_all: list) -> dict:
        """
           Created dict where key is salary. And generate dict
           with vacancies' list
        """

        self.salary_all = defaultdict(list)

        for vacancy in list_all:
            if vacancy["salary"] is None or vacancy["salary"]["from"] is None:
                self.salary_all['from_None'].append(vacancy)
            else:
                self.salary_all[vacancy["salary"]['from']].append(vacancy)
        return self.salary_all

    def get_vacancies(self, salary_dict: dict, salary: int or str) -> list:
        """
           Get vacancies with necessary salary.
           If vacancies not found return that vacancies not found.
        """
        if len(salary_dict) < 1:
            self.message = "Vacancy not found"
            return self.message
        else:
            if salary == "":
                self.salary_all = salary_dict["from_None"]
                return self.salary_all
            elif isinstance(salary, int):
                self.salary_all = salary_dict[int(salary)]
                return self.salary_all

    def get_top_vacancies(self) -> list:
        """
        Get top vacancies.
        :return: list with vacancies.
        """
        salary_top = defaultdict(dict)
        for salary, vacancy in self.salary_all.items():
            if salary != 'from_None':
                for value in vacancy:
                    if value["salary"] is False:
                        continue
                    elif value["salary"]["to"] is not None:
                        salary_top[value["salary"]["to"]] = vacancy
        salary_top = dict(sorted(salary_top.items(), reverse=True))
        if len(salary_top) < 1:
            self.message = "Vacancy not found"
            return self.message
        self.salary_all = salary_top
        return self.salary_all
