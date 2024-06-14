from config import config
from src.parsing_vacancies import GetApiHh


def main():
    response = GetApiHh()

    data = response.get_vacancy_from_api("python, junior")
    print(data)


if __name__ == "__main__":
    main()
