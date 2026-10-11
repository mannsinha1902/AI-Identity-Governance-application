"""Generate reproducible, fictional employees, access and activity data."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from .policies import ROLE_ENTITLEMENTS, ALL_ENTITLEMENTS

def generate(n=500, seed=42):
    if n < 20:
        raise ValueError("n must be at least 20")
    rng = np.random.default_rng(seed)
    roles = list(ROLE_ENTITLEMENTS)
    employees, grants = [], []
    for i in range(n):
        eid = f"EMP{i+1:05d}"
        role = str(rng.choice(roles))
        status = str(rng.choice(["active", "inactive", "terminated"], p=[.85,.09,.06]))
        tenure = int(rng.integers(10, 1800))
        employees.append(dict(employee_id=eid, display_name=f"Demo Employee {i+1}", role=role,
                              department={"Engineer":"Engineering","Finance Analyst":"Finance","Finance Manager":"Finance","HR Specialist":"HR","Sales Associate":"Sales","IT Admin":"IT"}[role],
                              status=status, tenure_days=tenure))
        assigned = set(ROLE_ENTITLEMENTS[role])
        if rng.random() < .27:
            assigned.add(str(rng.choice(ALL_ENTITLEMENTS)))
        if rng.random() < .08:
            assigned.add(str(rng.choice(ALL_ENTITLEMENTS)))
        for ent in sorted(assigned):
            grants.append(dict(employee_id=eid, entitlement=ent,
                               days_since_used=int(rng.integers(0, 365)) if status == "active" else int(rng.integers(90, 500)),
                               days_since_granted=int(rng.integers(1, 800))))
    return pd.DataFrame(employees), pd.DataFrame(grants)

def save_data(directory="data", n=500, seed=42):
    folder = Path(directory); folder.mkdir(parents=True, exist_ok=True)
    employees, grants = generate(n, seed)
    employees.to_csv(folder / "employees.csv", index=False)
    grants.to_csv(folder / "access_grants.csv", index=False)
    return employees, grants

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", default="data")
    args = parser.parse_args()
    e, g = save_data(args.out, args.n, args.seed)
    print(f"Generated {len(e)} synthetic employees and {len(g)} access grants")
