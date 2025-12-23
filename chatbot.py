from data_processor import MedQuADProcessor
from entity_recognizer import MedicalEntityRecognizer
from retriever import MedicalRetriever
from typing import Dict, List
import os

class MedicalChatbot:
    def __init__(self):
        self.processor = MedQuADProcessor()
        self.entity_recognizer = MedicalEntityRecognizer()
        self.retriever = MedicalRetriever()
        self.is_initialized = False
    
    def initialize(self):
        """Initialize the chatbot by loading or creating the knowledge base"""
        print("Initializing Medical Chatbot...")
        
        # Check if processed data exists
        processed_data_path = "data/medquad_processed.csv"
        index_path = "data/retrieval_index"
        
        if os.path.exists(processed_data_path):
            print("Loading existing processed data...")
            import pandas as pd
            qa_df = pd.read_csv(processed_data_path)
        else:
            print("Processing MedQuAD dataset...")
            qa_df = self.processor.process_dataset()
        
        # Load or build retrieval index
        if not self.retriever.load_index(index_path):
            print("Building retrieval index...")
            self.retriever.build_index(qa_df, index_path)
        
        self.is_initialized = True
        print("Chatbot initialized successfully!")
    
    def get_response(self, user_question: str) -> Dict:
        """Get response for user question"""
        if not self.is_initialized:
            return {
                'answer': 'Chatbot is not initialized. Please wait...',
                'entities': {},
                'confidence': 0.0,
                'source': 'error'
            }
        
        # Extract medical entities
        entities = self.entity_recognizer.extract_entities(user_question)
        
        # Get best answer
        result = self.retriever.get_best_answer(user_question)
        
        # Enhance answer with entity information
        enhanced_answer = self._enhance_answer(result['answer'], entities)
        
        return {
            'answer': enhanced_answer,
            'entities': entities,
            'confidence': result['score'],
            'source': result['source'],
            'original_question': result['question']
        }
    
    def _enhance_answer(self, answer: str, entities: Dict) -> str:
        """Enhance answer with entity context"""
        if not any(entities.values()):
            return answer
        
        enhancement = "\n\n**Identified medical terms:**\n"
        
        for entity_type, entity_list in entities.items():
            if entity_list:
                enhancement += f"- {entity_type.title()}: {', '.join(entity_list)}\n"
        
        return answer + enhancement
    
    def get_similar_questions(self, user_question: str, top_k: int = 3) -> List[Dict]:
        """Get similar questions for user reference"""
        if not self.is_initialized:
            return []
        
        return self.retriever.retrieve(user_question, top_k)
    
    def add_disclaimer(self, response: str) -> str:
        """Add medical disclaimer to response"""
        disclaimer = "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Always consult with a healthcare provider for medical concerns."
        return response + disclaimer