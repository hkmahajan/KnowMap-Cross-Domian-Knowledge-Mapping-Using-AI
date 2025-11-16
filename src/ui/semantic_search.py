# src/ui/semantic_search.py
import os
import json
import streamlit as st
import networkx as nx
import pandas as pd
from pyvis.network import Network
from src.graph.build_graph import load_graph, subgraph_to_json
from src.semantic.embed_index import load_index, semantic_search

def semantic_search_page():
    st.markdown("## 🔍 Semantic Search & Exploration")
    st.info("Enter a query to find the most related nodes using embeddings, then visualize the resulting subgraph interactively.")

    # Check data availability
    if not os.path.exists("outputs/knowledge_graph.gpickle"):
        st.warning("Graph not built yet. Please build it first in the Graph Builder page.")
        return
    if not os.path.exists("outputs/embeddings.npy"):
        st.warning("Embedding index not found. Please build the index first.")
        return

    # Sidebar controls
    st.sidebar.header("Search Configuration")
    query = st.sidebar.text_input("Enter search query", placeholder="e.g., pain relief, dard ki dawa, Einstein")
    top_k = st.sidebar.slider("Top-k results", 1, 10, 5)
    radius = st.sidebar.slider("Subgraph exploration radius (k-hop)", 1, 3, 1)
    show_rel = st.sidebar.checkbox("Show edge relations", True)

    if st.sidebar.button("🚀 Perform Search"):
        try:
            # Load embeddings and graph
            nodes, embeddings = load_index()
            G = load_graph()

            results = semantic_search(query, nodes, embeddings, top_k=top_k)
            if not results:
                st.warning("No matching nodes found.")
                return

            st.subheader("Top Matching Nodes")
            for i, (node, score) in enumerate(results, 1):
                st.write(f"**#{i}** → {node} | **Score:** {score:.3f} | Connections: {len(G[node])}")

            # Expand subgraph around top matches
            selected_nodes = [n for n, _ in results]
            sub = nx.DiGraph()
            for n in selected_nodes:
                ego = nx.ego_graph(G, n, radius=radius)
                sub = nx.compose(sub, ego)

            if sub.number_of_nodes() == 0:
                st.warning("Subgraph is empty. Try a higher radius.")
                return

            # --- Visualization ---
            st.markdown("### 🕸️ Connected Subgraph")
            net = Network(height="700px", width="100%", bgcolor="#FFFFFF", directed=True)
            top_nodes = set(selected_nodes)

            for node in sub.nodes():
                color = "#ff4d4d" if node in top_nodes else "#97C2FC"
                net.add_node(node, label=node, title=node, color=color)

            for u, v, d in sub.edges(data=True):
                label = d.get("relation", "")
                conf = d.get("confidence", 1.0)
                edge_color = "#444444"
                if label.lower() in ("treats", "discovered"):
                    edge_color = "#00cc44"
                elif label.lower() in ("capital_of", "born_in"):
                    edge_color = "#3366ff"
                elif label.lower() in ("invented", "works_at"):
                    edge_color = "#ff9933"

                net.add_edge(u, v, label=label if show_rel else "", title=f"{label} ({conf:.2f})", color=edge_color)

            net.repulsion(node_distance=180, spring_length=150)
            os.makedirs("outputs", exist_ok=True)
            graph_html = os.path.join("outputs", "subgraph.html")
            net.save_graph(graph_html)
            st.components.v1.html(open(graph_html, "r", encoding="utf-8").read(), height=720, scrolling=True)

            # --- Download options ---
            st.markdown("### 📥 Download Subgraph")
            json_data = subgraph_to_json(sub)
            st.download_button(
                "Download as JSON",
                data=json.dumps(json_data, indent=2),
                file_name="subgraph.json",
                mime="application/json"
            )

            # Optional CSV export
            edges = [(u, v, d.get("relation", ""), d.get("confidence", 1.0)) for u, v, d in sub.edges(data=True)]
            edges_df = pd.DataFrame(edges, columns=["Source", "Target", "Relation", "Confidence"])
            csv_data = edges_df.to_csv(index=False).encode("utf-8")
            st.download_button("Download as CSV", data=csv_data, file_name="subgraph_edges.csv", mime="text/csv")

            # --- Stats summary ---
            st.markdown("---")
            st.metric("Nodes in Subgraph", sub.number_of_nodes())
            st.metric("Relationships", sub.number_of_edges())
            st.info("Red nodes are the top matching nodes from semantic search.")

        except Exception as e:
            st.error(f"Search failed: {e}")
