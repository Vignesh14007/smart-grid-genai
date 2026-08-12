# ⚡ Smart Grid GenAI

### Natural Language → SQL → Smart Grid Insights

An AI-powered Natural Language Query system that allows users to interact with smart-grid monitoring data using simple questions instead of writing SQL queries manually.

---

## 🚀 What is this?

Smart-grid systems generate large amounts of data such as:

- ⚡ Power
- 🔌 Voltage
- 📊 Current
- 🔋 Energy consumption
- 🏭 Transformers
- 🔗 Feeders
- 🕒 Timestamped measurements

Normally, users need SQL knowledge to analyze this data.

**Smart Grid GenAI solves this by providing a conversational interface powered by a local Large Language Model (LLM).**

### Example

**User asks:**

> Which transformer has the highest average power?

**AI generates:**

```sql
SELECT transformer_id,
       AVG(power) AS average_power
FROM power_measurements
GROUP BY transformer_id
ORDER BY average_power DESC
LIMIT 1;

System responds:

The transformer with the highest average power is TR_01.

✨ Key Features
🤖 Natural Language to SQL
🧠 Local LLM using Ollama + Llama 3
🐘 PostgreSQL database integration
🔒 SQL validation before execution
💬 Conversational follow-up questions
📊 Smart-grid data analysis
🖥️ Interactive Streamlit interface
🔐 Local AI processing
🏗️ Architecture
        👤 User
          │
          ▼
   Natural Language
          │
          ▼
   🤖 Llama 3 / Ollama
          │
          ▼
     SQL Generation
          │
          ▼
     🔒 SQL Validator
          │
          ▼
     🐘 PostgreSQL
          │
          ▼
     Query Results
          │
          ▼
    🧠 AI Answer
          │
          ▼
    💬 User Response
🛠️ Tech Stack
Technology	Purpose
🐍 Python	Application development
🤖 Ollama	Local LLM runtime
🧠 Llama 3 8B	Text-to-SQL & answer generation
🐘 PostgreSQL	Database
🔗 Psycopg2	Database connectivity
🖥️ Streamlit	Web interface
🗃️ SQL	Data querying
🔧 Git & GitHub	Version control
📊 Database
Database
smart_grid
Main Table
power_measurements
Columns
Column	Description
id	Measurement ID
timestamp	Measurement time
transformer_id	Transformer identifier
feeder_id	Feeder identifier
voltage	Voltage measurement
current	Current measurement
power	Power measurement
energy_consumption	Energy consumption

Current development dataset:

80 power measurement records

💬 Example Questions

The system can understand questions such as:

Which feeder has the highest power?
Which transformer has the highest average power?
What is the average power of each feeder?
Which feeder has the highest energy consumption?
What is the latest voltage of feeder F_01?
How many power measurements are available?
🔒 SQL Safety

AI-generated SQL is not directly executed.

The system first validates the generated query.

LLM
 ↓
Generated SQL
 ↓
SQL Validation
 ↓
Safe SELECT Query
 ↓
PostgreSQL

Read-only queries are allowed, while operations such as:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE

are blocked.

This provides an additional safety layer between the LLM and the database.

📁 Project Structure
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
⚙️ Setup
1. Clone
git clone https://github.com/Vignesh14007/smart-grid-genai.git
cd smart-grid-genai
2. Create virtual environment
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Start Ollama
ollama run llama3:8b
5. Start the application
streamlit run app.py

Open:

http://localhost:8501
🎯 Project Highlights
GenAI

Uses a local LLM to translate natural-language questions into SQL.

Database Integration

Connects the LLM workflow with a PostgreSQL smart-grid database.

AI Safety

Validates generated SQL before allowing database execution.

Conversational Interaction

Supports natural follow-up questions instead of requiring users to write independent SQL queries.

Local AI

Uses Ollama for local LLM inference, reducing dependency on external AI APIs.

🚀 Future Improvements
📈 Real-time power monitoring
📊 Interactive analytics dashboards
🚨 Power anomaly detection
🔔 Automated alerts
⚡ Feeder and transformer health analysis
📅 Historical trend analysis
🌐 Cloud deployment
📱 Responsive monitoring interface
👨‍💻 Author
Vigneshwaran

B.Tech Information Technology
Kongu Engineering College

Interests:
AI/ML • Generative AI • Data Science • Data Analytics

⭐ Core Idea
Natural Language
       ↓
      LLM
       ↓
      SQL
       ↓
   Validation
       ↓
  PostgreSQL
       ↓
   AI Answer

Making smart-grid data accessible through natural language.
