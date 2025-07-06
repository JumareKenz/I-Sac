"""
RAG-based memory system for AgentZ using ChromaDB
Stores and retrieves conversation context and business insights
"""

import os
import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from llm import AgentZLLM

class AgentZMemory:
    """Vector-based memory system for AgentZ conversations and insights"""
    
    def __init__(self, llm: AgentZLLM):
        self.llm = llm
        self.persist_directory = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Create collections
        self.conversations = self._get_or_create_collection("conversations")
        self.insights = self._get_or_create_collection("business_insights")
        self.companies = self._get_or_create_collection("companies")
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name)
        except ValueError:
            return self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def store_conversation_turn(self, 
                               user_message: str, 
                               assistant_response: str,
                               session_id: str = "default",
                               metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store a conversation turn (user message + assistant response)
        
        Args:
            user_message: User's input
            assistant_response: Assistant's response
            session_id: Conversation session identifier
            metadata: Additional metadata (tools used, topics, etc.)
        
        Returns:
            Document ID for the stored conversation turn
        """
        doc_id = str(uuid.uuid4())
        conversation_text = f"User: {user_message}\nAssistant: {assistant_response}"
        
        # Generate embedding
        try:
            embedding = self.llm.embed_query(conversation_text)
        except Exception as e:
            print(f"Failed to generate embedding: {e}")
            return doc_id
        
        # Prepare metadata
        store_metadata = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "assistant_response": assistant_response,
            "type": "conversation_turn"
        }
        
        if metadata:
            store_metadata.update(metadata)
        
        # Store in ChromaDB
        self.conversations.add(
            embeddings=[embedding],
            documents=[conversation_text],
            metadatas=[store_metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def store_business_insight(self, 
                              insight: str, 
                              category: str,
                              company: Optional[str] = None,
                              metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store a business insight or key learning
        
        Args:
            insight: The business insight or learning
            category: Category (validation, market, competition, etc.)
            company: Related company/product name
            metadata: Additional metadata
        
        Returns:
            Document ID for the stored insight
        """
        doc_id = str(uuid.uuid4())
        
        # Generate embedding
        try:
            embedding = self.llm.embed_query(insight)
        except Exception as e:
            print(f"Failed to generate embedding: {e}")
            return doc_id
        
        # Prepare metadata
        store_metadata = {
            "category": category,
            "company": company,
            "timestamp": datetime.now().isoformat(),
            "type": "business_insight"
        }
        
        if metadata:
            store_metadata.update(metadata)
        
        # Store in ChromaDB
        self.insights.add(
            embeddings=[embedding],
            documents=[insight],
            metadatas=[store_metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def store_company_profile(self, 
                             company_name: str, 
                             description: str,
                             metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store company/product profile
        
        Args:
            company_name: Name of the company/product
            description: Company description and details
            metadata: Additional metadata (industry, stage, etc.)
        
        Returns:
            Document ID for the stored company profile
        """
        doc_id = str(uuid.uuid4())
        profile_text = f"Company: {company_name}\nDescription: {description}"
        
        # Generate embedding
        try:
            embedding = self.llm.embed_query(profile_text)
        except Exception as e:
            print(f"Failed to generate embedding: {e}")
            return doc_id
        
        # Prepare metadata
        store_metadata = {
            "company_name": company_name,
            "timestamp": datetime.now().isoformat(),
            "type": "company_profile"
        }
        
        if metadata:
            store_metadata.update(metadata)
        
        # Store in ChromaDB
        self.companies.add(
            embeddings=[embedding],
            documents=[profile_text],
            metadatas=[store_metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def retrieve_relevant_context(self, 
                                 query: str, 
                                 collection_type: str = "all",
                                 limit: int = 5,
                                 session_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context based on query
        
        Args:
            query: Search query
            collection_type: Which collections to search ("conversations", "insights", "companies", "all")
            limit: Maximum number of results per collection
            session_id: Filter by session ID (for conversations)
        
        Returns:
            List of relevant context documents with metadata
        """
        results = []
        
        # Generate query embedding
        try:
            query_embedding = self.llm.embed_query(query)
        except Exception as e:
            print(f"Failed to generate query embedding: {e}")
            return results
        
        # Search conversations
        if collection_type in ["conversations", "all"]:
            try:
                where_filter = {"type": "conversation_turn"}
                if session_id:
                    where_filter["session_id"] = session_id
                
                conv_results = self.conversations.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where=where_filter
                )
                
                for i, doc in enumerate(conv_results["documents"][0]):
                    results.append({
                        "content": doc,
                        "metadata": conv_results["metadatas"][0][i],
                        "distance": conv_results["distances"][0][i],
                        "source": "conversation"
                    })
            except Exception as e:
                print(f"Error searching conversations: {e}")
        
        # Search business insights
        if collection_type in ["insights", "all"]:
            try:
                insight_results = self.insights.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where={"type": "business_insight"}
                )
                
                for i, doc in enumerate(insight_results["documents"][0]):
                    results.append({
                        "content": doc,
                        "metadata": insight_results["metadatas"][0][i],
                        "distance": insight_results["distances"][0][i],
                        "source": "insight"
                    })
            except Exception as e:
                print(f"Error searching insights: {e}")
        
        # Search company profiles
        if collection_type in ["companies", "all"]:
            try:
                company_results = self.companies.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where={"type": "company_profile"}
                )
                
                for i, doc in enumerate(company_results["documents"][0]):
                    results.append({
                        "content": doc,
                        "metadata": company_results["metadatas"][0][i],
                        "distance": company_results["distances"][0][i],
                        "source": "company"
                    })
            except Exception as e:
                print(f"Error searching companies: {e}")
        
        # Sort by relevance (distance)
        results.sort(key=lambda x: x["distance"])
        
        return results[:limit * 3]  # Return top results across all collections
    
    def get_session_history(self, 
                           session_id: str, 
                           limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get conversation history for a specific session
        
        Args:
            session_id: Session identifier
            limit: Maximum number of conversation turns to return
        
        Returns:
            List of conversation turns in chronological order
        """
        try:
            results = self.conversations.get(
                where={"session_id": session_id, "type": "conversation_turn"},
                limit=limit
            )
            
            # Sort by timestamp
            turns = []
            for i, doc in enumerate(results["documents"]):
                turn = {
                    "content": doc,
                    "metadata": results["metadatas"][i],
                    "id": results["ids"][i]
                }
                turns.append(turn)
            
            # Sort by timestamp (newest first)
            turns.sort(key=lambda x: x["metadata"]["timestamp"], reverse=True)
            
            return turns
            
        except Exception as e:
            print(f"Error retrieving session history: {e}")
            return []
    
    def clear_session(self, session_id: str) -> bool:
        """Clear all data for a specific session"""
        try:
            # Get all documents for this session
            results = self.conversations.get(
                where={"session_id": session_id}
            )
            
            if results["ids"]:
                self.conversations.delete(ids=results["ids"])
            
            return True
            
        except Exception as e:
            print(f"Error clearing session: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, int]:
        """Get memory statistics"""
        try:
            conv_count = self.conversations.count()
            insight_count = self.insights.count()
            company_count = self.companies.count()
            
            return {
                "conversations": conv_count,
                "insights": insight_count,
                "companies": company_count,
                "total": conv_count + insight_count + company_count
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {"conversations": 0, "insights": 0, "companies": 0, "total": 0}

# Factory function
def create_memory(llm: AgentZLLM) -> AgentZMemory:
    """Create and return AgentZ memory instance"""
    return AgentZMemory(llm)