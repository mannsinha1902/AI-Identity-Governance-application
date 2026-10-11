"""Run the complete reproducible demonstration pipeline."""
import argparse
import json
from pathlib import Path
import joblib
from .generate_data import save_data
from .database import connect, initialize
from .risk_scoring import assess
from .access_recommendations import build_features, train, recommend

def run(n=500, seed=42, db="identity_governance.db", out="outputs"):
    folder=Path(out); folder.mkdir(parents=True,exist_ok=True)
    employees, grants = save_data(n=n,seed=seed)
    with connect(db) as conn:
        initialize(conn,employees,grants)
    risks=assess(employees,grants)
    features=build_features(employees,grants)
    model, metrics=train(features,seed)
    recommendations=recommend(model,features)
    risks.to_csv(folder/"identity_risks.csv",index=False)
    recommendations.to_csv(folder/"access_recommendations.csv",index=False)
    (folder/"model_metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
    Path("models").mkdir(exist_ok=True)
    joblib.dump(model,"models/access_review_model.joblib")
    print(f"Employees: {len(employees)} | Grants: {len(grants)} | High-risk: {(risks.risk_level=='High').sum()}")
    print(f"Synthetic-label ROC AUC: {metrics['roc_auc']:.3f}")
    return metrics

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--n",type=int,default=500)
    parser.add_argument("--seed",type=int,default=42)
    args=parser.parse_args()
    run(args.n,args.seed)
