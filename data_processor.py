import os
import pandas as pd
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple
import requests
import zipfile

class MedQuADProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.qa_pairs = []
        
    def download_dataset(self):
        """Download MedQuAD dataset from GitHub"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        url = "https://github.com/abachaa/MedQuAD/archive/refs/heads/master.zip"
        zip_path = os.path.join(self.data_dir, "medquad.zip")
        
        if not os.path.exists(zip_path):
            print("Downloading MedQuAD dataset...")
            response = requests.get(url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.data_dir)
            print("Dataset downloaded and extracted!")
    
    def parse_xml_files(self) -> List[Dict]:
        """Parse XML files and extract Q&A pairs"""
        qa_pairs = []
        medquad_path = os.path.join(self.data_dir, "MedQuAD-master")
        
        # Common directories in MedQuAD
        directories = [
            "1_CancerGov_QA", "2_GARD_QA", "3_GHR_QA", "4_MPlus_Health_Topics_QA",
            "5_NIDDK_QA", "6_NINDS_QA", "7_SeniorHealth_QA", "8_CancerGov_QA",
            "9_CDC_QA", "10_MPlus_ADAM_QA", "11_MPlusDrugs_QA"
        ]
        
        for directory in directories:
            dir_path = os.path.join(medquad_path, directory)
            if os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if filename.endswith('.xml'):
                        file_path = os.path.join(dir_path, filename)
                        qa_pairs.extend(self._parse_single_xml(file_path, directory))
        
        return qa_pairs
    
    def _parse_single_xml(self, file_path: str, source: str) -> List[Dict]:
        """Parse a single XML file"""
        qa_pairs = []
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            for qa in root.findall('.//QAPair'):
                question_elem = qa.find('Question')
                answer_elem = qa.find('Answer')
                
                if question_elem is not None and answer_elem is not None:
                    question = question_elem.text.strip() if question_elem.text else ""
                    answer = answer_elem.text.strip() if answer_elem.text else ""
                    
                    if question and answer:
                        qa_pairs.append({
                            'question': question,
                            'answer': answer,
                            'source': source,
                            'file': os.path.basename(file_path)
                        })
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return qa_pairs
    
    def process_dataset(self) -> pd.DataFrame:
        """Main processing function"""
        self.download_dataset()
        qa_pairs = self.parse_xml_files()
        
        if not qa_pairs:
            # Fallback sample data if download fails
            qa_pairs = self._get_sample_data()
        
        df = pd.DataFrame(qa_pairs)
        df.to_csv(os.path.join(self.data_dir, 'medquad_processed.csv'), index=False)
        print(f"Processed {len(qa_pairs)} Q&A pairs")
        return df
    
    def _get_sample_data(self) -> List[Dict]:
        """Sample medical Q&A data as fallback"""
        return [
            {
                'question': 'What is diabetes?',
                'answer': 'Diabetes is a group of metabolic disorders characterized by high blood sugar levels over a prolonged period.',
                'source': 'sample',
                'file': 'sample.xml'
            },
            {
                'question': 'What are the symptoms of hypertension?',
                'answer': 'High blood pressure often has no symptoms. Some people may experience headaches, shortness of breath, or nosebleeds.',
                'source': 'sample',
                'file': 'sample.xml'
            },
            {
                'question': 'How is asthma treated?',
                'answer': 'Asthma is treated with bronchodilators for quick relief and anti-inflammatory medications for long-term control.',
                'source': 'sample',
                'file': 'sample.xml'
            }
        ]