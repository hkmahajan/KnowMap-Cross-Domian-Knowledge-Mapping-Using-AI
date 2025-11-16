# src/ui/app.py
import sys, os, time, json
import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# --- Import internal modules ---
from src.nlp.ner_re import extract_triples_from_text, extract_triples_from_file, save_triples_to_csv
from src.graph.build_graph import build_graph, load_graph, union_subgraphs, subgraph_to_json
from src.semantic.embed_index import build_index, load_index, semantic_search
from src.ui.admin_dashboard import admin_dashboard
from src.ui.graph_editor import graph_editor
from src.ui.feedback_page import feedback_page
from src.ui.deployment_page import deployment_page




# --- Import sub-pages ---
from src.ui.home import home_page
from src.ui.upload import upload_page
from src.ui.graph_page import graph_page
from src.ui.semantic_search import semantic_search_page
from src.ui.about import about_page
from src.ui.auth import auth_page
from src.graph.neo4j_utils import Neo4jHandler
from pyvis.network import Network
from src.ui.entity_extraction import entity_extraction_page

import json
neo4j_handler = Neo4jHandler()



# --- Global Page Config ---
st.set_page_config(page_title="KnowMap Dashboard", layout="wide", page_icon="🧠")

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
if "auth_user" not in st.session_state:
    auth_page()
    st.stop()

st.sidebar.success(f"👋 Logged in as: {st.session_state['auth_user']}")
if st.sidebar.button("Logout"):
    del st.session_state["auth_user"]
    st.rerun()

page = st.sidebar.radio(
    "Go to",
    ["🏠 Home",
        "📁 Upload",
        "⚙️ Build Graph",
        "🔍 Semantic Search",
        "🧾 Admin Dashboard",
        "🧠 Entity Extraction",
        "🧩 Graph Editor",
        "💬 Feedback",
        "ℹ️ About"],
)


# --- Routing ---
if page == "🏠 Home":
    home_page()
elif page == "📁 Upload":
    upload_page()
elif page == "⚙️ Build Graph":
    graph_page()
elif page == "🔍 Semantic Search":
    semantic_search_page()
elif page == "🧾 Admin Dashboard":
    admin_dashboard()
elif page == "🧠 Entity Extraction":
    entity_extraction_page()    
elif page == "🧩 Graph Editor":
    graph_editor()
elif page == "💬 Feedback":
    feedback_page()
elif page == "ℹ️ About":
    about_page()





# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.caption(" Knowledge Graph Explorer")
