from collections import defaultdict

from src.CompareVacancies import CompareVacancies


class UserInteraction(CompareVacancies):
    def __init__(self, name_vacancy):
        super().__init__(name_vacancy)
        self.save_info()
        self.vacancies = defaultdict(dict)

    def __str__(self):
        self.message = "Vacancy not found" if len(self.vacancies) == 0 else self.message
        return (f"Name of vacancy for search: {self.name_vacancy}\n"
                f"Count vacancies: {len(self.vacancies)}\n"
                f"Status: {self.message}")

    def choose_city(self, city: str, vacancies_dict: dict) -> dict:
        """
        Func for dort list with vacancies for city.
        :param vacancies_dict: dict with key of top
        salary and vacancies.
        :param city: user's city.
        :return: dict with vacancies for user.
        """

        right_top_vacancies = defaultdict(list)

        for salary, vacancies in vacancies_dict.items():
            for vacancy in vacancies:
                if vacancy['area']['name'] == city:
                    right_top_vacancies[salary].append(vacancy)
        return right_top_vacancies

    def make_info(self, count_vacancies: str, right_top_vacancies: dict) -> list:
        """
        Created list with vacancies for user.
        :param right_top_vacancies: dict with vacancies
        :param count_vacancies: how many vacancies
        user wants to see
        :return: list with vacancies.
        """
        if len(right_top_vacancies) < int(count_vacancies):
            count_vacancies = len(right_top_vacancies)

        for vacancy in right_top_vacancies.values():
            for index, value in enumerate(vacancy):
                self.vacancies[index + 1] = {"Name": value['name'],
                                             "Salary to": value['salary']['to'],
                                             "URL": value['alternate_url'],
                                             "Requirement": value['snippet']['requirement']}
                if len(self.vacancies) == int(count_vacancies):
                    break

        return self.vacancies

    def change_status(self):
        """
        Check status about requirement
        :return: True or False
        """
        return True if self.message == "Vacancies found" else False
