"""Interactive IAM portfolio demonstration; synthetic data only."""
import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st
from src.database import connect, load, audit
from src.generate_data import save_data
from src.database import initialize
from src.risk_scoring import assess
from src.access_recommendations import build_features, train, recommend
from src.lifecycle_management import onboard, change_role, offboard
from src.policies import ROLE_ENTITLEMENTS

st.set_page_config(page_title="Identity Governance Lab",page_icon="🛡️",layout="wide")
st.title("🛡️ AI-Assisted Identity Governance & Risk Analytics")
st.caption("Synthetic demo only · Policy findings are deterministic · ML suggestions require human review")
DB=Path("identity_governance.db")
if not DB.exists():
    e,g=save_data()
    with connect(DB) as c: initialize(c,e,g)

with st.sidebar:
    st.header("Demo controls")
    if st.button("Reset synthetic database"):
        e,g=save_data()
        with connect(DB) as c: initialize(c,e,g)
        st.rerun()
    st.caption("Reset discards local lifecycle changes and audit history.")

with connect(DB) as c:
    employees, grants=load(c)
risks=assess(employees,grants)
features=build_features(employees,grants)
model,metrics=train(features)
reviews=recommend(model,features)

t1,t2,t3,t4=st.tabs(["Risk overview","Access certifications","Lifecycle simulator","Audit log"])
with t1:
    a,b,c,d=st.columns(4)
    a.metric("Identities",len(employees))
    b.metric("Access grants",len(grants))
    c.metric("High-risk identities",int((risks.risk_level=="High").sum()))
    d.metric("Pending suggested reviews",int((reviews.recommendation=="REVIEW FOR REVOCATION").sum()))
    x,y=st.columns(2)
    with x:
        st.plotly_chart(px.histogram(risks,x="risk_level",category_orders={"risk_level":["Low","Medium","High"]},title="Risk distribution"),use_container_width=True)
    with y:
        st.plotly_chart(px.histogram(risks,x="department",color="risk_level",title="Risk by department"),use_container_width=True)
    st.subheader("Identity findings")
    st.dataframe(risks.sort_values("risk_score",ascending=False),use_container_width=True,hide_index=True)
with t2:
    st.write("Machine learning predicts synthetic heuristic labels. Scores are **not** validated real-world revocation probabilities.")
    st.metric("Held-out synthetic-label ROC AUC",f"{metrics['roc_auc']:.3f}")
    selected=st.selectbox("Review recommendation",["All","REVIEW FOR REVOCATION","RETAIN / MONITOR"])
    filtered=reviews if selected=="All" else reviews[reviews.recommendation==selected]
    st.dataframe(filtered[["employee_id","entitlement","role","status","days_since_used","revoke_score","recommendation","reason"]].sort_values("revoke_score",ascending=False),use_container_width=True,hide_index=True)
    st.info("Recommendations are advisory. No revocation occurs from this tab.")
with t3:
    st.subheader("Joiner · Mover · Leaver simulator")
    action=st.radio("Action",["Onboard","Change role","Offboard"],horizontal=True)
    if action=="Onboard":
        with st.form("onboard"):
            eid=st.text_input("New employee ID",value="DEMO99999")
            name=st.text_input("Display name",value="Demo New Hire")
            role=st.selectbox("Role",list(ROLE_ENTITLEMENTS))
            dept=st.text_input("Department",value="Demo")
            submit=st.form_submit_button("Create identity and role access")
        if submit:
            try:
                with connect(DB) as conn: onboard(conn,eid,name,role,dept)
                st.success("Identity created. Reload to see updated risk findings.")
            except (ValueError,sqlite3.IntegrityError) as exc: st.error(str(exc))
    else:
        eid=st.selectbox("Employee ID",employees.employee_id.tolist())
        if action=="Change role":
            role=st.selectbox("New role",list(ROLE_ENTITLEMENTS))
            if st.button("Apply role change"):
                try:
                    with connect(DB) as conn: change_role(conn,eid,role)
                    st.success("Role changed; old grants replaced with role baseline.")
                except ValueError as exc: st.error(str(exc))
        elif st.button("Offboard and revoke all grants"):
            with connect(DB) as conn: offboard(conn,eid)
            st.success("Employee terminated and all grants removed.")
    if st.button("Refresh dashboard"):
        st.rerun()
with t4:
    with connect(DB) as conn:
        events=pd.read_sql_query("SELECT * FROM audit_events ORDER BY event_id DESC LIMIT 500",conn)
    st.dataframe(events,use_container_width=True,hide_index=True)
    st.caption("Local append-only event records for demo purposes; not tamper-proof enterprise audit logging.")
