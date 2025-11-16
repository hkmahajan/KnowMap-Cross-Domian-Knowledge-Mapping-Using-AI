# 🧠 KnowMap — Cross-Domain Knowledge Graph Explorer

**KnowMap** is an intelligent NLP-based system that extracts entity-relation triples from text, builds a knowledge graph, and allows users to explore semantic relationships through an interactive Streamlit dashboard. It integrates with **Neo4j** for persistent graph storage and provides advanced semantic search capabilities.

---

## ✨ Features

- 🔐 **User Authentication System** - Secure login and registration
- 🧩 **Entity & Relation Extraction** - Automated NLP pipeline using SpaCy
- 🕸️ **Interactive Graph Visualization** - Dynamic graph rendering with PyVis
- 🧠 **Neo4j Database Integration** - Persistent graph storage and querying
- 🔍 **Semantic Search** - Multilingual search using Sentence Transformers
- 📄 **Multi-format Upload** - Support for CSV, Excel, and text files
- 📊 **Graph Analytics** - Node statistics and relationship insights
- 🎨 **Graph Editor** - Interactive node and edge editing
- 💬 **Feedback System** - User feedback collection and management
- 🧾 **Admin Dashboard** - System monitoring and user management

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Frontend/UI** | Streamlit, PyVis |
| **NLP Processing** | SpaCy, Transformers |
| **Database** | Neo4j (optional), SQLite |
| **Graph Processing** | NetworkX |
| **Machine Learning** | Sentence Transformers |
| **Deployment** | Docker, Docker Compose |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Neo4j database for persistent storage

### Installation

#### 1️⃣ Clone the repository
```bash
git clone https://github.com/hkmahajan/KnowMap-Cross-Domian-Knowledge-Mapping-Using-AI.git
cd KnowMap-Cross-Domian-Knowledge-Mapping-Using-AI

cd KnowMap-Cross-Domian-Knowledge-Mapping-Using-AI
```

#### 2️⃣ Create and activate virtual environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

#### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### 4️⃣ Run the application
```bash
streamlit run src/ui/app.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🐳 Docker Deployment

### Option 1: Using Docker Compose (Recommended)
```bash
docker-compose up
```

### Option 2: Build and Run Manually
```bash
# Build the image
docker build -t knowmap-app .

# Run the container
docker run -p 8501:8501 knowmap-app
```

Access the application at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. **Authentication**
- Create an account or login with existing credentials
- All user data is stored securely in SQLite database

### 2. **Upload Data**
- Navigate to **📁 Upload** page
- Choose input method:
  - Enter text directly
  - Upload CSV/Excel files
  - Use sample data
- Extract entity-relation triples automatically

### 3. **Build Knowledge Graph**
- Go to **⚙️ Build Graph** page
- Click "Build/Refresh Graph" to create the knowledge graph
- Build embedding index for semantic search
- Visualize the full graph with adjustable node limits

### 4. **Semantic Search**
- Visit **🔍 Semantic Search** page
- Enter search queries (supports English and Hindi)
- Adjust top-k results and exploration radius
- View interactive subgraph visualizations
- Download results as JSON or CSV

### 5. **Graph Editing**
- Use **🧩 Graph Editor** to modify nodes and relationships
- Add, edit, or delete graph elements
- Changes are reflected in real-time

### 6. **Admin Dashboard**
- Monitor system statistics
- View user activity logs
- Manage feedback submissions

---

## 🗺️ System Architecture

```
Text Input → NLP Extraction → Triple Generation → Graph Building → Embedding Index → Visualization & Search
                                                         ↓
                                                   Neo4j Storage
                                                    (Optional)
```

---

## 📁 Project Structure

```
KnowMap/
├── src/
│   ├── nlp/
│   │   └── ner_re.py              # Entity extraction & relation detection
│   ├── graph/
│   │   ├── build_graph.py         # Graph construction logic
│   │   └── neo4j_utils.py         # Neo4j database operations
│   ├── semantic/
│   │   └── embed_index.py         # Embedding generation & search
│   └── ui/
│       ├── app.py                 # Main application entry
│       ├── auth.py                # Authentication system
│       ├── home.py                # Home page
│       ├── upload.py              # Data upload interface
│       ├── graph_page.py          # Graph builder & visualizer
│       ├── semantic_search.py     # Semantic search interface
│       ├── graph_editor.py        # Graph editing tools
│       ├── admin_dashboard.py     # Admin panel
│       ├── feedback_page.py       # Feedback system
│       └── about.py               # About page
├── data/                          # Extracted triples (CSV)
├── outputs/                       # Generated graphs & embeddings
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose setup
└── README.md                      # Documentation
```

---

## 🔧 Configuration

### Neo4j Setup (Optional)
To enable Neo4j integration:

1. Install Neo4j Desktop or use Docker:
```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

2. Configure connection in the app sidebar:
   - URI: `bolt://localhost:7687`
   - Username: `neo4j`
   - Password: Your password

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](licence) file for details.

---

## 🙏 Acknowledgments

- **SpaCy** for NLP processing
- **Sentence Transformers** for semantic embeddings
- **NetworkX** for graph algorithms
- **PyVis** for interactive visualizations
- **Streamlit** for the web interface
- **Neo4j** for graph database capabilities

---

## 📧 Contact

For questions, suggestions, or issues, please open an issue on GitHub.

---

**⭐ Star this repository if you find it helpful!**


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

