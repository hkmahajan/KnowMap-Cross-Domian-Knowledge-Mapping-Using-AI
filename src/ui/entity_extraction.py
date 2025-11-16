import os
import streamlit as st
import pandas as pd
from pyvis.network import Network
from src.nlp.ner_re import extract_triples_from_text, extract_triples_from_file

def entity_extraction_page():
    st.title("🧠 Entity & Relation Extraction")
    st.markdown("Extract entities and relations from text or files, then visualize them as a Knowledge Graph.")

    mode = st.radio("Select Input Mode", ["Enter Text", "Upload CSV/Excel", "Use Sample"], horizontal=True)

    triples = []

    # 1️⃣ Manual Text Input
    if mode == "Enter Text":
        text = st.text_area(
            "📝 Paste or Type Text:",
            height=180,
            placeholder="Example: Albert Einstein discovered relativity in 1905."
        )
        if st.button("⚙️ Extract Triples"):
            if text.strip():
                triples = extract_triples_from_text(text)
                if triples:
                    st.success(f"✅ Extracted {len(triples)} triples")
                else:
                    st.warning("No triples found.")
            else:
                st.error("Please enter some text first.")

    # 2️⃣ File Upload (CSV / Excel)
    elif mode == "Upload CSV/Excel":
        uploaded = st.file_uploader("📁 Upload CSV or Excel file", type=["csv", "xls", "xlsx"])
        if uploaded:
            path = os.path.join("data", uploaded.name)
            os.makedirs("data", exist_ok=True)
            with open(path, "wb") as f:
                f.write(uploaded.getbuffer())
            st.success(f"✅ File '{uploaded.name}' uploaded successfully!")

            if st.button("⚙️ Extract Triples from File"):
                try:
                    # Auto-detect file type and load
                    if uploaded.name.endswith(".csv"):
                        df = pd.read_csv(path)
                    else:
                        df = pd.read_excel(path)

                    # Try to find a column with text content
                    text_col = None
                    for col in df.columns:
                        if df[col].dtype == "object":  # possible text column
                            text_col = col
                            break

                    if text_col:
                        st.info(f"Extracting triples from text column: **{text_col}**")
                        all_triples = []
                        for text in df[text_col].dropna().tolist():
                            triples_in_text = extract_triples_from_text(str(text))
                            all_triples.extend(triples_in_text)

                        triples = all_triples
                        if triples:
                            st.success(f"✅ Extracted {len(triples)} triples from file.")
                        else:
                            st.warning("No triples could be extracted from the uploaded file.")
                    else:
                        st.error("No text column found in the file. Please upload a file with sentences/text.")
                except Exception as e:
                    st.error(f"❌ File extraction failed: {e}")

    # 3️⃣ Sample Text Option
    else:
        if st.button("📄 Load Sample Text"):
            sample = (
                "Albert Einstein was born in Ulm. "
                "Paris is the capital of France. "
                "Aspirin treats headache. "
                "Tesla was founded by Elon Musk."
            )
            triples = extract_triples_from_text(sample)
            st.success(f"✅ Extracted {len(triples)} sample triples")

    # 4️⃣ Show Extracted Triples & Graph
    if triples:
        # Handle both 3-tuple and 4-tuple formats
        if len(triples[0]) == 4:
            df = pd.DataFrame(triples, columns=["Subject", "Relation", "Object", "Confidence"])
        else:
            df = pd.DataFrame(triples, columns=["Subject", "Relation", "Object"])

        st.subheader("📋 Extracted Triples")
        st.dataframe(df)

        # Visualize triples as graph
        st.subheader("📊 Triple Graph Visualization")
        net = Network(height="600px", width="100%", bgcolor="#ffffff", directed=True)

        for t in triples:
            subj, rel, obj = t[:3]
            conf = t[3] if len(t) == 4 else None
            edge_label = f"{rel} ({conf:.2f})" if conf else rel

            net.add_node(subj, label=subj, color="#90ee90")
            net.add_node(obj, label=obj, color="#ffcccb")
            net.add_edge(subj, obj, label=edge_label)

        net.repulsion(node_distance=180, spring_length=150)
        os.makedirs("outputs", exist_ok=True)
        out_file = "outputs/triples_graph.html"
        net.save_graph(out_file)

        with open(out_file, "r", encoding="utf-8") as html_file:
            html = html_file.read()
        st.components.v1.html(html, height=650, scrolling=True)
