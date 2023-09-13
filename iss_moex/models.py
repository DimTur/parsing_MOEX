from sqlalchemy import String, Float, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from db import engine


class Base(DeclarativeBase):
    pass


class Share(Base):
    __tablename__ = "shares"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    secid: Mapped[str] = mapped_column(String())  # share indicate
    last: Mapped[float] = mapped_column(Float(), nullable=True)  # share's last price
    valtoday: Mapped[float] = mapped_column(Float(), nullable=True)  # current volume in rub
    systime: Mapped[str] = mapped_column(String())  # current date and time (maybe rewrite to "date_time")

    def __repr__(self) -> str:
        return f"Share(" \
               f"id={self.id!r}, " \
               f"secid={self.secid!r}, " \
               f"last={self.last!r}, " \
               f"date_time={self.systime!r}" \
               f"valtoday={self.valtoday!r}" \
               f")"


Base.metadata.create_all(engine)
