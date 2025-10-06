import chromadb
from chromadb.utils import embedding_functions
import streamlit as st
from typing import List, Dict
import hashlib

class VectorStore:
    def __init__(self, collection_name="studysphere_docs"):
        """Initialize ChromaDB with sentence transformers"""
        self.client = chromadb.Client()
        
        # Use MiniLM for fast embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        try:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
    
    def chunk_text(self, text: str, chunk_size=500, overlap=50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def add_documents(self, text: str, source: str = "uploaded_file"):
        """Add documents to vector store with chunking"""
        try:
            chunks = self.chunk_text(text)
            
            if not chunks:
                st.warning("No text chunks created")
                return 0
            
            # Create unique IDs using hash
            ids = [hashlib.md5(f"{source}_{i}_{chunk[:50]}".encode()).hexdigest() 
                   for i, chunk in enumerate(chunks)]
            
            # Add metadata
            metadatas = [{"source": source, "chunk_id": i} for i in range(len(chunks))]
            
            # Add to collection in batches for speed
            batch_size = 100
            for i in range(0, len(chunks), batch_size):
                batch_chunks = chunks[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]
                batch_metadata = metadatas[i:i + batch_size]
                
                self.collection.add(
                    documents=batch_chunks,
                    ids=batch_ids,
                    metadatas=batch_metadata
                )
            
            return len(chunks)
        
        except Exception as e:
            st.error(f"Error adding documents: {e}")
            return 0
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Semantic search for relevant chunks"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            if not results['documents'] or not results['documents'][0]:
                return []
            
            # Format results
            formatted_results = []
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
            
            return formatted_results
        
        except Exception as e:
            st.error(f"Search error: {e}")
            return []
    
    def get_count(self) -> int:
        """Get number of chunks in collection"""
        try:
            return self.collection.count()
        except:
            return 0
    
    def clear_collection(self):
        """Clear all documents from collection"""
        try:
            # Delete and recreate collection
            self.client.delete_collection(self.collection.name)
            self.collection = self.client.create_collection(
                name=self.collection.name,
                embedding_function=self.embedding_function
            )
            return True
        except Exception as e:
            st.error(f"Error clearing collection: {e}")
            return False
    
    def rag_retrieve(self, question: str, top_k: int = 3) -> str:
        """Retrieve relevant context for RAG"""
        results = self.search(question, top_k=top_k)
        
        if not results:
            return ""
        
        # Combine top results
        context = "\n\n".join([r['content'] for r in results])
        return context