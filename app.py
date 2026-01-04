"""Streamlit application for text-to-SQL Business Intelligence."""

from typing import Dict, Any, List

import streamlit as st
import pandas as pd

from backend.db_chain import get_chain
from backend.data_processor import clean_sql_query, process_query_results
from backend.logger import get_logger
from backend.config import Config

logger = get_logger(__name__)

st.set_page_config(page_title="Query", layout="wide")

st.title("Query")

with st.sidebar:
    st.header("Settings")
    st.write(f"Connected to: **{Config.POSTGRES_DB} Database**")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me about your data."
        }
    ]


def render_message(message: Dict[str, Any]) -> None:
    """Render a chat message with optional data and chart.
    
    Args:
        message: Message dictionary with role, content, and optionally data/chart.
    """
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if "data" in message:
            st.dataframe(message["data"])
        
        if "chart" in message:
            st.plotly_chart(message["chart"])


for message in st.session_state.messages:
    render_message(message)


def process_query(prompt: str) -> Dict[str, Any]:
    """Process a user query and return response data.
    
    Args:
        prompt: User's natural language query.
        
    Returns:
        Dictionary containing message payload with role, content, data, chart, and sql.
        
    Raises:
        ValueError: If configuration is invalid.
        ConnectionError: If database connection fails.
        Exception: For other errors during query processing.
    """
    try:
        chain, db = get_chain()
        
        logger.info(f"Processing query: {prompt}")
        generated_sql = chain.invoke({"question": prompt})
        sql_query = clean_sql_query(generated_sql)
        logger.debug(f"Generated SQL: {sql_query}")
        
        result_str = db.run(sql_query)
        logger.debug(f"Query executed successfully, result length: {len(result_str)}")
        
        response_content, df, visualization = process_query_results(result_str)
        
        message_payload: Dict[str, Any] = {
            "role": "assistant",
            "content": response_content,
            "sql": sql_query
        }
        
        if df is not None:
            message_payload["data"] = df
        
        if visualization is not None:
            message_payload["chart"] = visualization
        
        return message_payload
    
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except ConnectionError as e:
        logger.error(f"Database connection error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing query: {e}", exc_info=True)
        raise


if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            try:
                message_payload = process_query(prompt)
                
                st.markdown(message_payload["content"])
                
                if "data" in message_payload:
                    st.dataframe(message_payload["data"])
                
                if "chart" in message_payload:
                    st.plotly_chart(message_payload["chart"])
                
                if "sql" in message_payload:
                    with st.expander("See SQL Query"):
                        st.code(message_payload["sql"], language="sql")
                
                display_payload = {k: v for k, v in message_payload.items() if k != "sql"}
                st.session_state.messages.append(display_payload)
            
            except ValueError as e:
                error_msg = f"Configuration Error: {str(e)}"
                st.error(error_msg)
                logger.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            
            except ConnectionError as e:
                error_msg = f"Database Connection Error: {str(e)}"
                st.error(error_msg)
                logger.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
            
            except Exception as e:
                error_msg = f"Error processing query: {str(e)}"
                st.error(error_msg)
                logger.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
