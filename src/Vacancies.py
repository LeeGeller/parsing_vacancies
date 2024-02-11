from src.GetApiHh import GetApiHh
from src.JsonSaver import JsonSaver
from src.Vacancy import Vacancy


class Vacancies(Vacancy):

    @classmethod
    def get_vacancy_list(cls, vacancies, city: str, salary_from: int) -> list:
        """
        Get list with vacancies dicts. This list with copy of class Vacancy
        :return: new lisrt with copy of class Vacancy
        """
        new_list = []
        for vacancy in vacancies:
            name_vacancy = vacancy["name"]
            url = vacancy["alternate_url"]
            if vacancy["area"]["name"] == city:
                city = vacancy["area"]["name"]
            if vacancy["salary"] is None:
                continue
            elif vacancy["salary"]["to"] is not None and vacancy["salary"]["from"] is not None:
                if vacancy["salary"]["from"] == salary_from:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                else:
                    continue
            else:
                continue
            new_list.append(cls(name_vacancy, salary_from, salary_to, url, city))
        return new_list


response = GetApiHh()
response.get_vacancy_from_api('python')
file_json = JsonSaver()
file_json.save_file(response.all_vacancy)
file_vacancies = file_json.read_file()
vacancy = Vacancies.get_vacancy_list(file_vacancies, 'Москва', 50000)

print(sorted(vacancy))
