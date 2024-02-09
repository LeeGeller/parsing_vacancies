from collections import defaultdict

from src.CompareVacancies import CompareVacancies


class UserInteraction(CompareVacancies):
    def __init__(self, name_vacancy):
        super().__init__(name_vacancy)
        self.get_vacancy_from_api()
        self.vacancies = defaultdict(list)

    def __str__(self):
        self.message = "Vacancy not found" if len(self.all_vacancy) == 0 else self.message
        return (f"Name of vacancy for search: {self.name_vacancy}\n"
                f"Count vacancies: {len(self.all_vacancy)}\n"
                f"Status: {self.message}")

    def make_info(self, top_salary: dict) -> list:
        """
        Created list with vacancies for user.
        :param right_top_vacancies: dict with vacancies
        :param count_vacancies: how many vacancies
        user wants to see
        :return: list with vacancies.
        """
        print(f"Top salary:")

        for top, vacancies in top_salary.items():
            print(f"Top sallary {top} - count {len(vacancies)}")


user = UserInteraction('python')

user.sorted_salary(user.all_vacancy, 50000, 'Москва')
user.get_top_vacancies(user.sort_salary)

user.make_info(user.top_salary)
