from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri=None, user=None, password=None):
        """
        Initialize Neo4j connection handler.
        If credentials are not passed here, you can connect later using connect().
        """
        self.driver = None
        self.uri = uri
        self.user = user
        self.password = password

        if uri and user and password:
            self.connect(uri, user, password)

    def connect(self, uri, user, password):
        """Connect to Neo4j Database"""
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()  # ✅ verifies the connection
            print("✅ Successfully connected to Neo4j!")
            return True, "✅ Connected to Neo4j successfully!"
        except Exception as e:
            print("❌ Connection failed:", e)
            self.driver = None
            return False, f"❌ Connection failed: {e}"

    def close(self):
        """Close the connection"""
        if self.driver:
            self.driver.close()
            print("🔒 Connection closed.")

    def store_triples(self, triples):
        """Store extracted triples in Neo4j"""
        if not self.driver:
            return "⚠️ Not connected to Neo4j."

        stored = 0
        with self.driver.session() as session:
            for t in triples:
                # Handle both 3-tuple and 4-tuple formats
                if len(t) == 3:
                    subj, rel, obj = t
                    conf = 1.0
                else:
                    subj, rel, obj, conf = t

                if not subj or not obj:
                    continue

                # Neo4j relationship labels must be uppercase and no spaces
                rel_label = rel.upper().replace(" ", "_")

                query = f"""
                MERGE (a:Entity {{name: $subj}})
                MERGE (b:Entity {{name: $obj}})
                MERGE (a)-[r:{rel_label} {{confidence: $conf}}]->(b)
                """
                session.run(query, {"subj": subj, "obj": obj, "conf": conf})
                stored += 1

        return f"✅ {stored} triples stored in Neo4j successfully!"

    def fetch_graph(self):
        """Fetch full graph (nodes and edges) from Neo4j"""
        if not self.driver:
            return [], []

        with self.driver.session() as session:
            nodes = session.run("MATCH (n) RETURN DISTINCT n.name AS name").data()
            edges = session.run("""
                MATCH (a)-[r]->(b)
                RETURN a.name AS source, type(r) AS relation, b.name AS target
            """).data()

        return nodes, edges
