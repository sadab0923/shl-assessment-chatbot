import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("catalog.json", "r") as f:
    catalog = json.load(f)

texts = []

for item in catalog:

    text = (
        item.get("name", "") +
        " " +
        item.get("description", "")
    )

    texts.append(text)

if len(texts) == 0:
    raise Exception("No catalog data found")

embeddings = model.encode(texts)

embeddings = np.array(embeddings).astype("float32")

# FIX
if len(embeddings.shape) == 1:
    embeddings = embeddings.reshape(1, -1)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)


def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx < len(catalog):
            results.append(catalog[idx])

    return results
