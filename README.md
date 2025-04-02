# Docuville Assignment
 
# Document Similarity Detection System - High Level Design

```mermaid
graph TD
    A[User] -->|Upload/Select Documents| B[Document Ingestion Service]
    B --> C[Document Preprocessing]
    C --> D[Algorithm Selection]
    D --> E[TF-IDF Vectorizer]
    D --> F[MinHash + LSH]
    E --> G[Similarity Calculation]
    F --> G
    G --> H[Results Storage]
    H --> I[Similarity Visualization]
    I --> A
    
    subgraph System Components
        B -->|Raw Documents| C
        C -->|Cleaned Text| D
        D -->|Algorithm Choice| E
        D -->|Algorithm Choice| F
        E -->|Document Vectors| G
        F -->|Document Hashes| G
        G -->|Similarity Scores| H
        H -->|Stored Results| I
    end

    subgraph Key Decisions
        D -->|Small Collection| E
        D -->|Large Collection| F
    end