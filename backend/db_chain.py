"""Database connection and LangChain SQL query chain setup."""

from typing import Tuple, Optional
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain.chains.base import Chain

from backend.config import Config
from backend.logger import get_logger

logger = get_logger(__name__)

_db: Optional[SQLDatabase] = None
_chain: Optional[Chain] = None


def get_db() -> SQLDatabase:
    """Get or create a cached database connection.
    
    Returns:
        SQLDatabase instance connected to the configured database.
        
    Raises:
        ValueError: If database URI is invalid.
        ConnectionError: If database connection fails.
    """
    global _db
    
    if _db is None:
        try:
            Config.validate()
            db_uri = Config.get_database_uri()
            logger.info(f"Connecting to database: {Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}")
            _db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=0)
            logger.info("Database connection established successfully")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise ConnectionError(f"Database connection failed: {e}") from e
    
    return _db


def get_chain() -> Tuple[Chain, SQLDatabase]:
    """Get or create a cached SQL query chain and database connection.
    
    Returns:
        Tuple of (SQL query chain, database connection).
        
    Raises:
        ValueError: If OPENAI_API_KEY is not configured.
        ConnectionError: If database connection fails.
    """
    global _chain, _db
    
    Config.validate()
    db = get_db()
    
    if _chain is None:
        try:
            logger.info(f"Initializing LangChain with model: {Config.OPENAI_MODEL}")
            llm = ChatOpenAI(
                model=Config.OPENAI_MODEL,
                temperature=Config.OPENAI_TEMPERATURE,
                openai_api_key=Config.OPENAI_API_KEY
            )
            _chain = create_sql_query_chain(llm, db)
            logger.info("SQL query chain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SQL query chain: {e}")
            raise ValueError(f"Failed to initialize SQL query chain: {e}") from e
    
    return _chain, db
