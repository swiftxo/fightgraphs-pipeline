from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fightgraphs_pipeline.models.postgresql_models import get_postgres_base
from contextlib import contextmanager
from sqlalchemy.engine import Engine

# Assuming Base is imported from your models file.
# from fightgraphs_pipeline.models.postgresql_models import Base
Base = get_postgres_base()


class PostgresController:
	"""
	Controller for managing PostgreSQL database connections and sessions.
	"""
	def __init__(self, db_uri: str, db_name: str, echo: bool = False):
		"""
		Initializes the PostgresController with a database connection.

		Args:
			db_uri (str): The PostgreSQL connection URI (e.g., "postgresql://user:pass@host:port").
			db_name (str): The name of the database.
			echo (bool): If True, the engine will log all statements.
		"""
		full_uri = f"{db_uri}/{db_name}"
		self._engine: Engine = create_engine(full_uri, echo=echo)
		self._session_local = sessionmaker(
			autocommit=False, autoflush=False, bind=self._engine
		)

	def init_db(self) -> None:
		"""
		Creates all database tables defined in the Base metadata.
		This should be called once when the application starts.
		"""
		Base.metadata.create_all(bind=self._engine)
		print("Database initialized.")

	@contextmanager
	def get_db_session(self) -> Session:
		"""
		Provides a transactional database session using a context manager.
		It automatically handles commit, rollback, and closing.

		Yields:
			Session: The SQLAlchemy session object.
		"""
		session: Session = self._session_local()
		try:
			yield session
			session.commit()
		except Exception:
			session.rollback()
			raise
		finally:
			session.close()

	def close_db(self) -> None:
		"""
		Closes the database engine connection.
		This should be called when the application is shutting down.
		"""
		self._engine.dispose()
		print("Database connection closed.")


