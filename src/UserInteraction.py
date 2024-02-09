from collections import defaultdict

from src.CompareVacancies import CompareVacancies


class UserInteraction(CompareVacancies):
    def __init__(self, name_vacancy):
        super().__init__(name_vacancy)
        self.get_vacancy_from_api()
        self.vacancies_list = defaultdict(list)

    def __str__(self):
        self.message = "Vacancy not found" if len(self.all_vacancy) == 0 else self.message
        return (f"Name of vacancy for search: {self.name_vacancy}\n"
                f"Count vacancies: {len(self.all_vacancy)}\n"
                f"Status: {self.message}")

    def make_info(self, top_salary: dict) -> list:
        """
        Created list with vacancies for user.
        :param top_salary: dict with vacancies
        user wants to see
        :return: list with vacancies.
        """
        print(f"Top salary:")
        count = 1

        for top, vacancies in top_salary.items():
            print(f"{count}. Top sallary {top} - count {len(vacancies)}")
            for value in vacancies:
                self.vacancies_list[count].extend([{"Name of vacancy": value['name']},
                                                   {"Salary from": value['salary']['from']},
                                                   {"Salary to": value['salary']['to']},
                                                   {"City": value['area']['name']},
                                                   {"URL": value['alternate_url']}])
                count += 1

    def last_info(self, top_salary: dict, number_of_vacancies: int):
        """
            Get info about top vacancies
            :param top_salary: dict with top vacancies
        """
        for params_vacancy in top_salary[number_of_vacancies]:
            for key, val in params_vacancy.items():
                print("{0}: {1}".format(key, val))



user = UserInteraction('python')

user.sorted_salary(user.all_vacancy, 50000, 'Москва')
user.get_top_vacancies(user.sort_salary)

user.make_info(user.top_salary)

user.last_info(user.vacancies_list, 8)
