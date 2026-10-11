"""ML assisted access review demo; never executes revocations automatically.

Synthetic labels are generated from a heuristic. This model learns to imitate
that heuristic and is NOT evidence of real-world predictive validity.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from .policies import PRIVILEGED
from .rbac_engine import allowed

def build_features(employees, grants):
    joined = grants.merge(employees[["employee_id","role","status","tenure_days"]], on="employee_id", validate="many_to_one")
    joined["excess"] = [int(not allowed(role, ent)) for role,ent in zip(joined.role,joined.entitlement)]
    joined["privileged"] = joined.entitlement.isin(PRIVILEGED).astype(int)
    joined["not_active"] = (joined.status != "active").astype(int)
    joined["dormant"] = (joined.days_since_used > 90).astype(int)
    joined["suggest_revoke"] = ((joined.excess == 1) | (joined.not_active == 1) | ((joined.dormant == 1) & (joined.privileged == 1))).astype(int)
    return joined

FEATURES = ["days_since_used", "days_since_granted", "tenure_days", "excess", "privileged", "not_active", "dormant"]

def train(features, seed=42):
    # Split by employee to prevent a person's grants appearing in both partitions.
    unique_ids = features.employee_id.unique()
    train_ids, test_ids = train_test_split(unique_ids,test_size=.25,random_state=seed)
    tr = features[features.employee_id.isin(train_ids)]
    te = features[features.employee_id.isin(test_ids)]
    if tr.suggest_revoke.nunique()<2 or te.suggest_revoke.nunique()<2:
        raise ValueError("Need both target classes in train and test data")
    model = RandomForestClassifier(n_estimators=120, max_depth=6, random_state=seed, class_weight="balanced")
    model.fit(tr[FEATURES], tr.suggest_revoke)
    predictions = model.predict(te[FEATURES])
    probabilities = model.predict_proba(te[FEATURES])[:,1]
    metrics = {"roc_auc":round(float(roc_auc_score(te.suggest_revoke, probabilities)),4),
               "classification_report":classification_report(te.suggest_revoke,predictions,output_dict=True,zero_division=0),
               "train_grants":len(tr),"test_grants":len(te)}
    return model, metrics

def recommend(model, features):
    output = features.copy()
    output["revoke_score"] = model.predict_proba(output[FEATURES])[:,1]
    output["recommendation"] = np.where(output.revoke_score >= .5,"REVIEW FOR REVOCATION","RETAIN / MONITOR")
    output["reason"] = np.select([output.not_active.eq(1),output.excess.eq(1),
                                    output.dormant.eq(1)&output.privileged.eq(1)],
                                   ["Identity inactive/terminated","Outside role baseline","Dormant privileged access"],
                                   default="No synthetic heuristic violation")
    return output
