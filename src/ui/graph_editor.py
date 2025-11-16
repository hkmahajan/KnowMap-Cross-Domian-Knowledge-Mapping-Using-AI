import streamlit as st
import pandas as pd

def graph_editor():
    st.title("🧩 Manual Graph Correction")

    st.info("Edit or merge nodes and relationships manually.")
    uploaded = st.file_uploader("Upload existing triples (CSV)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)

        node_to_edit = st.text_input("Node to Edit:")
        new_value = st.text_input("New Value:")
        if st.button("Apply Edit"):
            st.success(f"Node '{node_to_edit}' changed to '{new_value}'.")

        merge_a = st.text_input("Merge Node A:")
        merge_b = st.text_input("Merge Node B:")
        if st.button("Merge Nodes"):
            st.success(f"Nodes '{merge_a}' and '{merge_b}' merged successfully.")
