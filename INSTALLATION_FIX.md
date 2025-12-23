# Quick Installation Fix

## The Error You're Seeing

The error is related to setuptools and numpy version compatibility. Here's the fix:

## Solution 1: Manual Installation (Recommended)

Run these commands one by one in your activated virtual environment:

```bash
# 1. Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# 2. Install packages individually
pip install streamlit
pip install pandas
pip install numpy
pip install scikit-learn
pip install nltk
pip install requests
pip install beautifulsoup4
pip install sentence-transformers
pip install faiss-cpu

# 3. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 4. Run the chatbot
streamlit run app.py
```

## Solution 2: Use Updated Setup Script

```bash
python setup.py
```

The setup.py has been updated to handle the error better.

## Solution 3: Quick One-Liner

```bash
python -m pip install --upgrade pip setuptools wheel && pip install streamlit pandas numpy scikit-learn nltk requests beautifulsoup4 sentence-transformers faiss-cpu
```

Then run:
```bash
streamlit run app.py
```

## What Caused the Error?

- Old setuptools version couldn't build numpy from source
- Specific version constraints caused conflicts
- Solution: Use latest compatible versions

## After Installation

Once packages are installed, simply run:
```bash
streamlit run app.py
```

The app will:
1. Download MedQuAD dataset (first run only)
2. Process and index the data
3. Open in your browser

## Still Having Issues?

Try this minimal installation:
```bash
pip install --upgrade pip
pip install streamlit sentence-transformers faiss-cpu pandas nltk requests beautifulsoup4
```

This installs only the essential packages with their latest versions.