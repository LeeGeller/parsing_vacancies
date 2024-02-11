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
        return (f"\nName of vacancy: {self.name_vacancy}\n"
                f"Salary from: {self.salary_from}\n"
                f"Salary to: {self.salary_to}\n"
                f"City: {self.city}\n"
                f"URL: {self.url}\n")

    def __str__(self):
        return (f"Name of vacancy: {self.name_vacancy}\n"
                f"Salary from: {self.salary_from}\n"
                f"Salary to: {self.salary_to}\n"
                f"City: {self.city}\n"
                f"URL: {self.url}")

    def __lt__(self, other):
        if other.salary_to < self.salary_to:
            return True
