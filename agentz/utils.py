"""
Utility functions for AgentZ
Formatting, validation, and common helper functions
"""

import re
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for cross-platform color support
colorama.init()

console = Console()

class AgentZFormatter:
    """Formatting utilities for AgentZ output"""
    
    @staticmethod
    def print_welcome():
        """Print welcome message"""
        welcome_text = """
# 🚀 Welcome to AgentZ

Your AI Co-founder Assistant for startup validation and strategy.

**Available Commands:**
- Type your business idea or question
- `/help` - Show available commands
- `/tools` - List available research tools
- `/memory` - Show memory statistics
- `/clear` - Clear conversation history
- `/exit` - Exit AgentZ

Let's build something amazing together! 💡
        """
        console.print(Panel(Markdown(welcome_text), title="AgentZ", border_style="blue"))
    
    @staticmethod
    def print_thinking():
        """Show thinking indicator"""
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        )
    
    @staticmethod
    def format_response(response: str, source: str = "AgentZ") -> None:
        """Format and print AI response"""
        console.print(f"\n[bold blue]{source}:[/bold blue]")
        console.print(Markdown(response))
        console.print()
    
    @staticmethod
    def format_tool_result(tool_name: str, result: Dict[str, Any]) -> str:
        """Format tool execution results"""
        if "error" in result:
            return f"❌ **{tool_name} Error:** {result['error']}"
        
        # Format different tool results
        if tool_name == "market_research":
            return AgentZFormatter._format_market_research(result)
        elif tool_name == "competitor_analysis":
            return AgentZFormatter._format_competitor_analysis(result)
        elif tool_name == "idea_validation":
            return AgentZFormatter._format_validation_result(result)
        else:
            return f"**{tool_name} Results:**\n```json\n{json.dumps(result, indent=2)}\n```"
    
    @staticmethod
    def _format_market_research(result: Dict[str, Any]) -> str:
        """Format market research results"""
        market_size = result.get("market_size", {})
        
        output = f"""
## 📊 Market Research Results

### Market Size
- **TAM (Total Addressable Market):** {market_size.get('tam', 'N/A')}
- **SAM (Serviceable Addressable Market):** {market_size.get('sam', 'N/A')}
- **SOM (Serviceable Obtainable Market):** {market_size.get('som', 'N/A')}
- **Growth Rate:** {market_size.get('growth_rate', 'N/A')}% annually

### Key Trends
"""
        for trend in result.get("market_trends", []):
            output += f"- {trend}\n"
        
        output += "\n### Market Barriers\n"
        for barrier in result.get("barriers_to_entry", []):
            output += f"- {barrier}\n"
        
        return output
    
    @staticmethod
    def _format_competitor_analysis(result: Dict[str, Any]) -> str:
        """Format competitor analysis results"""
        output = "## 🏁 Competitor Analysis\n\n"
        
        # Direct competitors
        output += "### Direct Competitors\n"
        for comp in result.get("direct_competitors", []):
            output += f"**{comp.get('name', 'Unknown')}**\n"
            output += f"- Position: {comp.get('market_position', 'N/A')}\n"
            output += f"- Strengths: {', '.join(comp.get('strengths', []))}\n"
            output += f"- Weaknesses: {', '.join(comp.get('weaknesses', []))}\n\n"
        
        # Competitive gaps
        output += "### Opportunities\n"
        for gap in result.get("competitive_gaps", []):
            output += f"- {gap}\n"
        
        return output
    
    @staticmethod
    def _format_validation_result(result: Dict[str, Any]) -> str:
        """Format idea validation results"""
        score = result.get("overall_score", 0)
        
        # Score interpretation
        if score >= 8.0:
            score_emoji = "🟢"
            score_text = "Strong"
        elif score >= 7.0:
            score_emoji = "🟡"
            score_text = "Good"
        else:
            score_emoji = "🔴"
            score_text = "Needs Work"
        
        output = f"""
## {score_emoji} Idea Validation Results

**Overall Score:** {score}/10 ({score_text})

### Component Scores
- **Problem Validation:** {result.get('problem_validation', {}).get('score', 'N/A')}/10
- **Market Validation:** {result.get('market_validation', {}).get('score', 'N/A')}/10
- **Solution Validation:** {result.get('solution_validation', {}).get('score', 'N/A')}/10
- **Business Model:** {result.get('business_model_validation', {}).get('score', 'N/A')}/10

### Key Recommendations
"""
        for rec in result.get("recommendations", []):
            output += f"- {rec}\n"
        
        output += "\n### Next Steps\n"
        for step in result.get("next_steps", []):
            output += f"- {step}\n"
        
        return output
    
    @staticmethod
    def format_memory_stats(stats: Dict[str, int]) -> None:
        """Format and display memory statistics"""
        table = Table(title="Memory Statistics")
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right", style="magenta")
        
        table.add_row("Conversations", str(stats.get("conversations", 0)))
        table.add_row("Business Insights", str(stats.get("insights", 0)))
        table.add_row("Company Profiles", str(stats.get("companies", 0)))
        table.add_row("Total", str(stats.get("total", 0)), style="bold")
        
        console.print(table)
    
    @staticmethod
    def format_tools_list(tools: Dict[str, str]) -> None:
        """Format and display available tools"""
        table = Table(title="Available Research Tools")
        table.add_column("Tool", style="cyan")
        table.add_column("Description", style="white")
        
        for tool_name, description in tools.items():
            table.add_row(tool_name, description)
        
        console.print(table)
    
    @staticmethod
    def format_error(error_msg: str) -> None:
        """Format and display error messages"""
        console.print(f"[bold red]❌ Error:[/bold red] {error_msg}")
    
    @staticmethod
    def format_success(success_msg: str) -> None:
        """Format and display success messages"""
        console.print(f"[bold green]✅ Success:[/bold green] {success_msg}")
    
    @staticmethod
    def format_info(info_msg: str) -> None:
        """Format and display info messages"""
        console.print(f"[bold blue]ℹ️  Info:[/bold blue] {info_msg}")

class AgentZValidator:
    """Validation utilities for AgentZ"""
    
    @staticmethod
    def validate_api_keys() -> Dict[str, bool]:
        """Validate that required API keys are set"""
        import os
        
        validation = {}
        
        # Check Groq API key
        groq_key = os.getenv("GROQ_API_KEY")
        validation["groq"] = groq_key is not None and groq_key != "your_groq_api_key_here"
        
        # Check OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        validation["openai"] = openai_key is not None and openai_key != "your_openai_api_key_here"
        
        # Check PromptLayer (optional)
        promptlayer_key = os.getenv("PROMPTLAYER_API_KEY")
        validation["promptlayer"] = promptlayer_key is not None and promptlayer_key != "your_promptlayer_api_key_here"
        
        return validation
    
    @staticmethod
    def validate_input(user_input: str) -> bool:
        """Validate user input"""
        if not user_input or user_input.strip() == "":
            return False
        
        # Check for reasonable length
        if len(user_input.strip()) < 3:
            return False
        
        return True
    
    @staticmethod
    def extract_business_entities(text: str) -> Dict[str, List[str]]:
        """Extract business entities from text"""
        # Simple keyword extraction (would use NER in production)
        companies = re.findall(r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd|Co)\b', text)
        
        # Market keywords
        market_keywords = [
            'saas', 'software', 'healthcare', 'fintech', 'e-commerce',
            'marketplace', 'platform', 'mobile app', 'web app', 'ai',
            'machine learning', 'blockchain', 'cryptocurrency'
        ]
        
        markets = []
        text_lower = text.lower()
        for keyword in market_keywords:
            if keyword in text_lower:
                markets.append(keyword)
        
        return {
            "companies": companies,
            "markets": markets
        }

class AgentZUtils:
    """General utility functions"""
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """Truncate text to specified length"""
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."
    
    @staticmethod
    def parse_command(user_input: str) -> Dict[str, Any]:
        """Parse user commands"""
        user_input = user_input.strip()
        
        if user_input.startswith('/'):
            parts = user_input[1:].split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            return {
                "is_command": True,
                "command": command,
                "args": args
            }
        
        return {
            "is_command": False,
            "message": user_input
        }
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID"""
        from uuid import uuid4
        return str(uuid4())[:8]
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        filename = filename[:100]
        return filename
    
    @staticmethod
    def format_timestamp(timestamp: Optional[str] = None) -> str:
        """Format timestamp for display"""
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                return timestamp
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """Calculate simple text similarity (Jaccard similarity)"""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)

# Factory functions for easy access
def get_formatter() -> AgentZFormatter:
    """Get formatter instance"""
    return AgentZFormatter()

def get_validator() -> AgentZValidator:
    """Get validator instance"""
    return AgentZValidator()

def get_utils() -> AgentZUtils:
    """Get utils instance"""
    return AgentZUtils()