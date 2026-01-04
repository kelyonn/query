"""Data processing and visualization utilities."""

import re
import ast
from typing import Any, List, Tuple, Optional

import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure

from backend.constants import DEFAULT_COLUMN_NAMES, CHART_TITLE, DEFAULT_RESPONSE_MESSAGE
from backend.logger import get_logger

logger = get_logger(__name__)


def clean_sql_query(sql_query: str) -> str:
    """Extract SQL query from markdown code blocks or plain text.
    
    Args:
        sql_query: SQL query string that may contain markdown formatting.
        
    Returns:
        Cleaned SQL query string.
    """
    sql_query = re.sub(r"```sql\s*", "", sql_query)
    sql_query = re.sub(r"```\s*", "", sql_query)
    
    return sql_query.strip()


def parse_query_result(result_str: str) -> List[Any]:
    """Parse SQL query result string into a Python list.
    
    Args:
        result_str: String representation of query results.
        
    Returns:
        List of query results (list of tuples or empty list on error).
    """
    try:
        data_list = ast.literal_eval(result_str)
        if isinstance(data_list, list):
            return data_list
        logger.warning(f"Query result is not a list: {type(data_list)}")
        return []
    except (ValueError, SyntaxError) as e:
        logger.warning(f"Failed to parse query result: {e}")
        return []


def create_dataframe(query_results: List[Any]) -> pd.DataFrame:
    """Create a pandas DataFrame from query results.
    
    Args:
        query_results: List of tuples/rows from SQL query.
        
    Returns:
        DataFrame with query results.
    """
    if not query_results:
        return pd.DataFrame()
    
    df = pd.DataFrame(query_results)
    
    if len(df.columns) == 2:
        df.columns = DEFAULT_COLUMN_NAMES
    
    return df


def create_visualization(df: pd.DataFrame) -> Optional[Figure]:
    """Create a bar chart visualization from a DataFrame.
    
    Args:
        df: DataFrame with query results (expected 2 columns).
        
    Returns:
        Plotly figure if visualization is possible, None otherwise.
    """
    if len(df.columns) != 2:
        return None
    
    try:
        value_column = df.columns[1]
        df = df.copy()
        df[value_column] = pd.to_numeric(df[value_column], errors="coerce")
        
        if df[value_column].isna().all():
            logger.debug("Value column is not numeric, skipping visualization")
            return None
        
        category_column = df.columns[0]
        fig = px.bar(
            df,
            x=category_column,
            y=value_column,
            title=CHART_TITLE,
            color=value_column
        )
        
        logger.debug("Visualization created successfully")
        return fig
    
    except (ValueError, KeyError, TypeError) as e:
        logger.warning(f"Failed to create visualization: {e}")
        return None


def process_query_results(result_str: str) -> Tuple[str, Optional[pd.DataFrame], Optional[Figure]]:
    """Process SQL query results into formatted data and visualization.
    
    Args:
        result_str: Raw string result from SQL query execution.
        
    Returns:
        Tuple of (response message, DataFrame if data available, Figure if visualization available).
    """
    query_results = parse_query_result(result_str)
    
    if not query_results:
        return result_str, None, None
    
    df = create_dataframe(query_results)
    
    if df.empty:
        return result_str, None, None
    
    visualization = create_visualization(df)
    
    return DEFAULT_RESPONSE_MESSAGE, df, visualization

