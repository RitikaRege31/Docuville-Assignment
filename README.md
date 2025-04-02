# Docuville Assignment
 
┌──────────────────────────────────────────────────────────────┐
│          DOCUMENT SIMILARITY DETECTION SYSTEM                │
└──────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────┐
│                     SYSTEM COMPONENTS                        │
└──────────────────────────────────────────────────────────────┘

┌────────────┐    ┌───────────┐    ┌────────────┐    ┌─────────────┐
│            │    │           │    │            │    │             │
│ Document   │    │ Prepro-   │    │ Similarity │    │  Results    │
│ Ingestion  │───▶│ cessing  │───▶│ Detection  │──▶│Visualization│
│            │    │           │    │            │    │             │
└────────────┘    └───────────┘    └────────────┘    └─────────────┘
      │                  │               │                │
      │                  │               │                │
      ▼                  ▼               ▼                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐
│ Local Files │  │ Text        │  │ Algorithm   │  │ Similarity      │
│ Web Sources │  │ Normalization│ │ Selection      │ Matrix Display  │
│ Databases   │  │ Tokenization│  │ (TF-IDF vs  │  │ Top Pairs Report│
│             │  │ Stopword    │  │ MinHash)    │  │ Interactive     │
└─────────────┘  │ Removal     │  │             │  │ Comparison      │
                 └─────────────┘  └─────────────┘  └─────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                             DATA FLOW                              │
└────────────────────────────────────────────────────────────────────┘

1. INPUT PHASE:
   - Documents ingested from multiple sources
   - Supported formats: raw text, files, web URLs

2. PROCESSING PHASE:
   ┌───────────────┐     ┌───────────────┐     ┌────────────────┐
   │ Batch Mode    │     │ Stream Mode   │     │ On-Demand      │
   │ (Process      │     │ (Continuous   │     │ (Single        │
   │ collections)  │     │ monitoring)   │     │ comparisons)   │
   └───────────────┘     └───────────────┘     └────────────────┘

3. ALGORITHM SELECTION:
   ┌───────────────────────────────┐    ┌────────────────────────────┐
   │ TF-IDF + Cosine Similarity    │    │ MinHash + LSH              │
   ├───────────────────────────────┤    ├────────────────────────────┤
   │ - Higher accuracy             │    │ - Faster for large dataset │
   │ - Better for small collections│    │ - Approximate results      │
   │ - O(n²) complexity            │    │ - O(n) query complexity    │
   └───────────────────────────────┘    └────────────────────────────┘

4. OUTPUT PHASE:
   - Similarity scores (0-1) between documents
   - Identification of duplicate/near-duplicate documents
   - Visualization of document clusters

┌─────────────────────────────────────────────────────────────────────┐
│                SCALABILITY CONSIDERATIONS                           │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐    ┌─────────────┐    ┌─────────────┐    ┌────────────┐
│ Distributed  │    │ Caching     │    │ Load        │    │ Horizontal │
│ Processing   │    │ Layer       │    │ Balancing   │    │ Scaling    │
│ (Spark,      │    │ (Redis)     │    │             │    │            │
│ Hadoop)      │    │             │    │             │    │            │
└──────────────┘    └─────────────┘    └─────────────┘    └────────────┘

Key Decision Points:
1. Document Volume → Algorithm Selection
2. Latency Requirements → Processing Mode
3. Accuracy Needs → TF-IDF vs MinHash tuning
4. Resource Constraints → Scaling approach