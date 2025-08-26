import os, streamlit as st
from career_agent.config import load_config
from career_agent.agent import run_pipeline
from career_agent.database import ensure_db, read_jobs, set_label
from career_agent.feedback import train_model_from_feedback

st.set_page_config(page_title="Career Agent", layout="wide")
st.title("Career Agent — Job Scanner & Recommender")

cfg = load_config("agent_config.json")
eng = ensure_db(cfg.db_path)

st.sidebar.header("Run Scan")
excel_file = st.sidebar.text_input("Excel path", value="Career sites.xlsx")
out_dir = st.sidebar.text_input("Output folder", value="out_jobs")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Scan Now"):
        if not os.path.exists(excel_file):
            st.error("Excel not found")
        else:
            with st.spinner("Scanning..."):
                df = run_pipeline(excel_file, out_dir, cfg, model_path=(cfg.model_path if os.path.exists(cfg.model_path) else None))
            st.success(f"Done. Rows: {len(df)}")

with col2:
    if st.button("Train model"):
        hist = read_jobs(eng, limit=100000)
        path = train_model_from_feedback(hist, os.path.join(out_dir, cfg.feedback_csv), cfg.model_path)
        st.success("Model trained" if path else "Need feedback first")

st.header("Results")
df = read_jobs(eng, limit=1000)
if df.empty:
    st.info("No jobs yet. Run a scan.")
else:
    st.dataframe(df, use_container_width=True, height=520)
    st.subheader("Give feedback")
    sel = st.selectbox("Select job URL", options=[""] + df["url"].tolist())
    a,b,c = st.columns(3)
    with a:
        if st.button("👍 Relevant") and sel:
            set_label(eng, sel, "pos"); st.success("Marked relevant")
    with b:
        if st.button("👎 Not relevant") and sel:
            set_label(eng, sel, "neg"); st.success("Marked not relevant")
    with c:
        if st.button("Clear label") and sel:
            set_label(eng, sel, None); st.success("Cleared")
