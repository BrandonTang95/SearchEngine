import pymongo
import math
from collections import defaultdict
from nltk import ngrams
import re

# Sample documents
documents = [
    "After the medication, headache and nausea were reported by the patient.",
    "The patient reported nausea and dizziness caused by the medication.",
    "Headache and dizziness are common effects of this medication.",
    "The medication caused a headache and nausea, but no dizziness was reported.",
]

# MongoDB Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["search_engine"]
terms_collection = db["terms"]
documents_collection = db["documents"]


# Step 1: Preprocess the documents
def preprocess_document(doc):
    doc = re.sub(r"[^\w\s]", "", doc)  # Remove punctuation
    doc = doc.lower()  # Convert to lowercase
    words = doc.split()  # Tokenize words
    unigrams = words
    bigrams = [" ".join(ngram) for ngram in ngrams(words, 2)]
    trigrams = [" ".join(ngram) for ngram in ngrams(words, 3)]
    return unigrams + bigrams + trigrams


# Step 2: Build Inverted Index and Store in MongoDB
def build_inverted_index(documents):
    # Clear the collections to avoid duplicates
    documents_collection.delete_many({})  # Clear all documents
    terms_collection.delete_many({})  # Clear all terms

    term_to_docs = defaultdict(list)

    # Store documents in MongoDB
    for doc_id, content in enumerate(documents, start=1):
        tokens = preprocess_document(content)
        token_counts = defaultdict(int)

        for token in tokens:
            token_counts[token] += 1

        # Save document with raw content
        documents_collection.insert_one({"_id": doc_id, "content": content})

        # Update inverted index
        for token, count in token_counts.items():
            term_to_docs[token].append({"doc_id": doc_id, "tf": count})

    # Save terms to MongoDB
    vocabulary = {term: i for i, term in enumerate(term_to_docs.keys())}
    for term, docs in term_to_docs.items():
        terms_collection.insert_one(
            {
                "term": term,
                "pos": vocabulary[term],  # Add the position
                "docs": docs,
            }
        )
    return vocabulary


# Step 3: Compute Cosine Similarity
def compute_cosine_similarity(query, vocabulary):
    query_tokens = preprocess_document(query)
    query_vector = {
        vocabulary[token]: 1 for token in query_tokens if token in vocabulary
    }
    doc_scores = defaultdict(float)

    # Retrieve matching documents
    for token in query_tokens:
        term = terms_collection.find_one({"term": token})
        if term:
            for doc in term["docs"]:
                doc_id = doc["doc_id"]
                tf = doc["tf"]

                # Compute the score incrementally for each document
                doc_scores[doc_id] += query_vector.get(term["pos"], 0) * tf

    # Retrieve and rank documents based on scores
    results = []
    for doc_id, score in doc_scores.items():
        doc_content = documents_collection.find_one({"_id": doc_id})["content"]
        results.append((doc_content, score))

    # Sort results by score in descending order
    results.sort(key=lambda x: x[1], reverse=True)
    return results


# Build the index
vocabulary = build_inverted_index(documents)

# Queries
queries = [
    "nausea and dizziness",
    "effects",
    "nausea was reported",
    "dizziness",
    "the medication",
]

# Step 4: Execute Queries and Display Results
for i, query in enumerate(queries, start=1):
    print(f"Query {i}: {query}")
    results = compute_cosine_similarity(query, vocabulary)
    for content, score in results:
        print(f"{content}, {score:.2f}")
    print()
