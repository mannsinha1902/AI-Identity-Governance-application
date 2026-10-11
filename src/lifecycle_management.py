"""Simulated joiner/mover/leaver operations with audit logging."""
from .policies import ROLE_ENTITLEMENTS
from .database import audit

def onboard(conn, employee_id, display_name, role, department):
    if role not in ROLE_ENTITLEMENTS:
        raise ValueError("Unknown role")
    with conn:
        conn.execute("INSERT INTO employees VALUES (?,?,?,?,?,?)",
                     (employee_id, display_name, role, department, "active", 0))
        for ent in ROLE_ENTITLEMENTS[role]:
            conn.execute("INSERT INTO access_grants VALUES (?,?,?,?)", (employee_id,ent,0,0))
    audit(conn,employee_id,"ONBOARD",f"role={role}")

def change_role(conn, employee_id, new_role):
    if new_role not in ROLE_ENTITLEMENTS:
        raise ValueError("Unknown role")
    row = conn.execute("SELECT status FROM employees WHERE employee_id=?",(employee_id,)).fetchone()
    if not row or row[0] != "active":
        raise ValueError("Employee must exist and be active")
    with conn:
        conn.execute("UPDATE employees SET role=? WHERE employee_id=?",(new_role,employee_id))
        conn.execute("DELETE FROM access_grants WHERE employee_id=?",(employee_id,))
        for ent in ROLE_ENTITLEMENTS[new_role]:
            conn.execute("INSERT INTO access_grants VALUES (?,?,?,?)",(employee_id,ent,0,0))
    audit(conn,employee_id,"ROLE_CHANGE",f"new_role={new_role}")

def offboard(conn, employee_id):
    with conn:
        cur=conn.execute("UPDATE employees SET status='terminated' WHERE employee_id=?",(employee_id,))
        if cur.rowcount != 1:
            raise ValueError("Employee not found")
        conn.execute("DELETE FROM access_grants WHERE employee_id=?",(employee_id,))
    audit(conn,employee_id,"OFFBOARD","All access revoked")
