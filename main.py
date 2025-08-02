from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# 1. Load model from local path
model = SentenceTransformer('./models/all-MiniLM-L6-v2')

# 2. Text inputs
texts = [
    "Python is a programming language.",
    "Django is a Python web framework.",
    "SpaceX is an aerospace company."
]

# 3. Generate embeddings
embeddings = model.encode(texts)

# 4. Connect to Neo4j (adjust credentials if needed)
uri = "bolt://localhost:7687"
username = "neo4j"
password = "123456@#"

driver = GraphDatabase.driver(uri, auth=(username, password))

# 5. Create nodes and relationships in Neo4j
def store_in_neo4j(tx, text, vector):
    tx.run(
        "MERGE (t:Text {content: $text, embedding: $embedding})",
        text=text,
        embedding=vector.tolist()
    )

with driver.session() as session:
    for text, embedding in zip(texts, embeddings):
        session.execute_write(store_in_neo4j, text, embedding)

print("✅ Data stored in Neo4j!")

# 6. Close driver
driver.close()
