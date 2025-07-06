# 🚀 AgentZ - AI Co-founder Assistant

**AgentZ** is an agentic AI co-founder that helps entrepreneurs validate ideas, understand markets, and plan smarter through natural conversation. Built with modern AI technologies for fast, intelligent startup guidance.

## ✨ Features

- **🤖 Conversational Interface** - Natural terminal-based chat with AI co-founder
- **🧠 Smart Memory System** - RAG-based context retrieval using ChromaDB
- **🔧 Research Tools** - Mock integrations for market research, competitor analysis, and idea validation
- **⚡ Fast Inference** - Powered by Groq (Mixtral/Llama3) for near-instant responses
- **📊 Vector Search** - OpenAI embeddings for intelligent memory retrieval
- **📈 PromptLayer Support** - Optional prompt tracking and analytics
- **🎯 Founder-Focused** - Prompts inspired by successful startup methodologies

## 🏗️ Architecture

```
agentz/
├── .env              # API keys and configuration
├── main.py           # Core engine and conversation loop
├── llm.py            # LLM wrapper (Groq + OpenAI)
├── prompts.py        # Strategic prompt templates
├── memory.py         # RAG-based context retrieval
├── tools.py          # Mock research tools
└── utils.py          # Formatting and utilities
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Copy the `.env` file and add your API keys:

```bash
cp agentz/.env.example agentz/.env
```

Edit `agentz/.env`:

```env
# Required API Keys
GROQ_API_KEY=your_groq_api_key_here          # Get from https://console.groq.com/
OPENAI_API_KEY=your_openai_api_key_here      # Get from https://platform.openai.com/

# Optional
PROMPTLAYER_API_KEY=your_promptlayer_key     # Get from https://promptlayer.com/
ENABLE_PROMPTLAYER=false
```

### 3. Run AgentZ

```bash
cd agentz
python main.py
```

## 🔑 API Keys Setup

### Required APIs

1. **Groq API** (Free tier available)
   - Sign up at [console.groq.com](https://console.groq.com/)
   - Create API key
   - Fast inference with Mixtral-8x7B or Llama3

2. **OpenAI API** (Pay-per-use)
   - Sign up at [platform.openai.com](https://platform.openai.com/)
   - Create API key
   - Used for embeddings (text-embedding-3-small)

### Optional APIs

3. **PromptLayer** (Optional - for prompt tracking)
   - Sign up at [promptlayer.com](https://promptlayer.com/)
   - Enable in `.env` with `ENABLE_PROMPTLAYER=true`

## 💬 How to Use

### Natural Conversation

Just start typing your business questions:

```
💬 You: I have an idea for a SaaS project management tool. Is this viable?

🤖 AgentZ: Let me help you validate this idea...
[Automatically runs idea validation and market research]
```

### Commands

- `/help` - Show all available commands
- `/tools` - List research tools
- `/memory` - Show conversation memory stats
- `/research <topic>` - Quick research on any topic
- `/clear` - Clear conversation history
- `/config` - Show current configuration
- `/exit` - Exit AgentZ

### Example Conversations

**Market Research:**
```
💬 You: What's the market size for fintech solutions?
🤖 AgentZ: [Runs market research tool and provides TAM/SAM/SOM analysis]
```

**Competitor Analysis:**
```
💬 You: Who are the main competitors in e-commerce platforms?
🤖 AgentZ: [Analyzes competitive landscape with positioning map]
```

**Idea Validation:**
```
💬 You: Should I build a mobile app for food delivery?
🤖 AgentZ: [Validates idea across problem, market, solution, and business model]
```

## 🔧 Configuration

### Models

- **Default LLM:** `mixtral-8x7b-32768` (Groq)
- **Default Embeddings:** `text-embedding-3-small` (OpenAI)
- **Vector DB:** ChromaDB (local persistence)

### Customization

Edit `agentz/.env` to customize:

```env
GROQ_MODEL=llama3-70b-8192              # Switch to Llama3
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002  # Use different embeddings
CHROMA_PERSIST_DIRECTORY=./my_memory    # Custom memory location
```

## 🛠️ Development

### Architecture Overview

- **LLM Layer:** Groq for fast inference, OpenAI for embeddings
- **Memory Layer:** ChromaDB vector store with RAG retrieval
- **Tools Layer:** Mock integrations simulating real business tools
- **Interface Layer:** Rich terminal UI with conversation management

### Key Components

1. **`llm.py`** - Abstracts LLM calls with error handling and optional PromptLayer tracking
2. **`memory.py`** - Vector-based memory system for conversations and insights
3. **`tools.py`** - Mock tools for market research, competitive analysis, idea validation
4. **`prompts.py`** - Strategic prompts inspired by lean startup methodology
5. **`main.py`** - Orchestrates all components in conversation loop

### Adding New Tools

```python
# In tools.py
class MyCustomTool:
    def analyze(self, data: str) -> Dict[str, Any]:
        # Your tool logic here
        return {"result": "analysis"}

# Register in AgentZTools class
def execute_tool(self, tool_name: str, **kwargs):
    if tool_name == "my_custom_tool":
        return self.my_custom.analyze(kwargs.get("data", ""))
```

## 📊 Research Tools

### Market Research Tool
- **TAM/SAM/SOM Analysis** - Market size estimates
- **Customer Segments** - Target customer identification  
- **Market Trends** - Industry trend analysis
- **Barriers to Entry** - Competitive barriers assessment

### Competitor Analysis Tool
- **Direct/Indirect Competitors** - Competitive landscape mapping
- **Feature Comparison** - Product feature matrix
- **Pricing Analysis** - Competitive pricing intelligence
- **Market Share** - Market position estimates
- **Competitive Gaps** - Opportunity identification

### Idea Validation Tool
- **Problem Validation** - Problem-market fit assessment
- **Market Validation** - Market opportunity scoring
- **Solution Validation** - Solution effectiveness analysis
- **Business Model Validation** - Revenue model viability
- **Risk Assessment** - Key risk factors and mitigation

## 🚧 Roadmap

### MVP Features ✅
- [x] Conversational interface
- [x] Vector-based memory
- [x] Mock research tools
- [x] Strategic prompts
- [x] Multi-model support

### Future Enhancements
- [ ] Real API integrations (Crunchbase, PitchBook, etc.)
- [ ] Web interface
- [ ] Business plan generation
- [ ] Financial modeling tools
- [ ] Team collaboration features
- [ ] Integration with startup tools (Notion, Airtable, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Common Issues

**API Key Errors:**
```bash
❌ Error: GROQ_API_KEY not set in .env file
```
- Check that your `.env` file exists in the `agentz/` directory
- Verify API keys are correct and not placeholder values

**Import Errors:**
```bash
❌ Error: No module named 'chromadb'
```
- Run `pip install -r requirements.txt`
- Make sure you're in the project root directory

**Memory Issues:**
```bash
❌ Error: ChromaDB connection failed
```
- Check disk space for ChromaDB storage
- Ensure write permissions in project directory

### Getting Help

- 📧 Create an issue on GitHub
- 💬 Check existing issues for solutions
- 📖 Read the troubleshooting guide

## 🙏 Acknowledgments

- **LangChain** for orchestration framework
- **Groq** for blazing-fast inference
- **OpenAI** for embeddings
- **ChromaDB** for vector storage
- **Rich** for beautiful terminal UI

---

**Built with ❤️ for entrepreneurs who want to build something amazing.**

*AgentZ - Your AI Co-founder for startup success* 🚀
