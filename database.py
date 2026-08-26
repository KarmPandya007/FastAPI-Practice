import os
import urllib.parse
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi_app")

load_dotenv()

RAW_DB_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

def fix_db_url(url_str: str) -> str:
    """
    Safely fixes PostgreSQL connection strings where passwords contain special characters like '@'.
    Example: postgresql://user:pass@123@host:5432/db -> postgresql://user:pass%40123@host:5432/db
    """
    if not url_str:
        return "sqlite:///./users.db"
    
    # Standardize postgres dialect prefix for SQLAlchemy
    if url_str.startswith("postgres://"):
        url_str = url_str.replace("postgres://", "postgresql://", 1)
        
    if url_str.startswith("postgresql://"):
        try:
            # Strip scheme
            scheme_sep = "postgresql://"
            rest = url_str[len(scheme_sep):]
            
            # Find the last '@' which separates credentials from host:port/db
            last_at_idx = rest.rfind("@")
            if last_at_idx != -1:
                user_pass = rest[:last_at_idx]
                host_part = rest[last_at_idx + 1:]
                
                # Split user and pass by first ':'
                if ":" in user_pass:
                    user, raw_pass = user_pass.split(":", 1)
                    # Quote password safely without double encoding existing %
                    encoded_pass = urllib.parse.quote(urllib.parse.unquote(raw_pass))
                    return f"postgresql://{user}:{encoded_pass}@{host_part}"
        except Exception as err:
            logger.warning(f"Failed to auto-fix DB URL formatting: {err}")
            
    return url_str

# Processed DB URI
DATABASE_URL = fix_db_url(RAW_DB_URI)

def get_engine(url: str):
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        return create_engine(url, connect_args=connect_args)
    
    try:
        # Try connecting with standard PostgreSQL engine
        eng = create_engine(url, connect_args={"connect_timeout": 3}, pool_pre_ping=True)
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Successfully connected to PostgreSQL database.")
        return eng
    except Exception as exc:
        logger.warning(f"Could not connect to target PostgreSQL database ({exc}). Falling back to SQLite database for development reliability.")
        fallback_url = "sqlite:///./users.db"
        return create_engine(fallback_url, connect_args={"check_same_thread": False})

engine = get_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """
    FastAPI dependency that provides a transactional database session.
    Automatically handles rollback on error and closes session on completion.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
