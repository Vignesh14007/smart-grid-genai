# ⚡ Smart Grid GenAI

### Natural Language → SQL → Smart Grid Insights

An AI-powered natural language query system for smart-grid data analysis.

Smart Grid GenAI allows users to ask questions about power-grid measurements in plain English instead of manually writing SQL queries. A local Large Language Model converts the question into SQL, validates the generated query for safety, executes it against PostgreSQL, and converts the result into a human-readable answer.

---

## 🚀 Overview

Smart-grid monitoring systems generate large volumes of structured data such as:

- ⚡ Power
- 🔌 Voltage
- 📊 Current
- 🔋 Energy consumption
- 🏭 Transformer measurements
- 🔗 Feeder measurements
- 🕐 Timestamped readings

Traditionally, users need SQL knowledge to analyze this data.

**Smart Grid GenAI bridges the gap between natural language and database analytics.**

### Example

**User asks:**

> Which feeder has the highest power?

**AI generates SQL:**

    SELECT feeder_id,
           MAX(power) AS max_power
    FROM power_measurements
    GROUP BY feeder_id
    ORDER BY max_power DESC
    LIMIT 1;

**System responds:**

> The feeder with the highest power is F_01.

---

## ✨ Key Features

- 🗣️ Natural language database querying
- 🤖 Local LLM-based SQL generation
- 🧠 Llama 3 through Ollama
- 🐘 PostgreSQL database integration
- 🔐 SQL validation before execution
- 🛡️ Read-only database querying
- 💬 Conversational follow-up questions
- 📊 Smart-grid measurement analysis
- 🖥️ Interactive Streamlit interface
- 🔒 Local AI processing without external AI APIs

---

## 🏗️ System Architecture

    User
      │
      ▼
    Natural Language Question
      │
      ▼
    Streamlit Interface
      │
      ▼
    Llama 3 + Ollama
      │
      ▼
    SQL Generation
      │
      ▼
    SQL Validator
      │
      ▼
    Safe SELECT Query
      │
      ▼
    PostgreSQL
      │
      ▼
    Query Result
      │
      ▼
    AI Answer Generator
      │
      ▼
    Human-Readable Response

---

## 🔄 How It Works

The system follows a multi-stage AI-to-database pipeline:

    Natural Language
           ↓
          LLM
           ↓
     SQL Generation
           ↓
      SQL Cleaning
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

### 1. User Query

The user enters a question using natural language.

Example:

    What is the latest voltage of feeder F_01?

### 2. SQL Generation

The local LLM interprets the question and generates the corresponding SQL query.

### 3. SQL Validation

The generated query is cleaned and validated before execution.

Only read-only SELECT queries are allowed.

### 4. Database Execution

The validated query is executed against the PostgreSQL smart-grid database.

### 5. Result Processing

The database result is passed to the answer-generation layer.

### 6. AI Response

The local LLM converts the database result into a concise natural-language response.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Ollama | Local LLM runtime |
| Llama 3 8B | Natural language understanding and SQL generation |
| PostgreSQL | Smart-grid database |
| Psycopg2 | PostgreSQL connectivity |
| Streamlit | Web application interface |
| SQL | Database querying |
| Git & GitHub | Version control |

---

## 🗄️ Database

The project uses a PostgreSQL database containing smart-grid power measurements.

### Main Table

    power_measurements

### Important Columns

| Column | Description |
|---|---|
| id | Measurement ID |
| timestamp | Measurement time |
| transformer_id | Transformer identifier |
| feeder_id | Feeder identifier |
| voltage | Voltage measurement |
| current | Current measurement |
| power | Power measurement |
| energy_consumption | Energy consumption |

---

## 💬 Example Questions

The system can understand questions such as:

    Which feeder has the highest power?

    Which transformer has the highest average power?

    What is the average power of each feeder?

    Which feeder has the highest energy consumption?

    What is the latest voltage of feeder F_01?

    What is the current of feeder F_01?

    How many power measurements are available?

    Which transformer has the highest power?

    What was the latest measurement for F_01?

Users do not need to manually write SQL queries.

---

## 🔐 SQL Safety

AI-generated SQL is **not blindly executed**.

Before execution, the generated query passes through a validation layer.

Only read-only SELECT queries are permitted.

The validator blocks potentially destructive operations such as:

    INSERT
    UPDATE
    DELETE
    DROP
    ALTER
    TRUNCATE
    CREATE

Safety pipeline:

    LLM
      ↓
    Generated SQL
      ↓
    SQL Cleaning
      ↓
    SQL Validation
      ↓
    Safe SELECT Query
      ↓
    PostgreSQL

This provides an additional safety layer between the LLM and the PostgreSQL database.

---

## 📁 Project Structure

    smart-grid-genai/
    │
    ├── app.py
    ├── llm_sql.py
    ├── query_engine.py
    ├── db_test.py
    │
    ├── src/
    │   ├── sql_validator.py
    │   └── answer_generator.py
    │
    ├── data/
    │   └── processed/
    │       └── power_grid_clean.csv
    │
    ├── requirements.txt
    ├── README.md
    └── .gitignore

### Core Components

**app.py**

Streamlit user interface and application workflow.

**llm_sql.py**

Handles natural-language-to-SQL generation using the local LLM.

**query_engine.py**

Handles PostgreSQL connection and SQL execution.

**src/sql_validator.py**

Cleans and validates AI-generated SQL before execution.

**src/answer_generator.py**

Converts database results into natural-language answers.

**db_test.py**

Used to verify PostgreSQL database connectivity.

---

## ⚙️ Installation

### 1. Clone the Repository

    git clone https://github.com/Vignesh14007/smart-grid-genai.git
    cd smart-grid-genai

### 2. Create a Virtual Environment

    python3 -m venv venv

### 3. Activate the Environment

    source venv/bin/activate

### 4. Install Dependencies

    pip install -r requirements.txt

### 5. Start Ollama

Make sure Ollama is installed and running.

Download the required model:

    ollama pull llama3:8b

### 6. Configure PostgreSQL

Configure the PostgreSQL database connection used by the project.

Example:

    Host     : 127.0.0.1
    Port     : 5432
    Database : smart_grid
    User     : smartgrid_user

### 7. Start the Application

    streamlit run app.py

Open the application at:

    http://localhost:8501

---

## 🧪 Testing

### Test Database Connection

    python db_test.py

### Test Answer Generator

    python -c "from src.answer_generator import generate_answer; print('Answer generator working')"

---

## 🎯 Project Objective

The main objective of Smart Grid GenAI is to make structured smart-grid data accessible through natural language.

Instead of requiring users to understand:

    SQL + Database Schema + Query Syntax

the system provides:

    Natural Language
           ↓
          AI
           ↓
        Insights

This approach makes smart-grid data analysis more accessible to users who may not have advanced SQL knowledge.

---

## 💡 What Makes This Project Different?

Unlike a basic chatbot that only generates text, this project connects a **local LLM with a real relational database**.

The AI is part of an actual data-processing pipeline:

    User
      ↓
    Natural Language
      ↓
    Local LLM
      ↓
    SQL Generation
      ↓
    SQL Validation
      ↓
    PostgreSQL
      ↓
    Real Database Data
      ↓
    AI-generated Insight

The project demonstrates practical integration of:

- Generative AI
- Large Language Models
- Natural Language Processing
- SQL
- PostgreSQL
- Database Systems
- Data Analytics
- AI Safety
- Application Development

---

## 🔮 Future Improvements

- 📡 Real-time smart-grid data integration
- 📊 Interactive power analytics dashboards
- 🚨 Power anomaly detection
- 🔔 Automated alerts
- ⚡ Feeder health analysis
- 🏭 Transformer health analysis
- 📈 Historical trend analysis
- 🔮 Power demand forecasting
- 🌐 Cloud deployment
- 📱 Responsive monitoring interface

---

## 📌 Project Status

**Current Status: Functional Prototype**

Current implementation:

    Natural Language Query
            ↓
         Local LLM
            ↓
       SQL Generation
            ↓
       SQL Validation
            ↓
    PostgreSQL Execution
            ↓
      AI-generated Answer

---

## 👨‍💻 Author

**Vigneshwaran**

B.Tech Information Technology  
Kongu Engineering College

**Interests:** AI/ML · Generative AI 

---

## ⭐ Key Takeaway

> **Smart Grid GenAI makes smart-grid data accessible through natural language by combining LLMs, SQL, PostgreSQL, and AI-powered data analysis.**

---

⭐ If you find this project interesting, consider giving the repository a star.
