"""
Test script to verify StudySphere AI setup
Run this before starting the main app
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    
    required_packages = [
        ('streamlit', 'Streamlit'),
        ('dotenv', 'python-dotenv'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('pptx', 'python-pptx'),
        ('pytesseract', 'pytesseract'),
        ('PIL', 'Pillow'),
        ('chromadb', 'chromadb'),
        ('sentence_transformers', 'sentence-transformers'),
        ('torch', 'torch'),
        ('google.generativeai', 'google-generativeai'),
        ('pyttsx3', 'pyttsx3'),
        ('pyperclip', 'pyperclip')
    ]
    
    failed = []
    for package, pip_name in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {pip_name}")
        except ImportError:
            print(f"  ❌ {pip_name} - NOT INSTALLED")
            failed.append(pip_name)
    
    if failed:
        print(f"\n⚠️  Missing packages: {', '.join(failed)}")
        print(f"Install with: pip install {' '.join(failed)}")
        return False
    
    print("\n✅ All packages installed!")
    return True


def test_env_file():
    """Test if .env file exists and has API key"""
    print("\n🔍 Testing .env configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.path.exists('.env'):
        print("  ❌ .env file not found!")
        print("  Create a .env file with: GEMINI_API_KEY=your_key_here")
        return False
    
    print("  ✅ .env file exists")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  ❌ GEMINI_API_KEY not set in .env")
        print("  Add to .env: GEMINI_API_KEY=your_key_here")
        return False
    
    print(f"  ✅ API key found (starts with: {api_key[:10]}...)")
    return True


def test_tesseract():
    """Test if Tesseract OCR is available"""
    print("\n🔍 Testing Tesseract OCR...")
    
    import pytesseract
    from PIL import Image
    import io
    
    # Set tesseract path if in env
    tesseract_path = os.getenv("TESSERACT_CMD")
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        print(f"  ℹ️  Using Tesseract from: {tesseract_path}")
    
    try:
        # Create a simple test image
        version = pytesseract.get_tesseract_version()
        print(f"  ✅ Tesseract version: {version}")
        return True
    except Exception as e:
        print(f"  ❌ Tesseract not found: {e}")
        print("  Install from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("  Or set path in .env: TESSERACT_CMD=path/to/tesseract.exe")
        return False


def test_gemini_api():
    """Test if Gemini API is working"""
    print("\n🔍 Testing Gemini API connection...")
    
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("  ❌ API key not found")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = model.generate_content("Say 'Hello'")
        print(f"  ✅ API working! Response: {response.text[:50]}")
        return True
        
    except Exception as e:
        print(f"  ❌ API error: {e}")
        print("  Check your API key at: https://aistudio.google.com/app/apikey")
        return False


def test_chromadb():
    """Test if ChromaDB is working"""
    print("\n🔍 Testing ChromaDB...")
    
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        
        client = chromadb.Client()
        
        # Test embedding function
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        print("  ✅ ChromaDB initialized")
        print("  ✅ Sentence transformer loaded")
        return True
        
    except Exception as e:
        print(f"  ❌ ChromaDB error: {e}")
        return False


def test_modules():
    """Test if custom modules can be imported"""
    print("\n🔍 Testing custom modules...")
    
    try:
        from modules.file_loader import FileLoader
        print("  ✅ file_loader.py")
        
        from modules.gemini_processor import GeminiProcessor
        print("  ✅ gemini_processor.py")
        
        from modules.vector_store import VectorStore
        print("  ✅ vector_store.py")
        
        from modules.rag_pipeline import RAGPipeline
        print("  ✅ rag_pipeline.py")
        
        from modules.utils import TTSManager
        print("  ✅ utils.py")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Module import error: {e}")
        print("  Make sure all module files are in the 'modules' folder")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🎓 StudySphere AI - Setup Verification")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Environment": test_env_file(),
        "Tesseract OCR": test_tesseract(),
        "Gemini API": test_gemini_api(),
        "ChromaDB": test_chromadb(),
        "Custom Modules": test_modules()
    }
    
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test:.<30} {status}")
    
    print("=" * 60)
    print(f"\nScore: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 SUCCESS! All tests passed!")
        print("You can now run: streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Create .env file with GEMINI_API_KEY")
        print("3. Install Tesseract OCR")
        print("4. Verify all module files exist in 'modules' folder")
        return 1


if __name__ == "__main__":
    sys.exit(main())