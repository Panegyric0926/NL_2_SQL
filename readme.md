# Natural Language to SQL Converter

This project provides an end-to-end pipeline that converts user input in natural language into executable SQL queries. It leverages state-of-the-art embedding models for understanding user intent and interacts with databases via structured, secure code.

---

## Project Aim

The primary goal of this project is to bridge the gap between human language and database queries. Users can input questions or requests in everyday language, and the system will interpret, validate, and convert these into SQL commands for execution against a target database.

---

## Workflow

The core process is illustrated in the flowchart below (also available as [flow chart.html](flow%20chart.html) and [flow chart.jpeg](flow%20chart.jpeg)):

![Flow Chart](flow%20chart.jpeg)

1. **Convert Natural Language to Structured Language:**  
   The user’s query is analyzed and transformed into a structured format suitable for further processing.

2. **Is Query Relevant?**  
   The system checks if the query is relevant to the supported database schema and logic.
   - **No:** The process stops.
   - **Yes:** Continue to the next step.

3. **Use Structured Language to Query Database:**  
   The system attempts to match the structured query against existing data and known results.

4. **Is There a Match in Database?**  
   - **Yes:** The answer is returned from the database.
   - **No:** The system continues to the next steps.

5. **Convert Structured Language into Real SQL Code:**  
   The structured language is translated into valid SQL syntax.

6. **Check for Errors in SQL Code:**  
   The generated SQL is checked for errors and potential issues.

7. **Update Database with New Result:**  
   If appropriate, the database is updated or the query result is stored.

---

## Project Structure

| File / Folder         | Description                                            |
|-----------------------|--------------------------------------------------------|
| `main.py`             | Main entry point (non-UI version)                     |
| `ui.py`               | Main entry point for the UI version                    |
| `call_database.py`    | Handles calls to the database service                  |
| `database_app.py`     | Hosts the database service                             |
| `db.json`             | The raw database file                                  |
| `call_embedding.py`   | Handles calls to the embedding service                 |
| `embedding_app.py`    | Hosts the embedding service                            |
| `call_llm.py`         | Handles calls to the language model service            |
| `prompt.py`           | Stores and manages prompts for LLMs                    |
| `flow chart.html`     | Source HTML for the flowchart diagram                  |
| `flow chart.jpeg`     | JPEG version of the flowchart diagram                  |
| `command.txt`         | Stores commands to start the services                  |

---

## Embedding Model

This project uses the [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3) embedding model from Hugging Face.

---

## Getting Started

1. Start the embedding and database services (see `command.txt` for instructions).
2. Run either `main.py` for the CLI version or `ui.py` for the UI version.

---