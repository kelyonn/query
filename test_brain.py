"""Test script for the SQL query chain."""

from backend.db_chain import get_chain
from backend.data_processor import clean_sql_query
from backend.logger import get_logger
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

logger = get_logger(__name__)


def manual_check() -> None:
    """Test the SQL query chain with a sample question."""
    logger.info("Initializing SQL query chain...")
    
    try:
        chain, db = get_chain()
        
        question = "What are the top 3 most sold tracks?"
        logger.info(f"Question: {question}")
        
        logger.info("Generating SQL query...")
        generated_sql = chain.invoke({"question": question})
        sql_query = clean_sql_query(generated_sql)
        logger.info(f"Generated SQL:\n{sql_query}")
        
        logger.info("Executing SQL query...")
        execute_tool = QuerySQLDataBaseTool(db=db)
        result = execute_tool.invoke(sql_query)
        
        logger.info(f"Result:\n{result}")
        logger.info("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)


if __name__ == "__main__":
    manual_check()
