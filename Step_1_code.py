import os
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import requests
from bs4 import BeautifulSoup

class DocumentSimilarityDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents = []
        self.filenames = []
    
    def preprocess_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def load_sample_documents(self, num_documents=5):
        """Load sample documents from Project Gutenberg"""
        gutenberg_books = [
            ('The Adventures of Sherlock Holmes', 'https://www.gutenberg.org/files/1661/1661-0.txt'),
            ('Pride and Prejudice', 'https://www.gutenberg.org/files/1342/1342-0.txt'),
            ('Frankenstein', 'https://www.gutenberg.org/files/84/84-0.txt'),
            ('The Picture of Dorian Gray', 'https://www.gutenberg.org/files/174/174-0.txt'),
            ('A Tale of Two Cities', 'https://www.gutenberg.org/files/98/98-0.txt'),
            ('The Great Gatsby', 'https://www.gutenberg.org/files/64317/64317-0.txt'),
            ('Moby Dick', 'https://www.gutenberg.org/files/2701/2701-0.txt'),
            ('Alice\'s Adventures in Wonderland', 'https://www.gutenberg.org/files/11/11-0.txt')
        ]
        
        self.documents = []
        self.filenames = []
        
        for title, url in gutenberg_books[:num_documents]:
            try:
                response = requests.get(url)
                response.encoding = 'utf-8'
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                
                # Remove Gutenberg header and footer
                start = text.find("START OF THIS PROJECT GUTENBERG EBOOK")
                end = text.find("END OF THIS PROJECT GUTENBERG EBOOK")
                
                if start != -1 and end != -1:
                    text = text[start:end]
                
                # Preprocess and store
                processed_text = self.preprocess_text(text)
                self.documents.append(processed_text)
                self.filenames.append(title)
                print(f"Loaded: {title}")
            except Exception as e:
                print(f"Failed to load {title}: {str(e)}")
        
        if not self.documents:
            raise ValueError("No documents were loaded. Please check your internet connection.")
    
    def load_custom_documents(self, filepaths):
        """Load documents from local files"""
        self.documents = []
        self.filenames = []
        
        for filepath in filepaths:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    text = f.read()
                    processed_text = self.preprocess_text(text)
                    self.documents.append(processed_text)
                    self.filenames.append(os.path.basename(filepath))
            except Exception as e:
                print(f"Failed to load {filepath}: {str(e)}")
    
    def compute_similarity_matrix(self):
        """Compute pairwise similarity between all documents"""
        if not self.documents:
            raise ValueError("No documents loaded")
        
        # Vectorize documents using TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        
        # Compute cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        return similarity_matrix
    
    def get_most_similar_pairs(self, top_n=3):
        """Get the top N most similar document pairs"""
        similarity_matrix = self.compute_similarity_matrix()
        pairs = []
        
        # Get upper triangle indices without diagonal
        rows, cols = np.triu_indices(len(similarity_matrix), k=1)
        
        # Create list of (score, i, j) tuples
        for i, j in zip(rows, cols):
            score = similarity_matrix[i, j]
            pairs.append((score, i, j))
        
        # Sort by score descending
        pairs.sort(reverse=True, key=lambda x: x[0])
        
        # Prepare results
        results = []
        for score, i, j in pairs[:top_n]:
            results.append({
                'document1': self.filenames[i],
                'document2': self.filenames[j],
                'similarity_score': round(score, 4)
            })
        
        return results
    
    def compare_two_documents(self, doc1_index, doc2_index):
        """Compare two specific documents by their indices"""
        similarity_matrix = self.compute_similarity_matrix()
        score = similarity_matrix[doc1_index, doc2_index]
        
        return {
            'document1': self.filenames[doc1_index],
            'document2': self.filenames[doc2_index],
            'similarity_score': round(score, 4)
        }

def main():
    # Initialize the detector
    detector = DocumentSimilarityDetector()
    
    # Option 1: Load sample documents from Project Gutenberg
    print("Loading sample documents from Project Gutenberg...")
    detector.load_sample_documents(num_documents=5)
    
    # Option 2: Or load your own documents
    # detector.load_custom_documents(['doc1.txt', 'doc2.txt', 'doc3.txt'])
    
    # Compute and display similarity matrix
    similarity_matrix = detector.compute_similarity_matrix()
    print("\nSimilarity Matrix:")
    print(np.round(similarity_matrix, 3))
    
    # Get most similar pairs
    print("\nMost Similar Document Pairs:")
    similar_pairs = detector.get_most_similar_pairs(top_n=3)
    for pair in similar_pairs:
        print(f"{pair['document1']} vs {pair['document2']}: {pair['similarity_score']}")
    
    # Compare two specific documents
    print("\nComparing first two documents:")
    comparison = detector.compare_two_documents(0, 1)
    print(f"{comparison['document1']} vs {comparison['document2']}: {comparison['similarity_score']}")

if __name__ == "__main__":
    main()