from sqlalchemy import String, Integer, Date, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Share(Base):
    __tablename__ = "shares"

    id: Mapped[int] = mapped_column(primery_key=True)
    secid: Mapped[str] = mapped_column(String())
    shortname: Mapped[str] = mapped_column(String())
    trade_date: Mapped[str] = mapped_column(Date())  # trading date
    num_trades: Mapped[int] = mapped_column(Integer())  # number of trades
    value: Mapped[int] = mapped_column(String)  # trading volume
    open_price: Mapped[float] = mapped_column(Float)
    close_price: Mapped[float] = mapped_column(Float)
    low_price: Mapped[float] = mapped_column(Float)
    max_price: Mapped[float] = mapped_column(Float)
    marcket_price_trade_value: Mapped[float] = mapped_column(Float)

    # def __repr__(self) -> str: