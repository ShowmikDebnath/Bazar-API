from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL
db_url = "postgresql://showmik@localhost:5432/bazar"

# Engine - the actual connection to the postgresql
engine = create_engine(db_url)

# SessionLocal - Used to talk to the database
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

# Base - parent class for all your models
Base = declarative_base()

# Dependency - gives a db session to each API request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


