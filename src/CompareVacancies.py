from src.GetVacancies import GetVacancies
from collections import defaultdict


class CompareVacancies(GetVacancies):
    def __init__(self, name_vacancy: str, salary=''):
        super().__init__(name_vacancy)
        self.salary = salary
        self.salary_all: dict = {}

    def generate_salary_dict(self) -> dict:
        """
           Created dict where key is salary. And generate dict
           with vacancies' list
        """
        self.salary_all = defaultdict(list)

        for vacancy in self.all:
            if vacancy["salary"] is None or vacancy["salary"]["from"] is None:
                self.salary_all['from_None'].append(vacancy)
            else:
                self.salary_all[vacancy["salary"]['from']].append(vacancy)
        return self.salary_all

    def get_vacancies(self) -> list:
        """
           Get vacancies with necessary salary.
           If vacancies not found return that vacancies not found.
        """
        self.generate_salary_dict()
        if self.salary == '':
            return self.salary_all
        elif self.salary == "from_None":
            return self.salary_all.get("from_None")
        else:
            if len(self.salary_all[self.salary]) == 0:
                return (f"I not found vacancies with this salary.\n"
                        f"Check your salary: '{self.salary}' for search.\n"
                        f"It must be integer. Not float or string.\n")
            return self.salary_all[self.salary]

    def get_top_vacancies(self) -> list:
        """
        Get top vacancies.
        :return: list with vacancies.
        """
        self.salary_top = defaultdict(list)
        vacancies = self.get_vacancies()
        for vacancy in vacancies:
            if vacancy["salary"]["to"] is not None:
                self.salary_top[vacancy["salary"]["to"]].append(vacancy)
        self.salary_top = dict(sorted(self.salary_top.items(), reverse=True))
        return self.salary_top
