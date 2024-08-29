
from sqlalchemy import select, desc
from sqlalchemy.orm import Mapped, mapped_column
from database.engine import engine, Base, session_factory



class VacanciesORM(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_vacancy: Mapped[str]
    company: Mapped[str | None]
    location: Mapped[str | None]
    description: Mapped[str | None]
    url: Mapped[str | None]
    experience: Mapped[str | None]
    salary_from: Mapped[int]
    salary_to: Mapped[int]


    @staticmethod
    def create_table() -> None:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def insert_data(vacancies_list: list[dict]) -> None:
        vacancies_set = set(tuple(vacancy.items() for vacancy in vacancies_list))
        with session_factory() as session:
            for vacancy_tuple in vacancies_set:
                session.add(VacanciesORM(**dict(vacancy_tuple)))
            session.commit()

    @staticmethod
    def select_data() -> list[dict]:
        with session_factory() as session:

            query = select(VacanciesORM)

            result = session.execute(query)
            vacancies = result.scalars().all()

        return [vacancy.__dict__ for vacancy in vacancies]

    @staticmethod
    def get_top_vacancies_without_experience(limit: int = 20) -> list[dict]:
        with session_factory() as session:
            query = (
                select(VacanciesORM)
                .where(VacanciesORM.experience == 'Нет опыта')
                .order_by(desc(VacanciesORM.salary_to))
                .limit(limit)
            )
            result = session.execute(query)
            vacancies = result.scalars().all()

        return [vacancy.__dict__ for vacancy in vacancies]
