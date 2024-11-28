# SearchEngine

# **MongoDB Search Engine with Vector Space Model**

## **Overview**
This project implements a simple search engine using a **Vector Space Model**. The engine builds an inverted index for a set of documents, stores it in MongoDB, and processes queries to rank documents based on their relevance to the query. It uses cosine similarity for ranking, allowing for efficient information retrieval.

---

## **Features**
- **Inverted Index**: 
  - Terms are stored in MongoDB (`terms` collection), referencing the documents they appear in.
  - Index supports unigrams, bigrams, and trigrams.
- **Document Storage**: 
  - Original documents are stored in MongoDB (`documents` collection) without stemming, lemmatization, or stop-word removal.
- **Query Processing**:
  - Handles queries by retrieving relevant documents using the inverted index.
  - Ranks documents using the **Vector Space Model** with cosine similarity.
- **TF-IDF Weights**:
  - Tracks term frequencies for efficient scoring.
- **MongoDB Integration**:
  - Uses MongoDB for storing and querying terms and documents.
- **Output**:
  - Displays ranked documents with scores for each query.

---

## **Setup Instructions**

### **1. Prerequisites**
- **Python 3.7 or higher**  
- **MongoDB installed and running**  
  - [Download MongoDB Community Edition](https://www.mongodb.com/try/download/community)
- **Required Python Libraries**:
  Install dependencies with:
  ```bash
  pip install pymongo nltk
  ```

---

### **2. Usage**
1. Clone the repository or save the script.
2. Run the script:
   ```bash
   python search_engine.py
   ```
3. The script will:
   - Build an inverted index for the sample documents.
   - Process queries.
   - Output ranked results for each query.

---

## **Project Structure**

### **Main Script**
- **`search_engine.py`**:
  - Builds the inverted index and stores it in MongoDB.
  - Handles queries and ranks documents using cosine similarity.

### **MongoDB Collections**
- **`documents`**:
  - Stores original documents with their `_id` and `content`.
  - Example:
    ```json
    {
        "_id": 1,
        "content": "After the medication, headache and nausea were reported by the patient."
    }
    ```
- **`terms`**:
  - Stores the inverted index with terms, their position in the vocabulary, and document references.
  - Example:
    ```json
    {
        "_id": ObjectId("..."),
        "term": "nausea",
        "pos": 7,
        "docs": [
            { "doc_id": 1, "tf": 1 },
            { "doc_id": 2, "tf": 1 },
            { "doc_id": 4, "tf": 1 }
        ]
    }
    ```

---

## **Query Example**

### Sample Queries:
1. `"nausea and dizziness"`
2. `"effects"`
3. `"nausea was reported"`
4. `"dizziness"`
5. `"the medication"`

### Console Output Example:
For the query **"nausea and dizziness"**, the output might look like:
```
Query 1: nausea and dizziness
The patient reported nausea and dizziness caused by the medication., 6.00
The medication caused a headache and nausea, but no dizziness was reported., 3.00
Headache and dizziness are common effects of this medication., 3.00
After the medication, headache and nausea were reported by the patient., 2.00
```

---

## **How It Works**

### **Step 1: Preprocessing**
- Documents are tokenized into:
  - Unigrams: Individual words (e.g., `"nausea"`).
  - Bigrams: Two-word combinations (e.g., `"nausea was"`).
  - Trigrams: Three-word combinations (e.g., `"nausea was reported"`).
- Punctuation is removed, and all terms are lowercased.

### **Step 2: Build Inverted Index**
- Terms are stored with their:
  - **`pos`**: Position in the vocabulary.
  - **`docs`**: List of documents containing the term, including the term frequency (TF).

### **Step 3: Query Execution**
- Each query is tokenized into unigrams, bigrams, and trigrams.
- Relevant documents are retrieved from the `terms` collection.
- Cosine similarity scores are calculated for matching documents.

### **Step 4: Ranking**
- Documents are ranked based on cosine similarity scores.
- Results are displayed in descending order of relevance.

---

## **Enhancements**
- **Boolean Operators**: Add support for `AND`, `OR`, and `NOT` in queries.
- **Stop Words**: Optionally remove stop words to improve relevance.
- **Normalization**: Normalize scores to account for document length.

---

## **Dependencies**
- **Python Libraries**:
  - `pymongo`: For MongoDB integration.
  - `nltk`: For generating bigrams and trigrams.
  - `re`: For text preprocessing.
- **MongoDB**:
  - Required for storing and retrieving terms and documents.

---

## **Conclusion**
This project demonstrates a simple but efficient search engine using the Vector Space Model. The use of MongoDB ensures scalability for handling large datasets, while the implementation provides a solid foundation for further enhancements like Boolean queries and advanced ranking mechanisms.

