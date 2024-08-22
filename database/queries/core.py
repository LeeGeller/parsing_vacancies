from src.database import engine, Base, session_factory
from database.orm import VacanciesORM


def create_table() -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data(vacancies_list: list[dict]) -> None:
    with session_factory() as session:
        for vacancy_info in vacancies_list:
            session.add(VacanciesORM(**vacancy_info))
        session.commit()
