# src/ui/home.py
import streamlit as st

def home_page():
    st.title("🧠 KnowMap — Knowledge Mapping AI")
    st.markdown("""
    ### Welcome!
    """)
    

    st.markdown("""
    **Quick Steps**
    1. Go to *Upload* page to provide text or file.  
    2. Build the Knowledge Graph and Embedding Index.  
    3. Use *Semantic Search* to explore.  
    4. Visualize subgraphs interactively and export results.
    """)
