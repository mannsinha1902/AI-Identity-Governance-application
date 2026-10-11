CREATE TABLE IF NOT EXISTS employees (
 employee_id TEXT PRIMARY KEY, display_name TEXT NOT NULL, role TEXT NOT NULL,
 department TEXT NOT NULL, status TEXT NOT NULL CHECK(status IN ('active','inactive','terminated')),
 tenure_days INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS access_grants (
 employee_id TEXT NOT NULL REFERENCES employees(employee_id), entitlement TEXT NOT NULL,
 days_since_used INTEGER NOT NULL, days_since_granted INTEGER NOT NULL,
 PRIMARY KEY(employee_id, entitlement)
);
CREATE TABLE IF NOT EXISTS audit_events (
 event_id INTEGER PRIMARY KEY AUTOINCREMENT, employee_id TEXT NOT NULL,
 action TEXT NOT NULL, detail TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
