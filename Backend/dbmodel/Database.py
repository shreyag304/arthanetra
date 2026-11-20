import os
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

DEFAULT_DATABASE_URL = "postgresql://chaiaurcode:chaiaurcode@localhost:5434/chaiDB"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def _init_engine():
    global DATABASE_URL
    try:
        connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {"connect_timeout": 3}
        test_engine = create_engine(DATABASE_URL, connect_args=connect_args)
        with test_engine.connect():
            pass
        return test_engine
    except Exception as e:
        fallback_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "arthanetra.db"))
        fallback_url = f"sqlite:///{fallback_path}"
        print(f"[ArthaNetra Database] Note: Could not connect to {DATABASE_URL} ({e}).")
        print(f"[ArthaNetra Database] Falling back to SQLite: {fallback_url}")
        DATABASE_URL = fallback_url
        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


engine = _init_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    # Safe SQLite auto-migrations for newly added columns
    try:
        from sqlalchemy import text
        with engine.begin() as conn:
            # Check existing columns on user_financial_profile
            result = conn.execute(text("PRAGMA table_info(user_financial_profile);")).fetchall()
            existing_cols = {row[1] for row in result}
            new_columns = [
                ("last_route", "VARCHAR"),
                ("last_topic", "VARCHAR"),
                ("last_scam_risk", "FLOAT"),
                ("last_user_query", "TEXT"),
            ]
            for col_name, col_type in new_columns:
                if col_name not in existing_cols:
                    conn.execute(text(f"ALTER TABLE user_financial_profile ADD COLUMN {col_name} {col_type};"))
    except Exception as mig_err:
        print(f"[Database] Schema auto-migration notice: {mig_err}")


def get_db():
    with Session(engine) as session:
        yield session
