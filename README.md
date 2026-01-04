# Query: Text-to-SQL Business Intelligence Tool

A text-to-SQL Business Intelligence tool built with LangChain and Streamlit that converts natural language questions into SQL queries and displays results with automatic visualizations.

## Features

- Natural language to SQL query conversion using OpenAI GPT-3.5-turbo
- Interactive chat interface built with Streamlit
- Automatic data visualization (bar charts for numeric results)
- PostgreSQL database integration (Chinook sample database)
- Query history and SQL query preview
- Error handling and logging

## Prerequisites

- Python 3.10 or higher
- PostgreSQL database (can be run via Docker Compose)
- OpenAI API key

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Database Configuration (defaults shown)
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=chinook

# Optional: OpenAI Model Configuration (defaults shown)
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0
```

### 3. Set Up Database

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

This will start a PostgreSQL container with the Chinook database. You'll need to import the database schema and data separately.

#### Option B: Using Existing PostgreSQL Server

Ensure your PostgreSQL server is running and create the Chinook database, then import the schema from `chinook.sql`.

### 4. Run the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## Usage

1. Start the application using `streamlit run app.py`
2. Type your question in natural language (e.g., "What are the top 5 selling tracks?")
3. The application will:
   - Generate a SQL query from your question
   - Execute the query against the database
   - Display the results as a table
   - Automatically create a visualization if applicable
   - Show the generated SQL query in an expandable section

## Testing

Run the test script to verify the setup:

```bash
python test_brain.py
```

This will test the SQL query generation and execution with a sample question.

## Project Structure

```
query/
├── app.py                 # Main Streamlit application
├── test_brain.py          # Test script
├── backend/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── constants.py       # Application constants
│   ├── data_processor.py  # Data processing and visualization
│   ├── db_chain.py        # Database connection and LangChain setup
│   └── logger.py          # Logging configuration
├── chinook.sql            # Database schema
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

All configuration is managed through environment variables. See the Setup section for required and optional variables.

The application uses module-level caching for database connections and LangChain chains to improve performance.

## Troubleshooting

### Database Connection Issues

- Ensure PostgreSQL is running and accessible
- Verify database credentials in `.env` file match your PostgreSQL setup
- Check that the database exists and is accessible

### OpenAI API Issues

- Verify your `OPENAI_API_KEY` is set correctly in `.env`
- Check your OpenAI account has sufficient credits
- Ensure you have internet connectivity

### Import Errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.10 or higher

## License

This project uses the Chinook sample database, which is licensed under the MIT License.
