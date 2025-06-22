# QueryMind - Natural Language Database Query Assistant

![QueryMind](https://img.shields.io/badge/QueryMind-Database%20Assistant-39ffa2)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Alpha-red)

<div align="center">
  <img src="https://github.com/user-attachments/assets/f0b1d48a-e48c-4d3b-a42c-3c4375ff2636" alt="QueryMind Banner" width="800"/>
  <p><em>Talk to your database using natural language</em></p>
</div>


## 🔮 Overview

**QueryMind** is an advanced database query assistant that lets you interact with SQLite databases using natural language. Powered by state-of-the-art language models, QueryMind translates your questions into precise SQL queries, making database exploration accessible to everyone—regardless of SQL expertise.

The system's core component, **SQLMancer**, is an LLM-powered agent that intelligently explores database schema and constructs optimized SQL queries based on your natural language requests.

> **Intelligence that speaks your language to extract insights — Talk to your database using natural language.**

## ✨ Key Features

- **Natural Language Interface** - Query your database using everyday language
- **Intelligent Schema Exploration** - The agent automatically explores and understands your database structure
- **Optimized Query Generation** - Produces efficient SQL queries tailored to your specific needs
- **Interactive Conversation** - Engage in a dialogue with the agent to refine your queries
- **Multiple LLM Options** - Support for both local models (via Ollama) and cloud-based models (via Groq)
- **Streamlit Web Interface** - User-friendly web application with database visualization
- **Command Line Interface** - For users who prefer terminal-based interaction

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- SQLite database(s) you want to query
- API key for Groq (if using cloud-based models)

### Running the Web Interface

Start the Streamlit web application:

```bash
streamlit run app.py
```

Then:
1. Upload your SQLite database using the file uploader
2. Explore available tables in the sidebar
3. Start querying your database using natural language!

### Using the Command Line Interface

For CLI usage:

```bash
python main.py /path/to/your/database.sqlite
```

Then simply enter your queries at the prompt.

## 🧩 Architecture

QueryMind is built with a modular architecture designed for flexibility and extensibility:

### Core Components

- **Agent Module** (`agent.py`): Implements the LLM-powered SQL agent that handles conversation flow and tool calls
- **Tools Module** (`tools.py`): Provides database interaction capabilities including schema exploration and query execution
- **Models Module** (`models.py`): Handles LLM provider integration with support for both Ollama and Groq
- **Config Module** (`config.py`): Manages application settings, model configurations, and path handling
- **Logging Module** (`logging.py`): Provides enhanced console logging with rich formatting
- **App Module** (`app.py`): Implements the Streamlit web interface
- **CLI Module** (`main.py`): Provides command-line interface functionality

### Data Flow

1. User inputs a natural language query
2. The agent processes the query using the LLM
3. The agent explores the database schema using database tools
4. A SQL query is constructed and executed
5. Results are formatted and presented to the user

## 🔎 Example Usage

### Basic Query

```
User: "Show me all customers who placed orders in the last month"

QueryMind: I'll help you find customers with recent orders. Let me explore your database structure first.

[QueryMind explores tables and relationships]

Here are the customers who placed orders in the last month:

| CustomerID | Name         | Email               | OrderCount |
|------------|--------------|---------------------|------------|
| C001       | John Smith   | john@example.com    | 3          |
| C007       | Emma Johnson | emma@example.com    | 1          |
| C012       | David Lee    | david@example.com   | 5          |

This query identified 3 customers who placed a total of 9 orders in the past month.
```

### Complex Analysis

```
User: "What are the top 5 products by revenue and what percentage of total revenue do they represent?"

QueryMind: I'll analyze your product revenue data. First, let me understand your database structure.

[QueryMind explores tables and relationships]

Here are the top 5 products by revenue with their contribution to total revenue:

| ProductID | ProductName    | Revenue  | Percentage |
|-----------|---------------|----------|------------|
| P103      | Premium Widget | $156,230 | 27.8%      |
| P245      | Ultra Gadget   | $98,700  | 17.6%      |
| P118      | Mega Tool      | $76,350  | 13.6%      |
| P422      | Super Device   | $52,800  | 9.4%       |
| P007      | Expert System  | $45,600  | 8.1%       |

These top 5 products represent 76.5% of your total revenue ($561,500).
```

## 🌟 Advanced Features

### Multiple Model Support

QueryMind supports various language models through two providers:

#### Ollama (Local Models)
- Qwen 2.5
- Gemma 3 (12B)
- DeepSeek (7B)
- SQLCoder

#### Groq (Cloud Models)
- LLaMA 3.3 (70B)
- Gemma 2 (9B)


### Database Exploration Tools

The system includes specialized tools for database interaction:

- **Table Listing**: Discover all available tables in your database
- **Schema Inspection**: Examine table structures, columns, and constraints
- **Data Sampling**: View sample data to understand content patterns
- **SQL Execution**: Run custom SQL queries with results formatting

## 🛠️ Technical Details

### System Requirements

- **Python**: 3.9 or higher
- **Memory**: 8GB+ (16GB+ recommended for larger databases)
- **Storage**: SSD recommended for better performance
- **GPU**: Optional but beneficial for local model inference

### Dependencies

- **LangChain**: Framework for LLM application development
- **Streamlit**: Web application framework
- **Rich**: Terminal formatting and styling
- **SQLite3**: Database engine
- **Groq/Ollama**: Model providers

## 📚 API Documentation

### Agent Module

```python
ask(query: str, history: List[BaseMessage], llm: BaseChatModel, max_iterations: int = 10) -> str
```
Processes a user's natural language query through the LLM agent to generate a response.

### Tools Module

Available database tools:
- `list_tables(reasoning: str) -> str`
- `sample_table(reasoning: str, table_name: str, row_sample_size: int) -> str`
- `describe_table(reasoning: str, table_name: str) -> str`
- `execute_sql(reasoning: str, sql_query: str) -> str`

### User Interface

![image](https://github.com/user-attachments/assets/6d1db7e3-fc6f-442f-8ba9-1daf56ed1833)
![image](https://github.com/user-attachments/assets/34a1ac23-892a-4e52-978f-6eebb0ad9f95)
![image](https://github.com/user-attachments/assets/571ef334-ae50-4fdd-b9d2-b3e5bb91126b)
![image](https://github.com/user-attachments/assets/4f0c6b26-61ec-426d-add3-b270fa427138)
![image](https://github.com/user-attachments/assets/5104fdda-9425-4ce1-8a89-14a501d30869)
![image](https://github.com/user-attachments/assets/e956e29e-6cfc-4675-8cb4-48f673d513f6)
![image](https://github.com/user-attachments/assets/0f66bca5-61b6-4237-8275-5c26387fcb05)
![image](https://github.com/user-attachments/assets/3e111cf7-2b0c-4a57-8b8f-90a7b08f9980)
![image](https://github.com/user-attachments/assets/42a7ed0e-3e52-4279-a0a4-a988d9e8828e)
![image](https://github.com/user-attachments/assets/37a63b79-6584-4a28-8328-20938c481ad3)
![image](https://github.com/user-attachments/assets/6842fa96-8eb2-4cb9-87a6-83ef41354742)
![image](https://github.com/user-attachments/assets/94937dec-73cf-4d21-9137-bbfc1a0f0fd2)
![image](https://github.com/user-attachments/assets/150e8ebb-9dc2-4201-8d2d-6f94ec152a32)







## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [LangChain](https://github.com/hwchase17/langchain) for providing the core LLM framework
- [Streamlit](https://github.com/streamlit/streamlit) for the web application framework
- [Groq](https://groq.com) for providing fast LLM inference
- [Ollama](https://ollama.ai) for local model support

---

<div align="center">
  <p>Developed with ❤️ by Ashwin Devan</p>
  <p>
    <a href="https://github.com/ashwindevan">GitHub</a> •
    <a href="https://twitter.com/yourusername">Twitter</a> •
    <a href="ashwindevan9@gmail.com">Contact</a>
  </p>
</div>
