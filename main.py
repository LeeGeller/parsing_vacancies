
from app.parsing_vacancies import ApiHh, ApiHabr
from database.queries.orm import VacanciesORM

query_vacancies_list = ['Python developer', 'Python разработчик']

hh = ApiHh()
habr = ApiHabr()

dirty_list_hh = hh.get_vacancy_from_api(query_vacancies_list, pages_limit=5)
clean_list_hh = hh.clean_vacancies_list(dirty_list_hh)

dirty_list_habr = habr.get_vacancy_from_api(query_vacancies_list, pages_limit=5)
clean_list_habr = habr.clean_vacancies_list(dirty_list_habr)

VacanciesORM.create_table()

VacanciesORM.insert_data(clean_list_hh + clean_list_habr)



top_vacancies = VacanciesORM.get_top_vacancies_without_experience(limit=20)

all_vacancies_without_experience_and_salary = VacanciesORM.get_vacancies_without_experience_and_salary()

avg_salaries = VacanciesORM.get_avg_salary()
min_salary = VacanciesORM.get_min_salary()
max_salary = VacanciesORM.get_max_salary()
top_salary = VacanciesORM.get_top_vacancies(limit=5)

print(top_salary)

