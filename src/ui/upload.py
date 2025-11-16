# src/ui/upload.py
import os
import streamlit as st
import pandas as pd
from src.nlp.ner_re import extract_triples_from_text, extract_triples_from_file, save_triples_to_csv

def upload_page():
    st.markdown("## 📥 Upload / Extract Knowledge Data")
    st.info("Provide text or upload a CSV/XLSX file. The system will extract (subject-relation-object) triples.")

    col1, col2 = st.columns(2)

    # ---- TEXT INPUT SECTION ----
    with col1:
        st.subheader("✏️ Enter Text Manually")
        text_input = st.text_area("Enter or paste text below:", height=200,
                                  placeholder="Example: Albert Einstein was born in Ulm.")
        if st.button("Extract from Text"):
            if not text_input.strip():
                st.warning("Please enter some text first.")
            else:
                triples = extract_triples_from_text(text_input)
                if triples:
                    out = save_triples_to_csv(triples)
                    st.success(f"Extracted {len(triples)} triples → saved to {out}")
                    st.dataframe(pd.DataFrame(triples, columns=["Subject", "Relation", "Object", "Confidence"]))
                else:
                    st.error("No triples detected. Try different text.")

    # ---- FILE UPLOAD SECTION ----
    with col2:
        st.subheader("📄 Upload CSV or Excel File")
        uploaded = st.file_uploader("Choose a dataset file", type=["csv", "xls", "xlsx"])
        if uploaded:
            tmp_path = os.path.join("data", uploaded.name)
            os.makedirs("data", exist_ok=True)
            with open(tmp_path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"File '{uploaded.name}' uploaded.")
            if st.button("Extract from File"):
                try:
                    triples = extract_triples_from_file(tmp_path)
                    if triples:
                        out = save_triples_to_csv(triples)
                        st.success(f"Extracted {len(triples)} triples → saved to {out}")
                        st.dataframe(pd.DataFrame(triples, columns=["Subject", "Relation", "Object", "Confidence"]))
                    else:
                        st.warning("No triples detected in file.")
                except Exception as e:
                    st.error(f"Extraction failed: {e}")

    st.markdown("---")
    if os.path.exists("data/triples.csv"):
        st.download_button(
            "📤 Download Extracted Triples CSV",
            data=open("data/triples.csv", "rb").read(),
            file_name="triples.csv",
            mime="text/csv"
        )
