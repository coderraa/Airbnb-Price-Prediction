# AI Search Optimization Agent

An agentic solution for AI search optimization using **LangChain** and **Google Gemini LLM**. This framework helps marketing platforms optimize their content for visibility and citation across AI-powered search systems like ChatGPT, Perplexity, Claude, and Google AI Overview.

## Features

- **Multi-Agent Architecture**: Specialized agents for SEO, keywords, content, competitors, and marketing strategy
- **LangChain Framework**: Built on LangChain for robust agent orchestration
- **Gemini LLM Integration**: Powered by Google's Gemini models for intelligent analysis
- **AI Search Optimization**: Specifically designed for AI-powered search platforms
- **Comprehensive Tools**: SEO analysis, keyword research, content optimization, competitor analysis
- **CLI Interface**: Easy-to-use command-line interface
- **Async Support**: Asynchronous operations for improved performance
- **Caching**: Built-in caching for faster repeated analyses

## Architecture

```
ai_search_optimizer/
├── agents/                 # Specialized LangChain agents
│   ├── base_agent.py      # Base agent class with Gemini integration
│   ├── seo_agent.py       # SEO analysis agent
│   ├── keyword_agent.py   # Keyword research agent
│   ├── content_agent.py   # Content optimization agent
│   ├── competitor_agent.py # Competitor analysis agent
│   └── marketing_agent.py # Marketing strategy agent
├── tools/                  # LangChain tools for agents
│   ├── seo_tools.py       # SEO analysis tools
│   ├── keyword_tools.py   # Keyword research tools
│   ├── content_tools.py   # Content optimization tools
│   └── competitor_tools.py # Competitor analysis tools
├── prompts/               # Prompt templates
├── utils/                 # Utility functions and caching
├── orchestrator.py        # Main orchestrator coordinating agents
├── config.py              # Configuration and settings
└── cli.py                 # Command-line interface
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-search-optimizer.git
cd ai-search-optimizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

## Configuration

Create a `.env` file with your configuration:

```env
# Google Gemini API Key (required)
AI_SEARCH_GOOGLE_API_KEY=your-google-api-key

# Model Configuration (optional)
AI_SEARCH_GEMINI_MODEL=gemini-1.5-pro
AI_SEARCH_GEMINI_TEMPERATURE=0.7

# SerpAPI for search results (optional)
AI_SEARCH_SERPAPI_KEY=your-serpapi-key

# Agent Configuration (optional)
AI_SEARCH_MAX_ITERATIONS=10
AI_SEARCH_VERBOSE=true

# Caching (optional)
AI_SEARCH_CACHE_ENABLED=true
AI_SEARCH_CACHE_TTL=3600
```

## Quick Start

### Using the CLI

```bash
# Analyze a URL for SEO optimization
python -m ai_search_optimizer.cli analyze-url https://example.com -k "AI marketing,automation"

# Research keywords for a topic
python -m ai_search_optimizer.cli research-keywords "AI marketing automation" -i "SaaS"

# Optimize content from a file
python -m ai_search_optimizer.cli optimize-content content.txt -k "AI,marketing" -p chatgpt

# Analyze competitors
python -m ai_search_optimizer.cli analyze-competitors "https://competitor1.com,https://competitor2.com"

# Create a marketing strategy
python -m ai_search_optimizer.cli create-strategy "MyBusiness" -i "Technology" -a "Small businesses" -g "Increase traffic,Build authority"

# Interactive mode
python -m ai_search_optimizer.cli interactive
```

### Using Python API

```python
from ai_search_optimizer import SearchOptimizationOrchestrator

# Initialize the orchestrator
orchestrator = SearchOptimizationOrchestrator(verbose=True)

# Run a natural language task
result = orchestrator.run("Help me optimize my SaaS product page for AI search")

# Or use comprehensive URL optimization
result = orchestrator.optimize_url(
    url="https://example.com",
    keywords=["AI analytics", "business intelligence"],
    include_competitors=["https://competitor.com"]
)

print(result["summary"])
```

### Using Individual Agents

```python
from ai_search_optimizer.agents import (
    SEOAgent,
    KeywordResearchAgent,
    ContentOptimizationAgent,
)

# SEO Analysis
seo_agent = SEOAgent()
result = seo_agent.analyze_url("https://example.com")

# Keyword Research
keyword_agent = KeywordResearchAgent()
result = keyword_agent.research_keywords("AI marketing", industry="Technology")

# Content Optimization
content_agent = ContentOptimizationAgent()
result = content_agent.optimize_content(
    content="Your content here...",
    keywords=["AI", "marketing"],
    target_platform="chatgpt"
)
```

### Using Tools Directly

```python
from ai_search_optimizer.tools import (
    SEOAnalyzerTool,
    KeywordResearchTool,
    AIVisibilityTool,
)

# Direct tool usage
seo_tool = SEOAnalyzerTool()
result = seo_tool._run(url="https://example.com")

keyword_tool = KeywordResearchTool()
result = keyword_tool._run(topic="machine learning")

visibility_tool = AIVisibilityTool()
result = visibility_tool._run(content="Your content...", topic="AI")
```

## Agents

### SEO Agent
Analyzes websites and content for SEO factors affecting visibility in both traditional and AI-powered search systems.

**Capabilities:**
- Technical SEO analysis (title, meta, headers)
- Content quality assessment
- AI-specific SEO recommendations
- Competitive SEO comparison

### Keyword Research Agent
Researches keywords effective for both traditional search and AI query patterns.

**Capabilities:**
- Semantic keyword expansion
- Long-tail keyword discovery
- Question-based keywords (crucial for AI)
- Intent-based keyword clusters

### Content Optimization Agent
Optimizes content for maximum visibility across AI platforms.

**Capabilities:**
- Structure optimization for AI readability
- Platform-specific recommendations (ChatGPT, Perplexity, Claude, Google)
- FAQ section generation
- Featured snippet optimization

### Competitor Analysis Agent
Analyzes competitor strategies and identifies opportunities.

**Capabilities:**
- Content strategy analysis
- AI optimization tactics identification
- Content gap analysis
- Competitive positioning

### Marketing Strategy Agent
Develops comprehensive AI search marketing strategies.

**Capabilities:**
- AI-first marketing strategy development
- Content calendar planning
- Thought leadership strategy
- ROI analysis and optimization

## AI Platform Optimization

The framework optimizes content for multiple AI platforms:

| Platform | Key Focus Areas |
|----------|----------------|
| ChatGPT | Conversational, practical examples, step-by-step content |
| Perplexity | Factual content, citations, statistics, data |
| Claude | Nuanced analysis, multiple perspectives, comprehensive coverage |
| Google AI | Structured content, header hierarchy, FAQ schema |

## Examples

See the `examples/` directory for detailed usage examples:

- `basic_usage.py` - Core functionality examples
- `advanced_usage.py` - Advanced features including async, caching, custom workflows

## API Reference

### SearchOptimizationOrchestrator

```python
orchestrator = SearchOptimizationOrchestrator(verbose=True)

# Natural language task
result = orchestrator.run("Your task description")

# URL optimization
result = orchestrator.optimize_url(url, keywords, include_competitors)

# Marketing plan
result = orchestrator.create_marketing_plan(business_info, goals, budget)

# Content optimization
result = orchestrator.optimize_content(content, keywords, target_platform)
```

### Agent Methods

All agents inherit from `BaseSearchOptimizationAgent` and provide:

```python
# Synchronous execution
result = agent.run(query)

# Asynchronous execution
result = await agent.arun(query)

# Get available tools
tools = agent.get_tool_names()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- Built with [LangChain](https://www.langchain.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
