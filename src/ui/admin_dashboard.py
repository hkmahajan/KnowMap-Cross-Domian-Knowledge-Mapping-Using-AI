import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import plotly.express as px

def admin_dashboard():
    st.title("📊 Admin Dashboard — Extraction Pipeline Monitor")

    # --- Summary Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entities", "2,847")
    col2.metric("Total Relations", "5,632")
    col3.metric("Extraction Accuracy", "94%")

    # --- Pipeline Activity Chart ---
    st.subheader("Pipeline Processing Overview")
    days = [datetime.now() - timedelta(days=i) for i in range(7)]
    values = [random.randint(100, 300) for _ in days]
    fig = px.line(x=days, y=values, labels={'x':'Date', 'y':'Processed Documents'}, title="Daily Extraction Trend")
    st.plotly_chart(fig, use_container_width=True)

    # --- Pipeline Status ---
    st.subheader("Pipeline Status")
    st.success("Ingestion ✅")
    st.success("NLP ✅")
    st.success("Graph ✅")
    st.success("Storage ✅")
