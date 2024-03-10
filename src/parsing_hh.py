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
        self.employer_info = []

    def __repr__(self):
        return f"{self.all_vacancy}"

    def get_vacancy_from_api(self, name_vacancy) -> list:
        """Get valid info about vacancies for user"""
        keys_response = {'text': {name_vacancy}, 'area': 113, 'per_page': 100, }
        info = requests.get(f'https://api.hh.ru/vacancies', keys_response)
        self.all_vacancy = json.loads(info.text)['items']
        return self.all_vacancy

    def get_info_about_employer(self, employer_id: int) -> list:
        """Get valid info about employer for user"""
        info = requests.get(f'https://api.hh.ru/employers/{employer_id}')
        self.employer_info = json.loads(info.text)
        return self.employer_info


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

    def __init__(self, name_vacancy: str, salary_from: int, salary_to: int, employer_id: int,
                 url: str, city: str, experience: str):
        self.name_vacancy = name_vacancy
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.employer_id = employer_id
        self.url = url
        self.city = city
        self.experience = experience

    def __repr__(self):
        return (f"Name{self.name_vacancy}, {self.salary_from}, {self.salary_to}, "
                f"{self.employer_id}, {self.url}, {self.city}, {self.experience}")

    def __lt__(self, other):
        if other.salary_to < self.salary_to:
            return True

    @staticmethod
    def sorted_vacancy_list(list_vacancy: list) -> list[dict[str: Any]]:
        """
        Sorted list arguments.
        :param list_vacancy: list with info about vacancies
        :return: new sorted list
        """
        new_list = list()

        for vacancy_info in list_vacancy:
            if vacancy_info["salary"] is None:
                continue
            elif vacancy_info["salary"]["from"] and vacancy_info["salary"]["to"]:
                new_list.append(
                    {'Name vacancy': vacancy_info["name"], 'Salary from': vacancy_info["salary"]["from"],
                     'Salary to': vacancy_info["salary"]["to"], 'Employer id': vacancy_info["employer"]["id"],
                     'URL': vacancy_info["alternate_url"],
                     'City': vacancy_info["area"]["name"], 'Experience': vacancy_info["experience"]["name"]})
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
            cls.list_vacancies.append([(cls(vacancy['Name vacancy'], vacancy['Salary from'], vacancy['Salary to'],
                                            vacancy['Employer id'], vacancy['URL'],
                                            vacancy['City'], vacancy['Experience']))])
        return cls.list_vacancies


class DBManager:

    def __init__(self, params: dict):
        self.params = params

    def create_data_base(self, name_db: str) -> None:
        """
        Create database and tables.
        :param name_db: name of database
        """

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True

        cur = conn.cursor()

        cur.execute(f'DROP DATABASE {name_db}')
        cur.execute(f'CREATE DATABASE {name_db}')

        return "Database created"

    def create_tables(self, name_db: str) -> None:
        """
        Create table for database.
        :param name_db: name of database
        """

        with psycopg2.connect(dbname=name_db, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE info_vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                name_vacancy VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                employer_id INTEGER,
                url TEXT,
                city VARCHAR(100),
                experience TEXT
            )
            """)
                cur.execute("""
                CREATE TABLE info_employers (
                employer_id INTEGER,
                company_name VARCHAR(255),
                description text,
                vacancies_url TEXT,
                CONSTRAINT pk_info_employers_employer_id PRIMARY KEY (employer_id)
                )
            """)
        conn.close()
        return "Tables created"

    def save_data_to_database(self, vacancies_file: list[dict[str: Any]], company_data: list[dict[str: Any]],
                              name_bd: str) -> None:
        """
        Save data info about vacancies.
        :param vacancies_file: info about vacancies for save
        :param company_data: info about employers for save
        :param name_bd: name of database
        """

        conn = psycopg2.connect(dbname=name_bd, **self.params)
        conn.autocommit = True
        with conn.cursor() as cur:
            for data in vacancies_file:
                count_columns = '%s ' * len(data)
                val = tuple(data.values())
                cur.execute(f"INSERT INTO info_vacancies (name_vacancy, salary_from, salary_to,"
                            f"employer_id, url, city, experience) "
                            f"VALUES({', '.join(count_columns.split())})", val)

            for data in company_data:
                count_columns = '%s ' * len(data)
                val = tuple(data.values())
                cur.execute(f"INSERT INTO info_employers (employer_id, company_name, description,"
                            f"vacancies_url)"
                            f"VALUES({', '.join(count_columns.split())})", val)
        conn.commit()
        conn.close()
        return f"Info about vacancies save in database: {name_bd} in tables."


response = GetApiHh()
# Get vacancies for user and info about employer
response.get_vacancy_from_api('оператор')
vacancies_list = response.all_vacancy

# Get clean vacancies list
clean_vacancies_list = Vacancy.sorted_vacancy_list(vacancies_list)

# Get employers id
employers_id = []

for info in clean_vacancies_list:
    employers_id.append(info.get('Employer id'))

# Get info about employers
employers_info = []
for id_employer in set(employers_id):
    employer_info = response.get_info_about_employer(id_employer)
    employers_info.append({'Employer id': employer_info['id'], 'Employer name': employer_info['name'],
                           'Employer description': employer_info['alternate_url'],
                           'Employer vacancies': employer_info['vacancies_url']})

# Create database
params = config()
database = DBManager(params)

print(database.create_data_base('vacancies'))

# Create tables
print(database.create_tables('vacancies'))

# Save info about vacancies and employers in database
print(database.save_data_to_database(clean_vacancies_list, employers_info, 'vacancies'))
