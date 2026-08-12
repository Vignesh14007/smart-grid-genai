# ⚡ Smart Grid GenAI — Natural Language Query Assistant

> A conversational GenAI system that allows users to query smart-grid monitoring data using natural language instead of writing SQL manually.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue.svg)](https://www.postgresql.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black.svg)](https://ollama.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

---

## 🎯 Why This Project?

Smart-grid monitoring systems continuously generate structured data containing voltage, current, power, energy consumption, feeders, transformers, and timestamps.

Traditionally, extracting insights from this data requires users to know SQL.

This project solves that problem by introducing a **natural-language interface over PostgreSQL**.

A user can simply ask:

> **"Which transformer has the highest average power?"**

The system understands the question, generates the appropriate SQL query using a local LLM, validates the query, executes it against PostgreSQL, and converts the result into a human-readable answer.

### Core Pipeline

```text
Natural Language
       ↓
     LLM
       ↓
   SQL Generation
       ↓
   SQL Validation
       ↓
   PostgreSQL
       ↓
   Query Result
       ↓
  AI Answer Generation
       ↓
 Human-readable Response
✨ Key Features
🗣️ Natural Language Database Querying
🤖 Local LLM-powered Text-to-SQL
🐘 PostgreSQL Smart-Grid Database
🔒 SQL Validation and Read-only Query Control
💬 Conversational Follow-up Questions
🧠 Context-aware queries
⚡ Smart-grid specific analytics
🖥️ Interactive Streamlit interface
🔐 Local LLM execution without sending database data to an external AI API
🧠 How It Works
1. User asks a question

Example:

Which feeder has the highest power?
2. LLM generates SQL

The local Llama 3 model converts the question into SQL:

SELECT feeder_id, power
FROM power_measurements
ORDER BY power DESC
LIMIT 1;
3. SQL validation

Before execution, the generated query passes through a validation layer.

The application allows read-only SELECT queries and blocks database modification operations such as:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
GRANT
REVOKE
4. PostgreSQL execution

The validated query is executed against the smart_grid PostgreSQL database.

5. Result generation

The database result is passed to the answer-generation layer and converted into a concise natural-language response.

6. Conversational context

The system can use previous conversation context for follow-up questions.

Example:

User:
Which feeder has the highest power?

AI:
The feeder with the highest power is F_01.

User:
What is its voltage?

AI:
The latest voltage measurement for F_01 is ...

This allows the user to interact with the database conversationally rather than treating every query as an isolated request.

🏗️ Architecture
┌─────────────────────────────┐
│            User             │
│   Natural Language Query    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Streamlit UI          │
│          app.py             │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Local LLM             │
│      Ollama + Llama 3       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Text-to-SQL           │
│        llm_sql.py           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       SQL Validator         │
│    sql_validator.py         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        PostgreSQL           │
│        smart_grid           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Query Engine          │
│      query_engine.py        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Answer Generator        │
│    answer_generator.py      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Natural Language        │
│          Answer             │
└─────────────────────────────┘
🛠️ Technology Stack
Layer	Technology
Language	Python
LLM Runtime	Ollama
LLM	Llama 3 8B
Database	PostgreSQL
Database Driver	Psycopg2
Frontend	Streamlit
Query Language	SQL
Version Control	Git
Repository	GitHub
📊 Smart-Grid Data Model

The system currently works with a PostgreSQL table:

power_measurements
Schema
Column	Description
id	Unique measurement identifier
timestamp	Measurement time
transformer_id	Transformer identifier
feeder_id	Feeder identifier
voltage	Voltage measurement
current	Current measurement
power	Power measurement
energy_consumption	Energy consumption

The current development dataset contains 80 measurement records.

💬 Example Queries

The system supports questions such as:

Power Analysis
Which feeder has the highest power?
Which feeder has the lowest power?
What is the average power of each feeder?
Transformer Analysis
Which transformer has the highest average power?
What is the average power of transformer TR_01?
Voltage & Current
Which measurement has the highest voltage?
What is the latest voltage of feeder F_01?
What is the latest current of feeder F_01?
Energy Analysis
Which feeder has the highest energy consumption?
Database Queries
How many power measurements are in the database?
🔒 AI-Generated SQL Safety

LLMs can generate incorrect or unsafe SQL.

Instead of directly executing model output, this project introduces a validation layer between the LLM and PostgreSQL.

LLM
 │
 ▼
Generated SQL
 │
 ▼
Validation
 │
 ├── Unsafe → Reject
 │
 └── Valid SELECT → Execute

This provides an additional control boundary before AI-generated queries reach the database.

📁 Project Structure
smart-grid-genai/
│
├── app.py
├── llm_sql.py
├── query_engine.py
├── db_test.py
│
├── src/
│   ├── __init__.py
│   ├── sql_validator.py
│   └── answer_generator.py
│
├── data/
│   ├── raw/
│   └── processed/
│       └── power_grid_clean.csv
│
├── requirements.txt
├── README.md
└── .gitignore
⚙️ Setup
Prerequisites

Make sure the following are installed:

Python 3.x
PostgreSQL
Ollama
Git
1. Clone the repository
git clone https://github.com/Vignesh14007/smart-grid-genai.git
cd smart-grid-genai
2. Create a virtual environment
python3 -m venv venv

Activate it:

source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure PostgreSQL

Create the database:

CREATE DATABASE smart_grid;

Create the power_measurements table using the schema described above and load the processed dataset.

Verify the data:

SELECT COUNT(*) FROM power_measurements;
5. Configure Ollama

Check available models:

ollama list

The project uses:

llama3:8b

If it is not installed:

ollama pull llama3:8b

Test it:

ollama run llama3:8b
6. Configure database credentials

Use environment variables for local credentials.

Example:

DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=smart_grid
DB_USER=smartgrid_user
DB_PASSWORD=your_password

Do not commit credentials or .env files to GitHub.

▶️ Run the Application

Activate the virtual environment:

source venv/bin/activate

Start the Streamlit application:

streamlit run app.py

Then open:

http://localhost:8501
🧪 Database Connection Test

Run:

python db_test.py

The application should successfully connect to PostgreSQL and report the available records.

🧩 Core Modules
app.py

Main Streamlit application.

Handles:

User interaction
Conversation history
Query workflow
Result presentation
llm_sql.py

Handles natural-language-to-SQL generation using Ollama and Llama 3.

query_engine.py

Handles PostgreSQL connectivity and SQL execution.

src/sql_validator.py

Cleans and validates LLM-generated SQL before database execution.

src/answer_generator.py

Converts database results into natural-language responses.

db_test.py

Verifies PostgreSQL connectivity and data availability.

🎯 What Makes This Project Different?

This project is not simply a chatbot.

It combines:

Generative AI
      +
Natural Language Processing
      +
Text-to-SQL
      +
Database Engineering
      +
SQL Safety
      +
Conversational Context
      +
Smart-Grid Analytics

The important engineering challenge is the connection between an LLM and a structured database.

The system must ensure that:

The user's intent is understood.
Correct SQL is generated.
Generated SQL is validated.
Only permitted queries reach the database.
Database results are correctly interpreted.
Follow-up questions retain context.
🚀 Future Improvements

The current system provides the foundation for a larger smart-grid intelligence platform.

Potential extensions include:

Real-time power monitoring
Time-series visualization
Feeder comparison dashboards
Transformer health analysis
Power anomaly detection
Fault detection
Automated alerts
Historical trend analysis
More robust Text-to-SQL evaluation
Role-based database access
Production deployment
🎓 Skills Demonstrated

This project demonstrates practical experience in:

Generative AI
Large Language Models
Prompt Engineering
Natural Language Processing
Text-to-SQL
Python
PostgreSQL
SQL
Database Connectivity
AI Output Validation
Conversational AI
Streamlit
Local LLM Deployment
Git & GitHub
👨‍💻 Author
Vigneshwaran

B.Tech Information Technology
Kongu Engineering College

Interested in:

AI/ML • Generative AI • Data Science • Data Analytics

⭐ Project Summary

Smart Grid GenAI demonstrates how a local Large Language Model can be connected to a structured PostgreSQL smart-grid database to create a conversational data-access layer.

Instead of asking users to learn SQL first, the system allows them to ask questions naturally and converts those questions into validated database queries.

Natural Language → SQL → Validation → Database → AI Answer

Built as an academic project with a focus on Generative AI, database interaction, and practical AI engineering.

### One important thing

Don't put your actual PostgreSQL password anywhere in this README or GitHub repository. Keep credentials in `.env` and put `.env` in `.gitignore`.

After pasting the README:

```bash
nano README.md


