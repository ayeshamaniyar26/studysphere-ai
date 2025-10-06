from modules.file_loader import FileLoader
from modules.gemini_processor import GeminiProcessor
from modules.vector_store import VectorStore
import streamlit as st

class RAGPipeline:
    """Self-correcting RAG Pipeline"""
    
    def __init__(self):
        self.loader = FileLoader()
        self.gemini = GeminiProcessor()
        self.vector_store = VectorStore()
    
    def process_single_file(self, uploaded_file):
        """Process a single uploaded file"""
        try:
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                return self.loader.load_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self.loader.load_docx(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                return self.loader.load_pptx(uploaded_file)
            elif file_type.startswith("image/"):
                return self.loader.load_image(uploaded_file)
            elif file_type == "text/plain":
                return self.loader.load_txt(uploaded_file)
            else:
                st.warning(f"Unsupported file type: {file_type}")
                return ""
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return ""
    
    def process_multiple_files(self, uploaded_files):
        """Process multiple uploaded files"""
        return self.loader.load_multiple_files(uploaded_files)
    
    def add_to_vectorstore(self, text: str, source: str = "document"):
        """Add text to vector store for RAG"""
        if not text or not text.strip():
            st.warning("No text to add to vector store")
            return 0
        
        with st.spinner("🔄 Creating embeddings and storing chunks..."):
            num_chunks = self.vector_store.add_documents(text, source)
            if num_chunks > 0:
                st.success(f"✅ Added {num_chunks} chunks to knowledge base")
            return num_chunks
    
    def get_vectorstore_stats(self):
        """Get vector store statistics"""
        return {
            "total_chunks": self.vector_store.get_count()
        }
    
    def clear_vectorstore(self):
        """Clear the vector store"""
        return self.vector_store.clear_collection()
    
    def rag_query(self, question: str, use_self_correction: bool = True):
        """
        RAG query with optional self-correction
        1. Retrieve relevant chunks
        2. Generate initial answer
        3. (Optional) Self-correct based on retrieved context
        """
        # Step 1: Retrieve relevant context
        context = self.vector_store.rag_retrieve(question, top_k=3)
        
        if not context:
            return "❌ No relevant information found in the knowledge base. Please upload documents first."
        
        # Step 2: Generate initial answer
        initial_answer = self.gemini.tutor_mode(question, context)
        
        # Step 3: Self-correction (optional)
        if use_self_correction:
            # Retrieve more context for verification
            additional_context = self.vector_store.rag_retrieve(question, top_k=5)
            refined_answer = self.gemini.refine_answer(question, initial_answer, additional_context)
            return refined_answer
        
        return initial_answer
    
    def semantic_search(self, query: str, top_k: int = 5):
        """Perform semantic search and return results"""
        return self.vector_store.search(query, top_k=top_k)
    
    def generate_summary(self, text: str, style: str = "concise", length: int = 150):
        """Generate summary using Gemini"""
        return self.gemini.generate_summary(text, style, length)
    
    def generate_quiz(self, text: str, num_questions: int = 5, difficulty: str = "medium"):
        """Generate quiz questions"""
        return self.gemini.generate_quiz(text, num_questions, difficulty)
    
    def generate_flashcards(self, text: str, num_cards: int = 10):
        """Generate flashcards"""
        return self.gemini.generate_flashcards(text, num_cards)
    
    def explain_image_content(self, ocr_text: str):
        """Explain content extracted from image"""
        return self.gemini.explain_image(ocr_text)