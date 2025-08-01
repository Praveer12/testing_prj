from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine


DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/e_comm"
engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine,autoflush=False)

Base = declarative_base()

def db_run():
    db = sessionLocal()
    try:
        yield db

    finally:
        db.close()

