from celery.bin.result import result
from sqlalchemy import select, desc, and_, or_, func
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
        vacancies_set = set(tuple(vacancy.items()) for vacancy in vacancies_list)
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

    @staticmethod
    def get_vacancies_without_experience_and_salary() -> list[dict]:
        with session_factory() as session:
            query = (
                select(VacanciesORM)
                .where(and_(
                    VacanciesORM.salary_to == 0,
                    VacanciesORM.salary_from == 0,
                    VacanciesORM.experience == 'Нет опыта'))
            )
            result = session.execute(query)
            vacancies = result.scalars().all()
        return [vacancy.__dict__ for vacancy in vacancies]

    @staticmethod
    def get_avg_salary():
        with session_factory() as session:
            query = (
                select(func.avg(VacanciesORM.salary_from).label('avg_salary_from'),
                        func.avg(VacanciesORM.salary_to).label('avg_salary_to'))
                .where(or_(
                    VacanciesORM.salary_to != 0,
                    VacanciesORM.salary_from != 0))

            )
            result = session.execute(query)
            vacancies = result.fetchone()

        return vacancies