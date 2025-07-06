"""
AgentZ - AI Co-founder Assistant
Main application loop orchestrating LLM, memory, tools, and user interaction
"""

import os
import sys
import signal
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Import AgentZ components
from llm import create_llm, AgentZLLM
from memory import create_memory, AgentZMemory
from tools import create_tools, AgentZTools
from utils import get_formatter, get_validator, get_utils
from prompts import (
    SYSTEM_PROMPT, IDEA_VALIDATION_PROMPT, MARKET_RESEARCH_PROMPT,
    COMPETITOR_ANALYSIS_PROMPT, REFLECTION_PROMPT, get_context_prompt
)

# Load environment variables
load_dotenv()

class AgentZ:
    """Main AgentZ application class"""
    
    def __init__(self):
        """Initialize AgentZ with all components"""
        self.formatter = get_formatter()
        self.validator = get_validator()
        self.utils = get_utils()
        
        # Initialize session
        self.session_id = self.utils.generate_session_id()
        self.conversation_history = []
        
        # Initialize components
        self.llm: Optional[AgentZLLM] = None
        self.memory: Optional[AgentZMemory] = None
        self.tools: Optional[AgentZTools] = None
        
        # State tracking
        self.context_limit = 10  # Number of conversation turns to keep in context
        self.last_tool_used = None
        self.business_context = {}  # Track business entities mentioned
        
    def initialize(self) -> bool:
        """Initialize all AgentZ components"""
        try:
            # Validate API keys
            api_validation = self.validator.validate_api_keys()
            
            if not api_validation.get("groq"):
                self.formatter.format_error("Groq API key not found or invalid. Please set GROQ_API_KEY in .env file.")
                return False
            
            if not api_validation.get("openai"):
                self.formatter.format_error("OpenAI API key not found or invalid. Please set OPENAI_API_KEY in .env file.")
                return False
            
            # Initialize LLM
            self.formatter.format_info("Initializing AgentZ components...")
            self.llm = create_llm()
            
            # Initialize memory with LLM
            self.memory = create_memory(self.llm)
            
            # Initialize tools
            self.tools = create_tools()
            
            # Test LLM connection
            test_response = self.llm.chat([
                {"role": "system", "content": "You are AgentZ. Respond with 'AgentZ initialized successfully.'"},
                {"role": "user", "content": "Test connection"}
            ])
            
            if "error" in test_response.lower():
                self.formatter.format_error(f"LLM initialization failed: {test_response}")
                return False
            
            self.formatter.format_success("AgentZ initialized successfully!")
            return True
            
        except Exception as e:
            self.formatter.format_error(f"Initialization failed: {str(e)}")
            return False
    
    def run(self):
        """Main application loop"""
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Initialize components
        if not self.initialize():
            return
        
        # Show welcome message
        self.formatter.print_welcome()
        
        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Parse command or message
                parsed = self.utils.parse_command(user_input)
                
                if parsed["is_command"]:
                    # Handle commands
                    if not self._handle_command(parsed["command"], parsed.get("args", "")):
                        break
                else:
                    # Handle regular conversation
                    if self.validator.validate_input(parsed["message"]):
                        self._handle_conversation(parsed["message"])
                    else:
                        self.formatter.format_error("Please provide a valid message.")
                        
            except KeyboardInterrupt:
                print("\n")
                self._graceful_shutdown()
                break
            except EOFError:
                print("\n")
                self._graceful_shutdown()
                break
            except Exception as e:
                self.formatter.format_error(f"Unexpected error: {str(e)}")
    
    def _handle_command(self, command: str, args: str) -> bool:
        """Handle user commands"""
        if command == "exit" or command == "quit":
            self._graceful_shutdown()
            return False
        
        elif command == "help":
            self._show_help()
        
        elif command == "tools":
            self._show_tools()
        
        elif command == "memory":
            self._show_memory_stats()
        
        elif command == "clear":
            self._clear_session()
        
        elif command == "config":
            self._show_config()
        
        elif command == "research":
            if args:
                self._quick_research(args)
            else:
                self.formatter.format_error("Please specify what to research. Example: /research market analysis for SaaS")
        
        else:
            self.formatter.format_error(f"Unknown command: {command}. Type /help for available commands.")
        
        return True
    
    def _handle_conversation(self, user_message: str):
        """Handle regular conversation with AI"""
        with self.formatter.print_thinking() as progress:
            progress.add_task(description="Thinking...", total=None)
            
            # Extract business entities
            entities = self.validator.extract_business_entities(user_message)
            self.business_context.update(entities)
            
            # Retrieve relevant context from memory
            relevant_context = []
            if self.memory:
                relevant_context = self.memory.retrieve_relevant_context(
                    user_message, 
                    session_id=self.session_id,
                    limit=3
                )
            
            # Determine if tools should be used
            tool_results = self._determine_and_execute_tools(user_message)
            
            # Build conversation messages
            messages = self._build_conversation_messages(
                user_message, 
                relevant_context, 
                tool_results
            )
            
            # Get AI response
            response = self.llm.chat(
                messages,
                metadata={
                    "session_id": self.session_id,
                    "tools_used": [self.last_tool_used] if self.last_tool_used else [],
                    "entities": entities
                }
            )
        
        # Format and display response
        self.formatter.format_response(response)
        
        # Store conversation in memory
        if self.memory:
            self.memory.store_conversation_turn(
                user_message,
                response,
                self.session_id,
                {
                    "tools_used": [self.last_tool_used] if self.last_tool_used else [],
                    "entities": entities
                }
            )
        
        # Update conversation history
        self.conversation_history.append({
            "user": user_message,
            "assistant": response,
            "timestamp": self.utils.format_timestamp()
        })
        
        # Keep only recent conversation history
        if len(self.conversation_history) > self.context_limit:
            self.conversation_history = self.conversation_history[-self.context_limit:]
        
        # Reset tool state
        self.last_tool_used = None
    
    def _determine_and_execute_tools(self, user_message: str) -> Dict[str, Any]:
        """Determine if tools should be used and execute them"""
        tool_results = {}
        
        if not self.tools:
            return tool_results
        
        message_lower = user_message.lower()
        
        # Market research triggers
        if any(trigger in message_lower for trigger in [
            "market size", "market research", "market analysis", "tam", "sam", "som",
            "market opportunity", "industry analysis", "market trends"
        ]):
            # Extract market and product info
            entities = self.validator.extract_business_entities(user_message)
            market = entities.get("markets", ["general"])[0] if entities.get("markets") else "general"
            product = "product" if not entities.get("companies") else entities.get("companies")[0]
            
            result = self.tools.execute_tool(
                "market_research",
                market=market,
                product=product
            )
            tool_results["market_research"] = result
            self.last_tool_used = "market_research"
        
        # Competitor analysis triggers
        elif any(trigger in message_lower for trigger in [
            "competitor", "competition", "competitive analysis", "market leaders",
            "alternatives", "similar products", "compare"
        ]):
            entities = self.validator.extract_business_entities(user_message)
            market = entities.get("markets", ["general"])[0] if entities.get("markets") else "general"
            product = "product" if not entities.get("companies") else entities.get("companies")[0]
            
            result = self.tools.execute_tool(
                "competitor_analysis",
                market=market,
                product=product
            )
            tool_results["competitor_analysis"] = result
            self.last_tool_used = "competitor_analysis"
        
        # Idea validation triggers
        elif any(trigger in message_lower for trigger in [
            "validate", "validation", "viable", "good idea", "worth pursuing",
            "should i build", "potential", "feasible"
        ]):
            result = self.tools.execute_tool(
                "idea_validation",
                idea=user_message,
                market=self.business_context.get("markets", ["general"])[0] if self.business_context.get("markets") else "general",
                target_customer="entrepreneurs"
            )
            tool_results["idea_validation"] = result
            self.last_tool_used = "idea_validation"
        
        return tool_results
    
    def _build_conversation_messages(self, 
                                   user_message: str, 
                                   relevant_context: List[Dict], 
                                   tool_results: Dict[str, Any]) -> List[Dict[str, str]]:
        """Build conversation messages for LLM"""
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add relevant context from memory
        if relevant_context:
            context_text = "Previous relevant context:\n"
            for ctx in relevant_context[:3]:  # Top 3 most relevant
                context_text += f"- {ctx['content'][:200]}...\n"
            
            messages.append({
                "role": "system", 
                "content": f"Context from previous conversations:\n{context_text}"
            })
        
        # Add recent conversation history
        for turn in self.conversation_history[-3:]:  # Last 3 turns
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["assistant"]})
        
        # Add tool results if any
        if tool_results:
            tool_summary = "Research results:\n"
            for tool_name, result in tool_results.items():
                formatted_result = self.formatter.format_tool_result(tool_name, result)
                tool_summary += f"\n{formatted_result}\n"
            
            messages.append({
                "role": "system",
                "content": f"Use this research data to inform your response:\n{tool_summary}"
            })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _show_help(self):
        """Show help information"""
        help_text = """
## 🤖 AgentZ Commands

**Conversation Commands:**
- Just type your business question or idea
- `/research <topic>` - Quick research on any business topic

**Utility Commands:**
- `/tools` - Show available research tools
- `/memory` - Show memory statistics
- `/clear` - Clear conversation history for this session
- `/config` - Show current configuration
- `/help` - Show this help message
- `/exit` or `/quit` - Exit AgentZ

**Example Questions:**
- "I have an idea for a SaaS tool for project management. Is this viable?"
- "What's the market size for e-commerce platforms?"
- "Who are the main competitors in the fintech space?"
- "Help me validate my business idea for a mobile app"
        """
        self.formatter.format_response(help_text, "Help")
    
    def _show_tools(self):
        """Show available research tools"""
        if self.tools:
            tools = self.tools.get_available_tools()
            self.formatter.format_tools_list(tools)
        else:
            self.formatter.format_error("Tools not initialized")
    
    def _show_memory_stats(self):
        """Show memory statistics"""
        if self.memory:
            stats = self.memory.get_statistics()
            self.formatter.format_memory_stats(stats)
        else:
            self.formatter.format_error("Memory not initialized")
    
    def _show_config(self):
        """Show current configuration"""
        if self.llm:
            config = self.llm.get_model_info()
            config_text = f"""
## ⚙️ AgentZ Configuration

**Session ID:** {self.session_id}
**LLM Model:** {config.get('llm_model', 'Unknown')}
**Embedding Model:** {config.get('embedding_model', 'Unknown')}
**PromptLayer:** {config.get('promptlayer_enabled', 'False')}
**Memory:** {'Enabled' if self.memory else 'Disabled'}
**Tools:** {'Enabled' if self.tools else 'Disabled'}
**Context Limit:** {self.context_limit} turns
            """
            self.formatter.format_response(config_text, "Configuration")
        else:
            self.formatter.format_error("Components not initialized")
    
    def _clear_session(self):
        """Clear current session"""
        if self.memory:
            success = self.memory.clear_session(self.session_id)
            if success:
                self.formatter.format_success("Session cleared successfully")
            else:
                self.formatter.format_error("Failed to clear session")
        
        # Clear local history
        self.conversation_history = []
        self.business_context = {}
        
        # Generate new session ID
        self.session_id = self.utils.generate_session_id()
        self.formatter.format_info(f"New session started: {self.session_id}")
    
    def _quick_research(self, topic: str):
        """Quick research on any topic"""
        with self.formatter.print_thinking() as progress:
            progress.add_task(description="Researching...", total=None)
            
            # Determine appropriate tool based on topic
            topic_lower = topic.lower()
            
            if "market" in topic_lower:
                result = self.tools.execute_tool("market_research", market=topic, product="general")
                formatted = self.formatter.format_tool_result("market_research", result)
            elif "competitor" in topic_lower:
                result = self.tools.execute_tool("competitor_analysis", market=topic, product="general")
                formatted = self.formatter.format_tool_result("competitor_analysis", result)
            else:
                result = self.tools.execute_tool("idea_validation", idea=topic, market="general", target_customer="general")
                formatted = self.formatter.format_tool_result("idea_validation", result)
        
        self.formatter.format_response(formatted, "Research Results")
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        print("\n")
        self.formatter.format_info("Received shutdown signal...")
        self._graceful_shutdown()
        sys.exit(0)
    
    def _graceful_shutdown(self):
        """Gracefully shutdown AgentZ"""
        self.formatter.format_info("Shutting down AgentZ...")
        
        # Could add cleanup logic here if needed
        # - Save session data
        # - Close database connections
        # - etc.
        
        self.formatter.format_success("Thanks for using AgentZ! Build something amazing! 🚀")

def main():
    """Main entry point"""
    try:
        # Create and run AgentZ
        agentz = AgentZ()
        agentz.run()
        
    except Exception as e:
        print(f"❌ Failed to start AgentZ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()