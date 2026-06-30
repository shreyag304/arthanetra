from sqlmodel import Field, Session, SQLModel, create_engine
from contextlib import contextmanager , asynccontextmanager

DATABASE_URL = "postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL, turn off in prod


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session