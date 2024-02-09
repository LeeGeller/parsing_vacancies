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
            if salary == "from_None":
                self.salary_all = salary_dict["from_None"]
                return self.salary_all
            elif isinstance(salary, int):
                self.salary_all = salary_dict[salary]
                return self.salary_all

    def get_top_vacancies(self) -> list:
        """
        Get top vacancies.
        :return: list with vacancies.
        """
        salary_top = defaultdict(list)
        for vacancy in self.salary_all:
            vacancy_salary = vacancy.get("salary")
            if vacancy_salary is None or vacancy_salary.get("to") is None:
                continue
            elif vacancy_salary:
                salary_top[vacancy["salary"]["to"]].append(vacancy)
        salary_top = dict(sorted(salary_top.items(), reverse=True))
        self.all = salary_top
        if len(self.all) < 1:
            self.message = "Vacancy not found"
            return self.message
        return self.all

