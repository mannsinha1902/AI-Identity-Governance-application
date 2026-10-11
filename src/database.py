"""SQLite persistence and append-only audit events for demo workflows."""
import sqlite3
from pathlib import Path
import pandas as pd

SCHEMA = Path(__file__).resolve().parents[1] / "sql" / "schema.sql"

def connect(path="identity_governance.db"):
    conn = sqlite3.connect(str(path))
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def initialize(conn, employees, grants):
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    conn.execute("DELETE FROM audit_events")
    conn.execute("DELETE FROM access_grants")
    conn.execute("DELETE FROM employees")
    employees.to_sql("employees", conn, if_exists="append", index=False)
    grants.to_sql("access_grants", conn, if_exists="append", index=False)
    conn.commit()

def load(conn):
    return (pd.read_sql_query("SELECT * FROM employees", conn),
            pd.read_sql_query("SELECT * FROM access_grants", conn))

def audit(conn, employee_id, action, detail):
    conn.execute("INSERT INTO audit_events(employee_id, action, detail) VALUES (?, ?, ?)",
                 (employee_id, action, detail))
    conn.commit()
