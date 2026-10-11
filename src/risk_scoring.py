"""Explainable rule-based risk engine. Scores are illustrative, not calibrated probabilities."""
import pandas as pd
from .policies import SOD_CONFLICTS, PRIVILEGED
from .rbac_engine import allowed

def assess(employees, grants):
    lookup = {eid: grp.to_dict("records") for eid, grp in grants.groupby("employee_id")}
    rows = []
    for emp in employees.to_dict("records"):
        items = lookup.get(emp["employee_id"], [])
        names = {x["entitlement"] for x in items}
        flags = []
        if emp["status"] == "terminated" and items:
            flags.append("terminated_with_access")
        if emp["status"] == "inactive" and items:
            flags.append("inactive_with_access")
        if any(not allowed(emp["role"], name) for name in names):
            flags.append("excess_entitlement")
        if any(a in names and b in names for a,b in SOD_CONFLICTS):
            flags.append("sod_conflict")
        if any(x["days_since_used"] > 90 for x in items):
            flags.append("dormant_access")
        if names & PRIVILEGED:
            flags.append("privileged_access")
        weights = {"terminated_with_access":45,"inactive_with_access":20,
                   "excess_entitlement":25,"sod_conflict":40,
                   "dormant_access":15,"privileged_access":10}
        score = min(100, sum(weights[x] for x in flags))
        rows.append({**emp, "grant_count":len(items), "risk_score":score,
                     "risk_level":"High" if score>=60 else "Medium" if score>=30 else "Low",
                     "risk_flags":", ".join(flags) or "none"})
    return pd.DataFrame(rows)
