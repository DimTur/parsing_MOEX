from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Share(Base):
    __tablename__ = "shares"

    id: Mapped[int] = mapped_column(primery_key=True)
    secid: Mapped[str] = mapped_column(String())  # share indicate
    shortname: Mapped[str] = mapped_column(String())  # share short name
    date_time: Mapped[str] = mapped_column(DateTime())  # current date and time await self.userdb.update_user(request, vk_id, {'time_to_go': datetime.datetime.now()}
    valtoday: Mapped[str] = mapped_column(Float())  # current volume in rub
    open: Mapped[float] = mapped_column(Float)  # share's open price


    # num_trades: Mapped[int] = mapped_column(Integer())  # number of trades
    # value: Mapped[int] = mapped_column(String)  # trading volume
    # close_price: Mapped[float] = mapped_column(Float)
    # low_price: Mapped[float] = mapped_column(Float)
    # max_price: Mapped[float] = mapped_column(Float)
    # marcket_price_trade_value: Mapped[float] = mapped_column(Float)

    # def __repr__(self) -> str: