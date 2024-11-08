import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.sqlalchemy_base import Base


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    telegram_user_id: Mapped[str] = mapped_column(unique=True, index=True)
    dttm_created: Mapped[datetime.datetime]
    full_name: Mapped[str]
    birthdate: Mapped[datetime.date]
    registration_address: Mapped[str]
    residential_address: Mapped[str]
    passport_number: Mapped[str] = mapped_column(String(10))
    passport_given_by: Mapped[str]
    passport_given_date: Mapped[datetime.date]
    snils: Mapped[str] = mapped_column(String(11))
    phone: Mapped[str]
    email: Mapped[str]
