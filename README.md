# Finance Api Project

## Get Started with Flask App
You have to be at the `finance-api/` repository level
```bash
python3 -m flask --app finance run --port 8000 --debug
```

## Stage 1: Expense API
- Add New Expense
- Read Expense
- Update Expense
- Delete Expense


# 📘 SQLite CLI Cheat Sheet

Use the `sqlite3` command-line interface to explore and interact with SQLite database.

## 🏁 Starting the CLI
```bash
    sqlite3 path/to/your/database.db
```

## Before Running your Queries.
Set these options for better formatting
```sql
    .headers on
    .mode column
    .nullvalue NULL
```

## Common SQL Queries
```sql
-- View first 10 rows of a table
SELECT * FROM table_name LIMIT 10;

-- Count total rows in a table
SELECT COUNT(*) FROM table_name;

-- Show table schema (columns and types)
PRAGMA table_info(table_name);

-- List all tables (alternative method)
SELECT name FROM sqlite_master WHERE type='table';

-- View CREATE TABLE statement
SELECT sql FROM sqlite_master WHERE type='table' AND name='your_table';
```

## General Commands
| Command               | Description                                 |
|-----------------------|---------------------------------------------|
| `.help`               | Show all available dot commands.            |
| `.exit` or `.quit`    | Exit the SQLite CLI.                        |
| `.tables`             | List all tables in the database.            |
| `.schema`             | Show schema for all tables.                 |
| `.schema table_name`  | Show schema of a specific table.            |
| `.databases`          | List attached databases and their file paths. |
| `.headers on`         | Show column headers in query results.       |
| `.mode column`        | Format query results in aligned columns.    |
| `.mode markdown`      | Output results in Markdown table format.    |
| `.nullvalue NULL`     | Show "NULL" for null values instead of blank. |
