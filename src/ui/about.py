# src/ui/about.py
import streamlit as st

def about_page():
    st.header("ℹ️ About KnowMap")
    st.markdown("""
    **KnowMap — Milestone 3**  
    Developed under the Cross-Domain Knowledge Mapping project.
    
    - Built with **Streamlit**, **spaCy**, **NetworkX**, **PyVis**, and **Sentence-Transformers**  
    - Supports English + Hindi/Hinglish queries  
    - Provides **semantic graph exploration**, **triple extraction**, and **multimodal search**

    ---
    © 2025 KnowMap AI · For educational use only.
    """)
