# Medical_Chatbot
# Medical Q&A Chatbot 🏥

A specialized medical question-answering chatbot using the MedQuAD dataset with semantic search, medical entity recognition, and an interactive Streamlit interface.

## Features

- ✅ **Semantic Search**: Uses sentence transformers and FAISS for accurate answer retrieval
- ✅ **Medical Entity Recognition**: Identifies symptoms, diseases, and treatments
- ✅ **MedQuAD Dataset**: Comprehensive medical Q&A from trusted sources
- ✅ **Interactive UI**: Clean Streamlit interface with chat history
- ✅ **Confidence Scoring**: Shows relevance scores for answers
- ✅ **Source Attribution**: Tracks answer sources

## Prerequisites

- Python 3.8 or higher
- Internet connection (for first-time setup)
- 2GB free disk space

## Step-by-Step Installation Guide

### Step 1: Clone or Download the Project

If you haven't already, ensure all project files are in your directory:
```
medical_chatbot/
├── app.py
├── chatbot.py
├── data_processor.py
├── entity_recognizer.py
├── retriever.py
├── setup.py
├── requirements.txt
└── README.md
```

### Step 2: Create Virtual Environment (Recommended)

Open Command Prompt or PowerShell in the project directory:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Run Setup Script

```bash
python setup.py
```

This will:
- Install all required packages
- Download necessary NLTK data
- Download spaCy model
- Create required directories

**Alternative Manual Installation:**

If setup.py fails, install manually:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords
```

### Step 4: Run the Chatbot

```bash
streamlit run app.py
```

The application will:
1. Open in your default browser (usually at http://localhost:8501)
2. Download the MedQuAD dataset on first run (may take 2-5 minutes)
3. Process the dataset and build the search index
4. Display the chat interface

## Usage Guide

### Asking Questions

1. Type your medical question in the chat input box
2. Press Enter or click Send
3. The chatbot will:
   - Find the most relevant answer
   - Identify medical entities (symptoms, diseases, treatments)
   - Show confidence score and source

### Example Questions

- "What is diabetes?"
- "What are the symptoms of hypertension?"
- "How is asthma treated?"
- "What causes heart disease?"
- "What are the side effects of chemotherapy?"

### Sidebar Settings

- **Show Medical Entities**: Toggle entity recognition display
- **Show Similar Questions**: Display related questions
- **Confidence Threshold**: Adjust minimum confidence for answers (0.0-1.0)

## Project Structure

```
medical_chatbot/
├── app.py                  # Streamlit UI
├── chatbot.py             # Main chatbot logic
├── data_processor.py      # MedQuAD dataset processing
├── entity_recognizer.py   # Medical entity recognition
├── retriever.py           # Semantic search with FAISS
├── setup.py               # Installation script
├── requirements.txt       # Python dependencies
├── data/                  # Dataset and processed files
│   ├── MedQuAD-master/   # Downloaded dataset
│   ├── medquad_processed.csv
│   ├── retrieval_index.faiss
│   └── retrieval_index.pkl
└── README.md
```

## Technical Details

### Components

1. **Data Processor** (`data_processor.py`)
   - Downloads MedQuAD dataset from GitHub
   - Parses XML files
   - Extracts Q&A pairs
   - Creates structured CSV

2. **Entity Recognizer** (`entity_recognizer.py`)
   - Uses NLTK for tokenization
   - Pattern matching for medical terms
   - Categorizes: symptoms, diseases, treatments

3. **Retriever** (`retriever.py`)
   - Sentence-BERT embeddings (all-MiniLM-L6-v2)
   - FAISS index for fast similarity search
   - Cosine similarity scoring

4. **Chatbot** (`chatbot.py`)
   - Integrates all components
   - Manages conversation flow
   - Adds medical disclaimers

5. **Streamlit App** (`app.py`)
   - User interface
   - Chat history
   - Settings and controls

### Technologies Used

- **Streamlit**: Web interface
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **NLTK**: Natural language processing
- **Pandas**: Data manipulation
- **spaCy**: Advanced NLP (optional)

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Dataset download fails

**Solution:**
- Check internet connection
- Manually download from: https://github.com/abachaa/MedQuAD
- Extract to `data/MedQuAD-master/`

### Issue: NLTK data not found

**Solution:**
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### Issue: Streamlit won't start

**Solution:**
```bash
# Check if port 8501 is in use
streamlit run app.py --server.port 8502
```

### Issue: Slow first run

**Solution:**
- First run downloads dataset and builds index (2-5 minutes)
- Subsequent runs are much faster (cached)

## Performance Optimization

- **First Run**: 2-5 minutes (dataset download + indexing)
- **Subsequent Runs**: 10-30 seconds (loads cached index)
- **Query Response**: < 1 second

## Limitations

- Educational purposes only - not a substitute for medical advice
- Limited to MedQuAD dataset knowledge
- English language only
- Basic entity recognition (can be enhanced with medical NER models)

## Future Enhancements

- [ ] Add medical NER with BioBERT
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with medical APIs
- [ ] User feedback mechanism
- [ ] Export chat history

## Dataset Information

**MedQuAD** (Medical Question Answering Dataset)
- Source: https://github.com/abachaa/MedQuAD
- Contains: 47,457 medical Q&A pairs
- Sources: NIH, CDC, Cancer.gov, and more
- License: Public domain

## Medical Disclaimer

⚠️ **IMPORTANT**: This chatbot provides educational information only and should not replace professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.

## License

This project is for educational purposes. The MedQuAD dataset is in the public domain.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Check internet connection for first run

## Credits

- **MedQuAD Dataset**: Asma Ben Abacha and Dina Demner-Fushman
- **Sentence Transformers**: UKPLab
- **FAISS**: Facebook AI Research
- **Streamlit**: Streamlit Inc.

---

**Built with ❤️ for medical education and research**
