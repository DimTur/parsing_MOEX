from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Share(Base):
    __tablename__ = "shares"

    id: Mapped[int] = mapped_column(primery_key=True)
    secid: Mapped[str] = mapped_column(String())  # share indicate
    last: Mapped[float] = mapped_column(Float)  # share's last price
    systime: Mapped[str] = mapped_column(DateTime())  # current date and time await self.userdb.update_user(request, vk_id, {'time_to_go': datetime.datetime.now()}
    valtoday: Mapped[str] = mapped_column(Float())  # current volume in rub

    def __repr__(self) -> str:
        return f"Share(" \
               f"id={self.id!r}, " \
               f"secid={self.secid!r}, " \
               f"last={self.last!r}, " \
               f"date_time={self.date_time!r}" \
               f"valtoday={self.valtoday!r}" \
               f")"
