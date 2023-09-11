from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    port="localhost",
    host="5432",
    database="iss_moex",
)

engine = create_async_engine(url)
Session = sessionmaker(bind=engine)
