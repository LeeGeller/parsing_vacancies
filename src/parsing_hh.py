import json
from abc import ABC, abstractmethod
from typing import Any
import requests
from config import config

from config import DATA
import psycopg2


class AbstractGetApiHh(ABC):

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def get_vacancy_from_api(self, name_vacancy):
        pass


class GetApiHh(AbstractGetApiHh):

    def __init__(self):
        self.all_vacancy = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, name_vacancy) -> list:
        """Get valid info about vacancies for user"""
        keys_response = {'text': f'NAME:{name_vacancy}', 'area': 113, 'per_page': 100, }
        info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
        self.all_vacancy = json.loads(info.text)['items']
        return self.all_vacancy


class AbstractJsonSaver(ABC):

    @abstractmethod
    def save_file(self, data: list):
        pass

    @abstractmethod
    def read_file(self):
        pass


class JsonSaver(AbstractJsonSaver):

    def save_file(self, data: list):
        """Save file"""
        with open(DATA, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))

    def read_file(self):
        """Read file"""
        with open(DATA, encoding='utf-8') as file:
            return json.load(file)

    def add_vacancy_to_file(self, data: list):
        old_list = self.read_file()
        new_list = data + old_list
        self.save_file(new_list)

    def delete_vacancy(self, vacancy: str):
        new_list = []

        old_list = self.read_file()

        for params in old_list:
            if params['name'] != vacancy:
                new_list.append(params)

        self.save_file(new_list)


class Vacancy:
    list_vacancies = []

    def __init__(self, name_vacancy: str, salary_from: int, salary_to: int, url: str, city: str):
        self.name_vacancy = name_vacancy
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.url = url
        self.city = city
        self.list_vacancies.append(self)

    def __repr__(self):
        return (f"\nName of vacancy: {self.name_vacancy}\n"
                f"Salary from: {self.salary_from}\n"
                f"Salary to: {self.salary_to}\n"
                f"City: {self.city}\n"
                f"URL: {self.url}\n")

    def __lt__(self, other):
        if other.salary_to < self.salary_to:
            return True

    @staticmethod
    def sorted_vacancy_list(list_vacancy: list, city: str, salary_from) -> list[dict[str: Any]]:
        """
        Sorted list arguments.
        :param list_vacancy: list with info about vacancies
        :param city: city, which choice user
        :param salary_from: salary, which choice user
        :return: new sorted list
        """
        new_list = list()

        for vacancy in list_vacancy:
            name_vacancy = vacancy["name"]
            url = vacancy["alternate_url"]
            if vacancy["area"]["name"] == city:
                city = vacancy["area"]["name"]
            if vacancy["salary"] is None:
                continue
            elif vacancy["salary"]["from"] and vacancy["salary"]["to"]:
                if vacancy["salary"]["from"] >= salary_from:
                    salary_from = vacancy["salary"]["from"]
                    salary_to = vacancy["salary"]["to"]
                    new_list.append(
                        {'Name vacancy': name_vacancy, 'Salary from': salary_from, 'Salary to': salary_to, 'URL': url,
                         'City': city})
                else:
                    continue
            else:
                continue
        return new_list

    @classmethod
    def get_vacancy_list(cls, list_vacancy: list) -> list:
        """
        Get list with vacancies dicts. This list with copy of class Vacancy
        :return: new lisrt with copy of class Vacancy
        """
        for vacancy in list_vacancy:
            cls(vacancy['Name vacancy'], vacancy['Salary from'], vacancy['Salary to'], vacancy['URL'],
                vacancy['City'])
        return cls.list_vacancies


class DBManager:
    def create_data_base(self, name_db: str, params: dict) -> None:
        """
        Create database and tables.
        :param params: parameters for connect with postgresql
        :param name_db: name of database
        """

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f'DROP DATABASE {name_db}')
        cur.execute(f'CREATE DATABASE {name_db}')

        cur.close()
        conn.close()
        print("Database created")

    def create_table(self, name_db: str, params: dict) -> None:
        """
        Create table for database.
        :param name_db: name of database
        :param params: parameters for connect with postgresql
        """
        with psycopg2.connect(dbname=name_db, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
            CREATE TABLE info_vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                name_vacancy VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                city VARCHAR(100),
                url TEXT
            )
        """)
        conn.close()
        print("Tables created")

    def save_data_to_database(self, data_file: list[dict[str: Any]], name_bd: str, params: dict) -> None:
        """
        Save data info about vacancies.
        :param data_file: info about vacancies for save
        :param name_bd: name of database
        :param params: parameters for connect with postgresql
        """

        conn = psycopg2.connect(dbname=name_bd, **params)
        with conn.cursor() as cur:
            for data in data_file:
                count_columns = '%s ' * len(data)
                val = tuple(data.values())
                cur.execute(f"INSERT INTO info_vacancies (name_vacancy, salary_from, salary_to, city, url) "
                            f"VALUES({', '.join(count_columns.split())})", val)
        conn.commit()
        conn.close()
        print(f"Info about vacancies save in database: {name_bd} in table info_vacancies.")


response = GetApiHh()
# Get vacancies for user
response.get_vacancy_from_api('оператор')

file_json = JsonSaver()

# Save response to JSON
file_json.save_file(response.all_vacancy)

# Read JSON file
file_vacancies = file_json.read_file()

sorted_list = Vacancy.sorted_vacancy_list(file_vacancies, 'Москва', 0)
# Print vacancies for user
vacancy = Vacancy.get_vacancy_list(sorted_list)
sorted_vacancies = sorted(vacancy)

print(*sorted_vacancies[:10])

d_base = DBManager()
params = config()
d_base.create_data_base('vacancies', params)
d_base.create_table('vacancies', params)

d_base.save_data_to_database(sorted_list, 'vacancies', params)
