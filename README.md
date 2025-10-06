# 🎓 StudySphere AI - Your 360° Learning Companion

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-Flash-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Transform any study material into powerful learning tools with AI**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation--setup) • [Usage](#-how-to-run) • [Tech Stack](#-tech-stack)

</div>

---

## 📖 About

**StudySphere AI** is an intelligent, AI-powered educational assistant that helps students study smarter, not harder. Built entirely with **free APIs** and designed to run locally, it transforms documents, images, and web content into interactive study materials including summaries, quizzes, flashcards, and more.

**⚠️ Note:** This is a **personal study tool** designed for individual use with your own Gemini API key. It uses free-tier APIs and is optimized for local deployment. Future versions may support multi-user deployment with enhanced infrastructure.

Perfect for students, educators, and lifelong learners who want to maximize their learning efficiency with cutting-edge AI technology—without paying for premium services!

---

## 🧠 **RAG Architecture**

StudySphere AI implements **advanced RAG (Retrieval-Augmented Generation)** with two modes:

### **1. Standard RAG Pipeline**
- 📚 **Document Chunking**: Splits text into 500-word chunks with 50-word overlap
- 🔢 **Embeddings**: Uses Sentence Transformers (MiniLM-L6-v2) for semantic understanding
- 🗄️ **Vector Database**: ChromaDB for efficient local storage and retrieval
- 🔍 **Semantic Search**: Natural language queries to find relevant information
- 🤖 **Context-Aware Generation**: Gemini generates answers using retrieved chunks

### **2. Self-Correcting RAG** ✨
- 🔄 **Two-Stage Retrieval**: Initial retrieval + verification retrieval
- ✅ **Answer Refinement**: AI validates and improves initial responses
- 🎯 **Higher Accuracy**: Reduces hallucinations and improves relevance
- 💡 **Toggle Feature**: Enable/disable via AI Tutor settings

**RAG Flow:**
```
Document Upload → Chunking → Embeddings → Vector DB → Query → 
Retrieval → Context → Gemini → Answer → (Optional) Self-Correction
```

---

## ✨ Features

### 📄 **Multi-Format Document Processing**
- ✅ **PDF, DOCX, PPTX, TXT** - Extract and process text from various document formats
- ✅ **Images (OCR)** - Extract text from images using Tesseract OCR
- ✅ **Multiple Files** - Batch process multiple documents at once
- ✅ **Smart Cleanup** - Remove headers, footers, and page numbers automatically

### 🤖 **AI-Powered Study Tools**
- 📝 **Smart Summaries** - Generate summaries in multiple styles (short, long, bullet points, exam-style)
- ❓ **Interactive Quizzes** - Auto-generate multiple-choice questions with explanations
- 💡 **Flashcards** - Create Q&A flashcards with progress tracking
- 🧠 **AI Tutor** - Ask questions and get intelligent answers based on your documents

### 🔍 **Advanced RAG System**
- 🎯 **Semantic Search** - Find relevant information using natural language
- 🗄️ **Vector Database** - ChromaDB for efficient document storage and retrieval
- 🔄 **Self-Correcting RAG** - Refines answers for better accuracy
- 📊 **Knowledge Base** - Build your personal study knowledge repository

### 🌐 **URL Intelligence**
- 📺 **YouTube Analysis** - Extract transcripts, detect language, and summarize videos
- 🌍 **Website Summarization** - Analyze and summarize web articles and blogs
- 🔗 **Smart Detection** - Automatically identifies content type and processes accordingly

### ⏱️ **Study Enhancement Tools**
- ⏰ **Quiz Timer** - Practice and Exam modes with countdown timers
- 🍅 **Pomodoro Timer** - 25/5 work/break sessions for focused studying
- 📊 **Progress Tracker** - Monitor your flashcard study progress
- 💡 **Daily Motivation** - Inspirational quotes to keep you motivated

### 🔊 **Audio Features**
- 🎵 **Text-to-Speech** - Listen to summaries, flashcards, and answers (powered by gTTS)
- 🔇 **Audio Controls** - Play, pause, and control audio playback

### 🎨 **User Experience**
- 🖼️ **Beautiful UI** - Modern, gradient-based design with intuitive navigation
- 🌓 **Responsive Layout** - Works seamlessly on desktop and tablet
- ⚡ **Fast Performance** - Optimized with caching and efficient processing
- 🆓 **100% Free** - No paid APIs or subscriptions required!

---

## 🧠 Tech Stack

### **Core Technologies**
| Technology | Purpose | Version |
|------------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | Backend Language | 3.8+ |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) | Web Framework | 1.31.0 |
| ![Gemini](https://img.shields.io/badge/Gemini-8E75B2?logo=google&logoColor=white) | AI Model | 2.0 Flash |

### **AI & ML Libraries**
- **Google Generative AI** - Gemini 2.0 Flash for text generation
- **ChromaDB** - Vector database for RAG
- **Sentence Transformers** - MiniLM for embeddings
- **PyTorch** - Deep learning framework

### **Document Processing**
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **python-pptx** - PowerPoint processing
- **pytesseract** - OCR for images
- **Pillow** - Image processing

### **Web & Audio**
- **gTTS** - Google Text-to-Speech
- **BeautifulSoup4** - Web scraping
- **youtube-transcript-api** - YouTube transcript extraction
- **requests** - HTTP library
- **langdetect** - Language detection

---

## ⚙️ Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- Tesseract OCR (for image processing)
- Google Gemini API key (free tier)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/studysphere-ai.git
cd studysphere-ai
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Install Tesseract OCR**

**Windows:**
1. Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Install to `C:\Program Files\Tesseract-OCR`
3. Add to PATH or set in `.env`

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### **Step 5: Get Gemini API Key**
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### **Step 6: Create `.env` File**
Create a `.env` file in the root directory:
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (only if Tesseract not in PATH)
TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### **Step 7: Run Setup Test**
```bash
python test_setup.py
```

---

## 🚀 How to Run

### **Start the Application**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### **Quick Start Guide**
1. 📤 **Upload** your study materials (PDF, DOCX, images, etc.)
2. 🧠 **Add to Knowledge Base** for RAG-powered Q&A
3. 📝 **Generate** summaries, quizzes, or flashcards
4. 🔍 **Search** your knowledge base semantically
5. 🤖 **Ask** the AI Tutor questions about your documents

---

## 📂 Folder Structure

```
studysphere-ai/
│
├── 📄 app.py                      # Main Streamlit application
├── 📋 requirements.txt            # Python dependencies
├── 📖 README.md                   # Project documentation
├── 🔧 .env                        # Environment variables (create this)
├── 🧪 test_setup.py              # Setup verification script
├── 🧪 test_gemini_models.py      # Model testing script
├── 🧪 check_models.py            # Available models checker
├── 🧪 test_ocr.py                # OCR testing script
│
├── 📁 modules/                    # Core application modules
│   ├── __init__.py               # Module initializer
│   ├── file_loader.py            # Document processing
│   ├── gemini_processor.py       # AI model interface
│   ├── rag_pipeline.py           # RAG implementation
│   ├── vector_store.py           # ChromaDB interface
│   ├── utils.py                  # Utility functions (TTS, timers, etc.)
│   ├── ocr_audio.py              # OCR and audio processing
│   └── text_processing.py        # Text manipulation
│
├── 📁 data/                       # Sample data (optional)
│   └── sample.pdf                # Example document
│
└── 📁 .streamlit/                 # Streamlit config (optional)
    └── config.toml               # Theme and settings
```

---

## 📸 Screenshots

### Dashboard
*Coming soon - Upload your screenshots here!*

### Summary Generation
*Coming soon - Upload your screenshots here!*

### Interactive Quiz
*Coming soon - Upload your screenshots here!*

### AI Tutor
*Coming soon - Upload your screenshots here!*

---

## 🎯 Use Cases

- 📚 **Students** - Summarize textbooks, create study materials, practice with quizzes
- 👨‍🏫 **Educators** - Generate teaching materials, create assessments
- 📖 **Researchers** - Analyze papers, extract key information, organize knowledge
- 💼 **Professionals** - Quick document summaries, information retrieval
- 🧠 **Lifelong Learners** - Study any topic efficiently with AI assistance

---

## 🔮 Future Improvements

- [ ] Multi-language support for non-English content
- [ ] Export study materials to PDF/DOCX
- [ ] Collaborative study sessions
- [ ] Study schedule planner with reminders
- [ ] Mobile app version
- [ ] Audio file transcription and analysis
- [ ] Integration with note-taking apps
- [ ] Spaced repetition system for flashcards
- [ ] Study analytics and insights dashboard
- [ ] Community-shared study sets
- [ ] **Multi-user deployment with API rate limiting**
- [ ] **Cloud-based vector storage for scalability**
- [ ] **Premium features with paid API integration**

---

## 🚀 Deployment Notes

### **Current Status: Personal Use**
This application is designed for **local, single-user deployment** using free-tier APIs.

**Limitations:**
- Gemini API Free Tier: 15 requests/min, 1500/day
- Local ChromaDB storage (not cloud-synced)
- Not optimized for concurrent users

**For Multi-User Deployment (Future):**
- Requires paid Gemini API with higher limits
- Needs cloud vector database (Pinecone, Weaviate)
- Rate limiting and user authentication
- Load balancing and caching strategies

**Want to use it?**
- Clone this repo
- Add your own Gemini API key
- Run locally on your machine
- Enjoy your personal AI study assistant! 🎓

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star this repository

### **How to Contribute**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **Google Gemini** - For the powerful free AI model
- **Streamlit** - For the amazing web framework
- **ChromaDB** - For the efficient vector database
- **Tesseract OCR** - For text extraction from images
- **All contributors** - For making this project better

---

## 💬 Contact & Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/studysphere-ai/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/studysphere-ai/discussions)
- 📧 **Email**: your.email@example.com
- 💼 **LinkedIn**: [Your Profile](https://linkedin.com/in/yourprofile)

---

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ by [Your Name]**

*Study smarter, not harder* 🎓

[⬆ Back to Top](#-studysphere-ai---your-360-learning-companion)

</div>