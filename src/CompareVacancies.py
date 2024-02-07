from src.Vacancy import Vacancy
from collections import defaultdict


class CompareVacancies(Vacancy):
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
            if vacancy['salary'] is None:
                self.salary_all[None].append(vacancy)
            elif vacancy['salary']['from'] is None:
                self.salary_all['from_None'].append(vacancy)
            else:
                self.salary_all[vacancy['salary']['from']].append(vacancy)
        return self.salary_all

    # def get_vacancy(self) -> list:
    #     """
    #        Get vacancies with necessary salary.
    #        If vacancies not found return that vacancies not found.
    #     """
    #     self.generate_salary_dict()
    #     if self.salary == '':
    #         for value in self.salary_all.values():
    #             return value
    #     elif self.salary == 'None':
    #         return self.salary_all.get(self.salary)


v = CompareVacancies('python', 'None')
print(v.get_vacancy_from_api())
