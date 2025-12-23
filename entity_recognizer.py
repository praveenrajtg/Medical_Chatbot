import re
from typing import List, Dict, Set
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class MedicalEntityRecognizer:
    def __init__(self):
        self._download_nltk_data()
        self.medical_entities = self._load_medical_entities()
        self.stop_words = set(stopwords.words('english'))
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
    
    def _load_medical_entities(self) -> Dict[str, Set[str]]:
        """Load predefined medical entities"""
        return {
            'symptoms': {
                'fever', 'headache', 'cough', 'fatigue', 'nausea', 'vomiting', 'diarrhea',
                'chest pain', 'shortness of breath', 'dizziness', 'weakness', 'pain',
                'swelling', 'rash', 'itching', 'bleeding', 'numbness', 'tingling',
                'blurred vision', 'difficulty breathing', 'abdominal pain', 'back pain',
                'joint pain', 'muscle pain', 'sore throat', 'runny nose', 'congestion'
            },
            'diseases': {
                'diabetes', 'hypertension', 'asthma', 'cancer', 'heart disease',
                'stroke', 'pneumonia', 'bronchitis', 'arthritis', 'osteoporosis',
                'depression', 'anxiety', 'migraine', 'epilepsy', 'alzheimer',
                'parkinson', 'tuberculosis', 'hepatitis', 'kidney disease',
                'liver disease', 'thyroid disorder', 'anemia', 'obesity'
            },
            'treatments': {
                'medication', 'surgery', 'therapy', 'exercise', 'diet', 'rest',
                'antibiotics', 'insulin', 'chemotherapy', 'radiation', 'physical therapy',
                'counseling', 'vaccination', 'immunization', 'prescription',
                'over-the-counter', 'treatment', 'procedure', 'operation'
            }
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract medical entities from text"""
        text_lower = text.lower()
        tokens = word_tokenize(text_lower)
        tokens = [token for token in tokens if token not in self.stop_words and token.isalpha()]
        
        entities = {
            'symptoms': [],
            'diseases': [],
            'treatments': []
        }
        
        # Extract entities by matching tokens and phrases
        for entity_type, entity_set in self.medical_entities.items():
            for entity in entity_set:
                if entity in text_lower:
                    entities[entity_type].append(entity)
        
        # Remove duplicates
        for entity_type in entities:
            entities[entity_type] = list(set(entities[entity_type]))
        
        return entities
    
    def get_entity_context(self, text: str, entity: str, window: int = 5) -> str:
        """Get context around a medical entity"""
        tokens = word_tokenize(text.lower())
        entity_tokens = word_tokenize(entity.lower())
        
        for i in range(len(tokens) - len(entity_tokens) + 1):
            if tokens[i:i+len(entity_tokens)] == entity_tokens:
                start = max(0, i - window)
                end = min(len(tokens), i + len(entity_tokens) + window)
                return ' '.join(tokens[start:end])
        
        return ""