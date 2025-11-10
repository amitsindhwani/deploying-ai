"""
This code is used to convert financial gloassary from the csv file to embeddings used by semantic service.

"""

from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import chromadb
from chromadb import PersistentClient


print("Loading model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Reading CSV...")
df = pd.read_csv("05_src/assignment_chat/data/financial glossary.csv")

term_definition = df["Definition"].tolist()
embeddings = model.encode(term_definition)

print("Creating ChromaDB client...")
client = PersistentClient(path="semantic_finance_db")
collection = client.get_or_create_collection("finance_knowledge")

print("Adding data to ChromaDB...")
collection.add(
    documents=term_definition,
    embeddings=embeddings.tolist(),
    metadatas=[{"Term": t} for t in df["Term"].tolist()],
    ids=[str(i) for i in range(len(term_definition))]
)

print("Database created and persisted.")
