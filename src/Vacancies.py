from src.GetApiHh import GetApiHh
from src.JsonSaver import JsonSaver
from src.Vacancy import Vacancy


class Vacancies(Vacancy):
    vacansies_for_user = []

    def __init__(self, list_vacancies):
        for vacancy in list_vacancies:
            self.vacansies_for_user.append(vacancy)

    @classmethod
    def get_vacancy_list(cls, name_vacancy, salary_from, salary_to, url, city):
        new_list = []
        for vacancy in cls.vacansies_for_user:
            name_vacancy = vacancy["name"]
            url = vacancy["name"]["alternate_url"]
            city = vacancy["area"]["name"]
            if vacancy["salary"] is None or vacancy["salary"]["from"] is None:
                salary_from = 0
            else:
                salary_from = vacancy["salary"]["from"]
            if vacancy["salary"] is None or vacancy["salary"]["to"] is not None:
                salary_to = vacancy["salary"]["to"]
            else:
                salary_to = 0
            new_list.append(cls(name_vacancy, salary_from, salary_to, url, city))


response = GetApiHh()
response.get_vacancy_from_api('python')
file_json = JsonSaver()
file_json.save_file(response.all_vacancy)
file_vacancies = file_json.read_file()
vacancy = Vacancies(file_vacancies)
print(vacancy.vacansies_for_user)
