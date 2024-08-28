from sqlalchemy import select
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
        with session_factory() as session:
            for vacancy_info in vacancies_list:
                session.add(VacanciesORM(**vacancy_info))
            session.commit()

    @staticmethod
    def select_data() -> list[dict]:
        with session_factory() as session:

            query = select(VacanciesORM)

            result = session.execute(query)
            vacancies = result.all()

            return vacancies
