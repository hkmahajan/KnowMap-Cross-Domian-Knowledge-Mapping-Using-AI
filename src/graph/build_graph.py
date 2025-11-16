import os
import pandas as pd
import networkx as nx
import json

DATA_PATH = "data/triples.csv"
OUTPUT_PATH = "outputs/knowledge_graph.gpickle"

def build_graph(csv_path: str = DATA_PATH):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"{csv_path} not found")

    df = pd.read_csv(csv_path)
    df.columns = [c.lower().strip() for c in df.columns]

    if not all(col in df.columns for col in ["subject", "relation", "object"]):
        raise ValueError("CSV must contain columns: subject, relation, object")

    G = nx.DiGraph()
    for _, row in df.iterrows():
        s = str(row["subject"]).strip()
        o = str(row["object"]).strip()
        r = str(row["relation"]).strip()
        try:
            conf = float(row.get("confidence", 1.0))
        except:
            conf = 1.0
        G.add_node(s)
        G.add_node(o)
        G.add_edge(s, o, relation=r, confidence=conf)

    os.makedirs("outputs", exist_ok=True)
    nx.write_gpickle(G, OUTPUT_PATH)
    return G

def load_graph():
    if not os.path.exists(OUTPUT_PATH):
        raise FileNotFoundError("Graph file not found. Build it first.")
    return nx.read_gpickle(OUTPUT_PATH)

def union_subgraphs(G, nodes, radius=1, relation_filter=None, min_confidence=0.0):
    sub = nx.DiGraph()
    for node in nodes:
        if node not in G:
            continue
        ego = nx.ego_graph(G, node, radius=radius, undirected=False)
        sub = nx.compose(sub, ego)

    edges_to_remove = []
    for u, v, d in sub.edges(data=True):
        try:
            conf = float(d.get("confidence", 0))
        except:
            conf = 0
        if conf < min_confidence:
            edges_to_remove.append((u, v))
        if relation_filter and d.get("relation", "") not in relation_filter:
            edges_to_remove.append((u, v))
    sub.remove_edges_from(edges_to_remove)
    sub.remove_nodes_from(list(nx.isolates(sub)))
    return sub

def subgraph_to_json(sub: nx.DiGraph):
    data = {"nodes": [], "edges": []}
    for node in sub.nodes():
        data["nodes"].append({"id": node, "label": node})
    for u, v, d in sub.edges(data=True):
        try:
            conf = float(d.get("confidence", 1.0))
        except:
            conf = 1.0
        data["edges"].append({
            "source": u,
            "target": v,
            "relation": d.get("relation", ""),
            "confidence": conf
        })
    return data

def get_graph_stats(G):
    if G is None:
        return {"nodes": 0, "edges": 0, "density": 0, "avg_degree": 0}
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    density = nx.density(G)
    avg_degree = (2 * num_edges / num_nodes) if num_nodes > 0 else 0
    return {"nodes": num_nodes, "edges": num_edges, "density": round(density,4), "avg_degree": round(avg_degree,2)}
