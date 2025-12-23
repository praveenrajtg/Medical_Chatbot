import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        # Install packages one by one to avoid conflicts
        packages = [
            "streamlit", "pandas", "numpy", "scikit-learn", 
            "nltk", "requests", "beautifulsoup4", 
            "sentence-transformers", "faiss-cpu"
        ]
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        print("Trying alternative installation...")
        # Fallback: install without version constraints
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--no-deps"])

def download_nltk_data():
    """Download NLTK data"""
    try:
        import nltk
        print("Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK data downloaded successfully!")
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")

def create_directories():
    """Create necessary directories"""
    directories = ["data"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main setup function"""
    print("Setting up Medical Q&A Chatbot...")
    print("=" * 50)
    
    try:
        create_directories()
        install_requirements()
        download_nltk_data()
        
        print("\n" + "=" * 50)
        print("Setup completed successfully!")
        print("\nTo run the chatbot:")
        print("streamlit run app.py")
        print("\nNote: First run will take longer as it downloads the MedQuAD dataset.")
        
    except Exception as e:
        print(f"Setup failed: {e}")
        print("Please try manual installation:")
        print("pip install streamlit pandas numpy scikit-learn nltk requests beautifulsoup4 sentence-transformers faiss-cpu")

if __name__ == "__main__":
    main()