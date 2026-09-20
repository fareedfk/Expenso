import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from apps.api.core.config import MYSQL_URL, MYSQL_ROOT_URL, SQLITE_URL, DB_NAME

logger = logging.getLogger("expenso.database")

Base = declarative_base()
engine = None
SessionLocal = None

def init_database():
    """Initialize database connection (MySQL with auto-create schema, or SQLite fallback)."""
    global engine, SessionLocal
    try:
        root_engine = create_engine(MYSQL_ROOT_URL, pool_pre_ping=True)
        with root_engine.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        root_engine.dispose()

        engine = create_engine(
            MYSQL_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=10,
            max_overflow=20
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Connected to MySQL '{DB_NAME}' successfully.")
    except Exception as e:
        logger.warning(f"MySQL unavailable ({e}). Falling back to SQLite.")
        engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

# Initialize on module load
init_database()

def get_db():
    """FastAPI Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
