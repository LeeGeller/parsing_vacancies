from src.GetApiHh import GetApiHh
from src.JsonSaver import JsonSaver
from src.Vacancy import Vacancy

response = GetApiHh()
response.get_vacancy_from_api('python')
file_json = JsonSaver()
file_json.save_file(response.all_vacancy)
file_vacancies = file_json.read_file()
vacancy = Vacancy.get_vacancy_list(file_vacancies, 'Москва', 50000)

print(*sorted(vacancy))
