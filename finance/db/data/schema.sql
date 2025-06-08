-- Create Expense Table
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    vendor TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);
-- Create Income Table
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    source TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    date TEXT NOT NULL
);
-- Create Category (Expense & Income) Table
-- Create Transfer Table (Coming Later)
-- Create Accounts Table (Coming Later)