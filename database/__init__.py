from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from config import sqlalchemy_database_uri
SQLALCHEMY_DATABASE_URI= 'postgresql://postgres:otanazar2007@localhost:5432/inspo_diplom_project'
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f'ошибка {e}')
        db.rollback()
    finally:
        db.close()