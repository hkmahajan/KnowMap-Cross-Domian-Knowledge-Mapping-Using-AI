import streamlit as st

def deployment_page():
    st.title("🚀 Deployment & Project Info")
    st.markdown("""
    ### Deployment Options
    - 🌐 **Streamlit Cloud**: Deploy directly using `streamlit deploy`
    - 🤗 **Hugging Face Spaces**: Host app using Gradio/Streamlit template
    - 🐳 **Docker**: Build image and run locally using `docker-compose`

    ### Project Summary
    - **Pipeline:** Entity & Relation Extraction → Neo4j → Streamlit Visualization  
    - **Admin Tools:** Monitor pipeline and fix data manually  
    - **Feedback System:** Collect user ratings to improve NLP accuracy  
    - **Deployment:** Production-ready dashboard  
    """)
