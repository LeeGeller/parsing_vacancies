from config import config
from src.parsing_hh import GetApiHh, JsonSaver, Vacancy, DBManager


def main():
    response = GetApiHh()

    while True:
        user_vacancy: str = input("Text name vacancy for search:\n")
        user_city: str = input("Text city in where you want to find vacancies:\n")
        if isinstance(user_city, str) and isinstance(user_vacancy, str):
            break
        print(f"Please, text alpha, not {user_city}")

    while True:
        user_salary = input("Text min salary for search:\n")
        if user_salary.isdigit():
            break
        print(f"Please, text digit, not {user_salary}")

    # Get vacancies for user
    response.get_vacancy_from_api(user_vacancy)

    file_json = JsonSaver()

    # Save response to JSON
    file_json.save_file(response.all_vacancy)

    # Read JSON file
    file_vacancies = file_json.read_file()

    # Sorted file with vacancies
    sorted_list = Vacancy.sorted_vacancy_list(file_vacancies, user_city, int(user_salary))

    # Print vacancies for user
    vacancy = Vacancy.get_vacancy_list(sorted_list)
    sorted_vacancies = sorted(vacancy)

    while True:
        count = input("How vacancies do you want to see:\n")
        if count.isdigit():
            break
        print(f"Please, text digit, not {count}")

    print(*sorted_vacancies[:int(count)])

    d_base = DBManager()
    params = config()

    # Create database
    d_base.create_data_base('vacancies', params)

    # Create tables
    d_base.create_table('vacancies', params)

    # Save info to database
    d_base.save_data_to_database(sorted_vacancies, 'vacancies', params)


if __name__ == '__main__':
    main()
