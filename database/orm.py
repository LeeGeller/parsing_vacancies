from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


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
