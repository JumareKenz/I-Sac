"""
LLM wrapper for AgentZ using Groq for fast inference
with optional PromptLayer integration for prompt tracking
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import promptlayer

# Load environment variables
load_dotenv()

class AgentZLLM:
    """LLM wrapper for AgentZ with Groq and optional PromptLayer integration"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.promptlayer_api_key = os.getenv("PROMPTLAYER_API_KEY")
        self.enable_promptlayer = os.getenv("ENABLE_PROMPTLAYER", "false").lower() == "true"
        
        # Initialize Groq model
        self.model_name = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
        self.llm = self._initialize_groq()
        
        # Initialize OpenAI embeddings
        self.embeddings = self._initialize_embeddings()
        
        # Initialize PromptLayer if enabled
        if self.enable_promptlayer and self.promptlayer_api_key:
            promptlayer.api_key = self.promptlayer_api_key
            self.promptlayer_enabled = True
        else:
            self.promptlayer_enabled = False
    
    def _initialize_groq(self) -> ChatGroq:
        """Initialize Groq LLM"""
        if not self.groq_api_key or self.groq_api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY not set in .env file")
        
        return ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=self.model_name,
            temperature=0.7,
            max_tokens=2048,
            timeout=30,
            max_retries=2,
        )
    
    def _initialize_embeddings(self) -> OpenAIEmbeddings:
        """Initialize OpenAI embeddings"""
        if not self.openai_api_key or self.openai_api_key == "your_openai_api_key_here":
            raise ValueError("OPENAI_API_KEY not set in .env file")
        
        return OpenAIEmbeddings(
            openai_api_key=self.openai_api_key,
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        )
    
    def chat(self, 
             messages: List[Dict[str, str]], 
             temperature: float = 0.7,
             max_tokens: int = 2048,
             metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Send chat messages to the LLM and get response
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            metadata: Optional metadata for PromptLayer tracking
        
        Returns:
            String response from the LLM
        """
        # Convert message format to LangChain format
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "system":
                langchain_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
        
        # Update LLM parameters
        self.llm.temperature = temperature
        self.llm.max_tokens = max_tokens
        
        try:
            # Get response from Groq
            response = self.llm.invoke(langchain_messages)
            response_text = response.content
            
            # Track with PromptLayer if enabled
            if self.promptlayer_enabled:
                self._track_with_promptlayer(messages, response_text, metadata)
            
            return response_text
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _track_with_promptlayer(self, 
                               messages: List[Dict[str, str]], 
                               response: str, 
                               metadata: Optional[Dict[str, Any]] = None):
        """Track prompt and response with PromptLayer"""
        try:
            # Format for PromptLayer
            prompt_template = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            
            promptlayer.track.prompt(
                function_name="agentz_chat",
                prompt_name="agentz_conversation",
                prompt_input_variables={"messages": messages},
                prompt_template=prompt_template,
                prompt_version=1,
                output=response,
                metadata=metadata or {},
                tags=["agentz", "startup-advisor"]
            )
        except Exception as e:
            print(f"PromptLayer tracking failed: {e}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text list"""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return []
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for single query"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            print(f"Error embedding query: {e}")
            return []
    
    def get_model_info(self) -> Dict[str, str]:
        """Get current model configuration"""
        return {
            "llm_model": self.model_name,
            "embedding_model": os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            "promptlayer_enabled": str(self.promptlayer_enabled),
            "provider": "Groq + OpenAI"
        }

# Factory function for easy initialization
def create_llm() -> AgentZLLM:
    """Create and return AgentZ LLM instance"""
    return AgentZLLM()