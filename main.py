
from app.parsing_vacancies import ApiHh, ApiHabr
from database.queries.orm import VacanciesORM

query_vacancies_list = ["python", "Python", 'Python developer', 'Python junior']

hh = ApiHh()
habr = ApiHabr()

dirty_list_hh = hh.get_vacancy_from_api(query_vacancies_list, pages_limit=2)
clean_list_hh = hh.clean_vacancies_list(dirty_list_hh)

dirty_list_habr = habr.get_vacancy_from_api(query_vacancies_list, pages_limit=2)
clean_list_habr = habr.clean_vacancies_list(dirty_list_habr)

VacanciesORM.create_table()

VacanciesORM.insert_data(clean_list_hh + clean_list_habr)
print(VacanciesORM.select_data())