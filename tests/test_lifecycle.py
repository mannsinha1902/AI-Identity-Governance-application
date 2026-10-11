from src.database import connect, initialize, load
from src.generate_data import generate
from src.lifecycle_management import onboard, change_role, offboard

def test_lifecycle(tmp_path):
    employees,grants=generate(20)
    with connect(tmp_path/"test.db") as conn:
        initialize(conn,employees,grants)
        onboard(conn,"NEW","Test User","Engineer","Engineering")
        assert conn.execute("SELECT COUNT(*) FROM access_grants WHERE employee_id='NEW'").fetchone()[0]==3
        change_role(conn,"NEW","HR Specialist")
        ents={r[0] for r in conn.execute("SELECT entitlement FROM access_grants WHERE employee_id='NEW'")}
        assert ents=={"hr_read","hr_edit"}
        offboard(conn,"NEW")
        assert conn.execute("SELECT COUNT(*) FROM access_grants WHERE employee_id='NEW'").fetchone()[0]==0
        assert conn.execute("SELECT status FROM employees WHERE employee_id='NEW'").fetchone()[0]=="terminated"
        assert conn.execute("SELECT COUNT(*) FROM audit_events WHERE employee_id='NEW'").fetchone()[0]==3
