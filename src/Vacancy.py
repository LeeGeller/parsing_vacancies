from src.JsonSaver import JsonSaver


class Vacancy:
    list_vacancy = []

    def __init__(self, name_vacancy: str, salary_from: int, salary_to: int, url: str, city: str):
        self.name_vacancy = name_vacancy
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.url = url
        self.city = city
        self.list_vacancy.append(self.__dict__)

    def __repr__(self):
        return f"{self.list_vacancy}"

    def __str__(self):
        return (f"Name of vacancy: {self.name_vacancy}\n"
                f"Salary from: {self.salary_from}\n"
                f"Salary to: {self.salary_to}\n"
                f"City: {self.city}\n"
                f"URL: {self.url}")

    def __lt__(self, other):
        if self.salary_from is None and other.salary_from is None:
            if self.salary_to >= other.salary_to:
                return self.salary_to
            return other.salary_to
        elif self.salary_to is None and other.salary_to is None:
            if self.salary_from >= other.salary_from:
                return self.salary_from
            return other.salary_from
        elif self.salary_from is None and other.salary_from is not None:
            if self.salary_to >= other.salary_to:
                return self.salary_to
            return other.salary_to



print(Vacancy('python', 100, 200, 'url', 'city').list_vacancy)

# @classmethod
# def created_vacancy(cls, vacancy_list: list):
#     """Crested class of vacancy_list"""
#
#     for params in vacancy_list:
#         name_vacancy = params['name']
#         return cls.list_vacancy

# def sorted_salary(self, list_all: list, salary: int, city: str) -> dict:
#     """
#        Generate dict with necessary salary
#        with vacancies' list
#     """
#
#     for vacancy in list_all:
#         if vacancy["salary"] is not None and vacancy["salary"]["from"] is not None:
#             if vacancy["area"]["name"] == city:
#                 if vacancy["salary"]['from'] == salary and vacancy["salary"]['from'] is not None:
#                     self.sort_salary[vacancy["salary"]['from']].append(vacancy)
#     return self.sort_salary
#
# def get_top_vacancies(self, sort_salary) -> list:
#     """
#     Get top vacancies.
#     :return: list with vacancies.
#     """
#
#     for top, vacancy in sort_salary.items():
#         for value in vacancy:
#             if value["salary"] is not None and value["salary"]["to"] is not None:
#                 self.top_salary[value["salary"]["to"]].extend(vacancy)
#
#     self.top_salary = dict(sorted(self.top_salary.items(), reverse=True))
#
#     if len(self.top_salary) < 1:
#         self.message = "Vacancy not found"
#         return self.message
#
#     return self.top_salary
