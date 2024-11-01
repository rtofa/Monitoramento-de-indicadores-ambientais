from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:root@localhost/ar_saude"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)