# src/ui/graph_page.py
import streamlit as st
import os
from src.graph.build_graph import build_graph, load_graph, get_graph_stats
from src.semantic.embed_index import build_index, load_index
from pyvis.network import Network
import streamlit.components.v1 as components

def graph_page():
    st.markdown("## 🧠 Knowledge Graph Builder & Indexer")
    st.info("This step builds or refreshes the graph from extracted triples, and creates embeddings for semantic search.")

    if not os.path.exists("data/triples.csv"):
        st.warning("No triples file found. Go to the Upload page to extract triples first.")
        return

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔨 Build / Refresh Graph"):
            try:
                G = build_graph()
                stats = get_graph_stats(G)
                st.success(f"Graph built successfully with {stats['nodes']} nodes and {stats['edges']} edges.")
                st.rerun()
            except Exception as e:
                st.error(f"Graph build failed: {e}")

    with col2:
        if st.button("📊 Build Embedding Index"):
            try:
                G = load_graph()
                nodes = list(G.nodes())
                count, dim = build_index(nodes)
                st.success(f"Built embeddings for {count} nodes (vector dim {dim}).")
            except Exception as e:
                st.error(f"Embedding index build failed: {e}")

    st.markdown("---")
    
    # Display graph statistics
    if os.path.exists("outputs/knowledge_graph.gpickle"):
        try:
            G = load_graph()
            stats = get_graph_stats(G)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nodes", stats["nodes"])
            with col2:
                st.metric("Edges", stats["edges"])
            with col3:
                if os.path.exists("outputs/embeddings.npy"):
                    st.metric("Index Status", "✅ Ready")
                else:
                    st.metric("Index Status", "⚠️ Not Built")
            
            # Add graph visualization
            st.markdown("---")
            st.markdown("### 🕸️ Full Knowledge Graph Visualization")
            
            # Limit visualization for large graphs
            max_nodes = st.slider("Max nodes to display", 10, 500, min(100, stats["nodes"]))
            
            if st.button("📊 Visualize Graph"):
                try:
                    # Create subgraph with limited nodes
                    nodes_to_show = list(G.nodes())[:max_nodes]
                    subG = G.subgraph(nodes_to_show)
                    
                    # Create PyVis network
                    net = Network(height="700px", width="100%", bgcolor="#FFFFFF", directed=True, notebook=False)
                    
                    # Add nodes
                    for node in subG.nodes():
                        degree = subG.degree(node)
                        size = 10 + min(degree * 3, 40)  # Scale size by connections
                        color = "#97C2FC" if degree < 3 else "#FFA500"
                        net.add_node(node, label=node, title=f"{node} ({degree} connections)", size=size, color=color)
                    
                    # Add edges
                    for u, v, d in subG.edges(data=True):
                        relation = d.get("relation", "")
                        confidence = d.get("confidence", 1.0)
                        net.add_edge(u, v, title=f"{relation} ({confidence:.2f})", label=relation[:20])
                    
                    # Configure physics
                    net.repulsion(node_distance=200, central_gravity=0.3, spring_length=200, spring_strength=0.05)
                    
                    # Save and display
                    os.makedirs("outputs", exist_ok=True)
                    graph_path = "outputs/full_graph.html"
                    net.save_graph(graph_path)
                    
                    with open(graph_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                    components.html(html_content, height=720, scrolling=True)
                    
                    st.info(f"Displaying {len(nodes_to_show)} nodes out of {stats['nodes']} total nodes")
                    
                except Exception as e:
                    st.error(f"Visualization failed: {e}")
                    
        except Exception as e:
            st.error(f"Graph load failed: {e}")
    else:
        st.info("Graph not built yet. Click 'Build / Refresh Graph' to create it.")
