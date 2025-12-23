import pandas as pd
import numpy as np
from typing import List, Tuple, Dict
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    USE_ADVANCED = True
except ImportError:
    USE_ADVANCED = False
    print("Using basic TF-IDF retrieval (sentence-transformers not available)")

class MedicalRetriever:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.qa_data = None
        self.use_advanced = USE_ADVANCED
        
        if self.use_advanced:
            self.model = SentenceTransformer(model_name)
            self.index = None
            self.embeddings = None
        else:
            self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
            self.tfidf_matrix = None
        
    def build_index(self, qa_df: pd.DataFrame, save_path: str = "data/retrieval_index"):
        """Build search index from Q&A data"""
        self.qa_data = qa_df
        questions = qa_df['question'].tolist()
        
        if self.use_advanced:
            return self._build_faiss_index(questions, save_path)
        else:
            return self._build_tfidf_index(questions, save_path)
    
    def _build_faiss_index(self, questions, save_path):
        """Build FAISS index"""
        print("Creating embeddings...")
        self.embeddings = self.model.encode(questions, show_progress_bar=True)
        
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        
        faiss.normalize_L2(self.embeddings)
        self.index.add(self.embeddings.astype('float32'))
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        faiss.write_index(self.index, f"{save_path}.faiss")
        
        with open(f"{save_path}.pkl", 'wb') as f:
            pickle.dump({
                'qa_data': self.qa_data,
                'embeddings': self.embeddings
            }, f)
        
        print(f"FAISS index built with {len(questions)} questions")
    
    def _build_tfidf_index(self, questions, save_path):
        """Build TF-IDF index"""
        print("Creating TF-IDF vectors...")
        self.tfidf_matrix = self.vectorizer.fit_transform(questions)
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(f"{save_path}_tfidf.pkl", 'wb') as f:
            pickle.dump({
                'qa_data': self.qa_data,
                'vectorizer': self.vectorizer,
                'tfidf_matrix': self.tfidf_matrix
            }, f)
        
        print(f"TF-IDF index built with {len(questions)} questions")
    
    def load_index(self, save_path: str = "data/retrieval_index"):
        """Load pre-built index"""
        try:
            if self.use_advanced and os.path.exists(f"{save_path}.faiss"):
                return self._load_faiss_index(save_path)
            elif os.path.exists(f"{save_path}_tfidf.pkl"):
                return self._load_tfidf_index(save_path)
            else:
                return False
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def _load_faiss_index(self, save_path):
        """Load FAISS index"""
        self.index = faiss.read_index(f"{save_path}.faiss")
        
        with open(f"{save_path}.pkl", 'rb') as f:
            data = pickle.load(f)
            self.qa_data = data['qa_data']
            self.embeddings = data['embeddings']
        
        print("FAISS index loaded successfully")
        return True
    
    def _load_tfidf_index(self, save_path):
        """Load TF-IDF index"""
        with open(f"{save_path}_tfidf.pkl", 'rb') as f:
            data = pickle.load(f)
            self.qa_data = data['qa_data']
            self.vectorizer = data['vectorizer']
            self.tfidf_matrix = data['tfidf_matrix']
        
        print("TF-IDF index loaded successfully")
        return True
    
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve most relevant Q&A pairs"""
        if self.qa_data is None:
            return []
        
        if self.use_advanced and self.index is not None:
            return self._retrieve_faiss(query, top_k)
        elif self.tfidf_matrix is not None:
            return self._retrieve_tfidf(query, top_k)
        else:
            return []
    
    def _retrieve_faiss(self, query, top_k):
        """Retrieve using FAISS"""
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx < len(self.qa_data):
                result = {
                    'question': self.qa_data.iloc[idx]['question'],
                    'answer': self.qa_data.iloc[idx]['answer'],
                    'source': self.qa_data.iloc[idx]['source'],
                    'score': float(score),
                    'rank': i + 1
                }
                results.append(result)
        
        return results
    
    def _retrieve_tfidf(self, query, top_k):
        """Retrieve using TF-IDF"""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        results = []
        for i, idx in enumerate(top_indices):
            if similarities[idx] > 0:
                result = {
                    'question': self.qa_data.iloc[idx]['question'],
                    'answer': self.qa_data.iloc[idx]['answer'],
                    'source': self.qa_data.iloc[idx]['source'],
                    'score': float(similarities[idx]),
                    'rank': i + 1
                }
                results.append(result)
        
        return results
    
    def get_best_answer(self, query: str, threshold: float = 0.3) -> Dict:
        """Get the best answer for a query"""
        results = self.retrieve(query, top_k=1)
        
        if results and results[0]['score'] >= threshold:
            return results[0]
        else:
            return {
                'question': query,
                'answer': "I'm sorry, I couldn't find a relevant answer to your question. Please consult with a healthcare professional for medical advice.",
                'source': 'fallback',
                'score': 0.0,
                'rank': 0
            }