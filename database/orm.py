from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class VacanciesORM(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name_vacancy: Mapped[str]
    company: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    url: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    salary_from: Mapped[int] = mapped_column(nullable=True)
    salary_to: Mapped[int] = mapped_column(nullable=True)
