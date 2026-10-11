import pandas as pd
from src.risk_scoring import assess

def test_terminated_identity_with_grant_is_high_risk():
    employees=pd.DataFrame([dict(employee_id="X",display_name="Test",role="Engineer",department="Engineering",status="terminated",tenure_days=20)])
    grants=pd.DataFrame([dict(employee_id="X",entitlement="github_read",days_since_used=200,days_since_granted=300)])
    risk=assess(employees,grants).iloc[0]
    assert risk.risk_level=="High"
    assert "terminated_with_access" in risk.risk_flags

def test_clean_identity_low_risk():
    employees=pd.DataFrame([dict(employee_id="X",display_name="Test",role="Engineer",department="Engineering",status="active",tenure_days=20)])
    grants=pd.DataFrame([dict(employee_id="X",entitlement="github_read",days_since_used=2,days_since_granted=10)])
    assert assess(employees,grants).iloc[0].risk_score==0
