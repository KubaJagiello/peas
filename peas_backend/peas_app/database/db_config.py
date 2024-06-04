from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    close_all_sessions,
    declarative_base,
    scoped_session,
    sessionmaker,
)

Base = declarative_base()


class DatabaseConfig:
    def __init__(self, database_url: str | None = None) -> None:
        if database_url is None:
            # Default to an SQLite file-based DB for production
            database_url = "sqlite:///sqlite.db"

        self._engine = create_engine(
            database_url, echo=False, connect_args={"check_same_thread": False}
        )
        self._session_factory = sessionmaker(bind=self._engine)
        self._session = scoped_session(self._session_factory)

    def get_session(self) -> Session:
        return self._session  #  type:  ignore

    def get_session_factory(self) -> sessionmaker:
        return self._session_factory

    def create_all_tables(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_all_tables(self) -> None:
        Base.metadata.drop_all(self._engine)

    def close_session(self) -> None:
        close_all_sessions()
        self._session.remove()
