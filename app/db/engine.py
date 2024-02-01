from sqlmodel import Field, SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
from .models.api_action import USSDAPIAction
from .models.form import USSDForm
from .models.option import USSDOption
from .models.state import USSDState
from .models.ussd_app import USSDApp
from .models.field import USSDField
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db() -> Session:
    with Session(engine) as db:
        yield db
    # db = SessionLocal()
    

if __name__ == "__main__":
    create_db_and_tables()