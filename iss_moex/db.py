import atexit

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


PG_DSN = "postgresql://user:1234@127.0.0.1:5432/moex_shares_db"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

