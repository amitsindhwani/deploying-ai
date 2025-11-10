"""
Service 2: Semantic Query Service (Financial Glossary)

This service allows users to ask questions about financial terms and retrieves answers using semantic search over a precompiled
ChromaDB of financial glossary definitions.

Note: I am using Financial terms glossary from the SIFMA Foundation SMG Glossary pdf (Copyright 2023 SIFMA Foundation), I copied page by page and 
created a csv file out of the terms listed in the pdf). The credit for the glossary goes to them.

A PDF glossary from the SIFMA Foundation/The Stock Market Game covers many terms related to investing and trading. 
https://www.stockmarketgame.org/SMG_Glossary.pdf?utm_source=chatgpt.com


"""

import os
import json
import numpy as np
import pandas as pd
from typing import List, Optional

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer


print("------Semantic Query Service------")

# Load model for query embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load precomputed ChromaDB collection
client = PersistentClient(path="semantic_finance_db")
collection = client.get_collection("finance_knowledge")

def semantic_query(user_query: str, top_k: int = 3) -> str:
    """
    Perform semantic search on the financial glossary.
    Returns the top-k relevant definitions as a readable string.
    """

    print("User query:", user_query)
    
    # Convert user query to embedding
    user_query_embedding = model.encode([user_query])[0]
    print("Query embedding generated (shape):", user_query_embedding.shape)

    # Search collection
    print("Search collection with the user query embeddings")
    
    query_results = collection.query(
        query_embeddings=[user_query_embedding],
        n_results=top_k
    )

    # Extract the terms and definitions
    print("Extract the terms and defintions")
    
    response_lines = []
    for term, definition in zip(query_results['metadatas'][0], query_results['documents'][0]):
        response_lines.append(f"{term['Term']}: {definition}")

    # Combine into one readable string
    final_response = "\n".join(response_lines)
    print("Final formatted response:\n", final_response)
    
    return final_response

