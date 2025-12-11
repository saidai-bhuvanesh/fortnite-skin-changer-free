"""
RAG Engine - Retrieval-Augmented Generation for personal documents
Uses ChromaDB for vector storage and semantic search
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
import sys
import hashlib

from .document_processor import DocumentProcessor

# Configure logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/rag_engine.log", rotation="10 MB")

class RAGEngine:
    """Retrieval-Augmented Generation engine for document Q&A"""
    
    def __init__(
        self,
        chroma_db_path: str = "./chroma_db",
        embedding_model: str = "all-MiniLM-L6-v2",
        collection_name: str = "personal_docs"
    ):
        """
        Initialize RAG engine
        
        Args:
            chroma_db_path: Path to ChromaDB storage
            embedding_model: Sentence transformer model name
            collection_name: ChromaDB collection name
        """
        self.chroma_db_path = Path(chroma_db_path)
        self.chroma_db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Personal documents for RAG"}
        )
        
        # Initialize embedding model
        logger.info(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # Initialize document processor
        self.doc_processor = DocumentProcessor()
        
        logger.info(f"RAG Engine initialized with {self.collection.count()} documents")
    
    def ingest_documents(
        self,
        docs_path: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ) -> Dict[str, any]:
        """
        Ingest all documents from a directory
        
        Args:
            docs_path: Path to documents directory
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            
        Returns:
            Ingestion statistics
        """
        logger.info(f"Starting document ingestion from: {docs_path}")
        
        # Process all documents
        documents = self.doc_processor.process_directory(docs_path)
        
        if not documents:
            logger.warning("No documents found to ingest")
            return {"documents_processed": 0, "chunks_created": 0, "status": "no_documents"}
        
        total_chunks = 0
        processed_docs = 0
        
        for doc in documents:
            if doc["error"]:
                logger.warning(f"Skipping {doc['metadata'].get('filename')}: {doc['error']}")
                continue
            
            # Chunk the document text
            chunks = self.doc_processor.chunk_text(
                doc["text"],
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            # Create embeddings and store
            for i, chunk in enumerate(chunks):
                # Create unique ID for chunk
                chunk_id = self._generate_chunk_id(doc["metadata"]["filename"], i)
                
                # Generate embedding
                embedding = self.embedding_model.encode(chunk).tolist()
                
                # Store in ChromaDB
                self.collection.add(
                    ids=[chunk_id],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{
                        **doc["metadata"],
                        "chunk_index": i,
                        "total_chunks": len(chunks)
                    }]
                )
            
            total_chunks += len(chunks)
            processed_docs += 1
            logger.info(f"Ingested {doc['metadata']['filename']}: {len(chunks)} chunks")
        
        result = {
            "documents_processed": processed_docs,
            "chunks_created": total_chunks,
            "status": "success"
        }
        
        logger.info(f"Ingestion complete: {result}")
        return result
    
    def query(
        self,
        query: str,
        top_k: int = 5,
        min_relevance: float = 0.3
    ) -> List[Dict[str, any]]:
        """
        Search for relevant document chunks
        
        Args:
            query: User's question
            top_k: Number of results to return
            min_relevance: Minimum relevance score (0-1)
            
        Returns:
            List of relevant chunks with metadata
        """
        if self.collection.count() == 0:
            logger.warning("No documents in collection")
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        chunks = []
        for i in range(len(results["ids"][0])):
            # Calculate relevance score (ChromaDB returns distances, convert to similarity)
            distance = results["distances"][0][i]
            relevance = 1 / (1 + distance)  # Convert distance to similarity
            
            if relevance >= min_relevance:
                chunks.append({
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "relevance": relevance
                })
        
        logger.info(f"Query returned {len(chunks)} relevant chunks")
        return chunks
    
    def answer_query(
        self,
        query: str,
        llm_chat,
        top_k: int = 5
    ) -> Dict[str, any]:
        """
        Answer a query using RAG (retrieve + generate)
        
        Args:
            query: User's question
            llm_chat: LLMChat instance for generation
            top_k: Number of chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        # Retrieve relevant chunks
        chunks = self.query(query, top_k=top_k)
        
        # If no relevant documents found, use general knowledge
        if not chunks:
            logger.info("No relevant documents found, using general knowledge")
            system_prompt = """You are Bhuvi's personal AI assistant. You're helpful, friendly, and conversational.

Answer the user's question using your general knowledge. Be:
- Conversational and natural (like talking to a friend)
- Helpful and informative
- Concise but complete
- Professional yet approachable

If the question is about you or your capabilities, explain that you're Bhuvi's AI assistant that can help with:
- Searching personal documents (RAG)
- Managing emails (Gmail)
- Creating LinkedIn content
- General questions and conversations"""
            
            answer = llm_chat.generate_response(
                query,
                system_prompt=system_prompt,
                temperature=0.7
            )
            
            return {
                "answer": answer,
                "sources": [],
                "method": "general_knowledge"
            }
        
        # Build context from chunks
        context = "\n\n".join([
            f"[Source: {chunk['metadata']['filename']}]\n{chunk['text']}"
            for chunk in chunks
        ])
        
        # Generate answer with LLM using document context
        system_prompt = f"""You are Bhuvi's personal AI assistant. Answer the question based on the context from their documents.

Be conversational and natural. If the context has the answer, use it and cite the source.
If the context doesn't fully answer the question, use what's available and supplement with general knowledge.

Context from documents:
{context}

Remember to:
- Be friendly and conversational
- Cite sources when using document information
- Supplement with general knowledge if needed"""
        
        answer = llm_chat.generate_response(
            query,
            system_prompt=system_prompt,
            temperature=0.5
        )
        
        # Extract unique sources
        sources = list(set([chunk["metadata"]["filename"] for chunk in chunks]))
        
        return {
            "answer": answer,
            "sources": sources,
            "chunks_used": len(chunks),
            "method": "rag"
        }
    
    def _generate_chunk_id(self, filename: str, chunk_index: int) -> str:
        """Generate unique ID for a document chunk"""
        id_string = f"{filename}_{chunk_index}"
        return hashlib.md5(id_string.encode()).hexdigest()
    
    def get_stats(self) -> Dict[str, any]:
        """Get collection statistics"""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection.name,
            "db_path": str(self.chroma_db_path)
        }
    
    def clear_collection(self):
        """Clear all documents from collection (use with caution!)"""
        logger.warning("Clearing all documents from RAG collection")
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"description": "Personal documents for RAG"}
        )
