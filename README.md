# AI-Driven Identity Access Governance & Risk Analytics

[![Python tests](https://github.com/mannsinha1902/ai-identity-access-governance/actions/workflows/tests.yml/badge.svg)](https://github.com/mannsinha1902/ai-identity-access-governance/actions/workflows/tests.yml)

An end-to-end **portfolio demonstration** of Identity Governance and Administration (IGA), inspired by enterprise IAM workflows. Built with **Python, SQLite, pandas, scikit-learn, Streamlit and Plotly**.

> **Synthetic data only.** This is an independent educational simulation, **not** a SailPoint integration, an EY client implementation, or a production-ready identity security platform. ML predictions imitate synthetic heuristic decisions and must not be interpreted as validated operational recommendations.

## Business questions
- Which identities hold risky or excessive permissions?
- Where do role-based access (RBAC) and separation-of-duties (SoD) violations occur?
- Which dormant privileged grants deserve human review?
- How can joiner/mover/leaver changes be documented and tested?

## Features
- Reproducible synthetic identities and entitlements, generated with a fixed seed
- SQLite persistence, SQL reporting queries, and demo audit event log
- Deterministic policy checks: least privilege, inactive/terminated access, dormancy, SoD conflicts, privileged entitlements
- Explainable 0–100 illustrative risk score and Low/Medium/High bands
- Random forest access-review **suggestions** with employee-level holdout split
- Streamlit dashboard with risk charts, access certification queue, and lifecycle simulator
- pytest coverage and GitHub Actions CI

## Quick start (Python 3.10+)

Run commands from the project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m src.pipeline
streamlit run app.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` and retry. On macOS/Linux, activate with `source .venv/bin/activate`.

The dashboard opens at `http://localhost:8501` by default. Press **Reset synthetic database** in the sidebar to restore the starting dataset. The CLI pipeline writes `data/*.csv`, `outputs/*.csv`, `outputs/model_metrics.json`, `models/*.joblib`, and `identity_governance.db`. The local database, model, and outputs are ignored by Git.

## Architecture

```text
Synthetic generator → SQLite + SQL → Policy / RBAC / SoD risk engine
                                     ↘ ML recommendation model (synthetic labels)
                                      ↘ Streamlit dashboard + lifecycle demo + audit events
```

## Model evaluation and limitations

The target `suggest_revoke` is **constructed from synthetic policy heuristics**, not historical human access-review outcomes. Therefore, a high ROC AUC means the model learned the generated heuristic; it does **not** demonstrate real-world access decision quality. The split is by employee ID to reduce leakage across multiple grants. All revocation suggestions require a human reviewer; no ML-driven access changes are executed. The risk score is illustrative and not a probability of compromise.

## Data dictionary

**employees.csv**: `employee_id`, `display_name` (fictional), `role`, `department`, `status`, `tenure_days`.

**access_grants.csv**: `employee_id`, `entitlement`, `days_since_used`, `days_since_granted`.

## SQL

- `sql/schema.sql`: normalized SQLite tables and constraints
- `sql/risk_queries.sql`: dormant access, terminated identity access, departmental grant counts

To query locally: `sqlite3 identity_governance.db` then `.read sql/risk_queries.sql` (if SQLite CLI is installed), or use a SQLite extension in VS Code.

## Test and reproduce

```powershell
python -m pytest -q
python -m src.generate_data --n 500 --seed 42
python -m src.pipeline --n 500 --seed 42
```

## Publish

See [docs/publish_to_github.md](docs/publish_to_github.md) for exact Windows / VS Code commands for `mannsinha1902/ai-identity-access-governance`.

## Portfolio talking points

- Simulated least-privilege and SoD policy controls across fictional employee identities
- Implemented joiner/mover/leaver workflows with audit records
- Built explainable rule-based risk scoring and ML-assisted certification triage
- Delivered a reproducible interactive dashboard with CI tests

## Responsible use

Do not add confidential company data or production credentials. The app is local-only, has no authentication or authorization layer, and should not be exposed publicly as an administrative service. The event log is not tamper-resistant.
