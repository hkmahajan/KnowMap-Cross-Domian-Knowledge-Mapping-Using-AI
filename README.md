# 🧠 KnowMap — Cross-Domain Knowledge Graph Explorer

**KnowMap** is an intelligent NLP-based system that extracts entity–relation triples from text, builds a knowledge graph, and allows users to explore semantic relationships through an interactive Streamlit dashboard. It also integrates with **Neo4j** for persistent graph storage and visualization.

---

## 🚀 Features

- 🔐 **User Authentication System**
- 🧩 **Entity & Relation Extraction (NLP Pipeline)**
- 🕸️ **Knowledge Graph Visualization**
- 🧠 **Neo4j Database Integration**
- 🔍 **Semantic Search on Graph Nodes**
- 📄 **CSV/Text Upload Support**
- 🧾 **Admin Dashboard & Feedback System**
- 🧰 **Dockerized Deployment**

---

## 🧰 Tech Stack

| Category | Tools/Frameworks |
|-----------|------------------|
| **Frontend/UI** | Streamlit |
| **Backend/NLP** | SpaCy, Transformers |
| **Database** | Neo4j |
| **Graph Processing** | NetworkX, PyVis |
| **Machine Learning** | Sentence Transformers |
| **Deployment** | Docker |

---

## 🧑‍💻 Run Locally (Development Setup)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ishwari418/Knowmap-cross-domain-knowledge-mapping-.git
cd knowmap

2️⃣ Create & activate a virtual environment

python -m venv env
env\Scripts\activate   # (on Windows)
# or
source env/bin/activate   # (on Mac/Linux)

3️⃣ Install dependencies

pip install -r requirements.txt
python -m spacy download en_core_web_sm

4️⃣ Run Streamlit app

streamlit run src/ui/app.py


🐳 Run via Docker (One Command)
If you don’t want to install anything manually, use Docker:

docker pull ishwari29/knowmap-app:latest
docker run -p 8501:8501 ishwari29/knowmap-app:latest

Then open http://localhost:8501
 in your browser.

🟢 This image includes the complete Streamlit app with all dependencies preinstalled.


🗺️ Project Workflow

Text Input → User enters or uploads text/CSV

NLP Extraction → Entities & Relations extracted as triples

Graph Construction → Built using NetworkX & saved as .gpickle

Semantic Search → Contextual node search via embeddings

Visualization → Interactive graph using PyVis

Neo4j Storage → Persistent knowledge graph for querying


📦 Directory Structure

knowmap-milestone/
├─ data/
│   └─ triples.csv
├─ outputs/
│   └─ knowledge_graph.gpickle
├─ users/
│   └─ users.db  ← authentication store
├─ src/
│  ├─ nlp/
│  │   └─ ner_re.py
│  ├─ graph/
│  │   └─ build_graph.py
│  ├─ semantic/
│  │   └─ embed_index.py
│  ├─ ui/
│  │   ├─ auth.py       ← login/register
│  │   ├─ dashboard.py  ← main dashboard
│  │   ├─ upload.py     ← upload dataset
│  │   ├─ search.py     ← semantic search explorer
│  │   └─ app.py        ← main entry point with navigation
└─ requirements.txt

⚖️ License

This project is licensed under the MIT License — you’re free to use, modify, and distribute it.


👩‍💻 Author

Ishwari Belhekar
B.Tech CSE (AI & ML)
ishwaribelhekar29@gmail.com
