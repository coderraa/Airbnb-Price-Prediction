"""
Keyword Research Agent for AI Search Optimization.
"""

from typing import List, Optional
from langchain.tools import BaseTool

from ai_search_optimizer.agents.base_agent import BaseSearchOptimizationAgent
from ai_search_optimizer.tools.keyword_tools import (
    KeywordResearchTool,
    KeywordDensityTool,
    SemanticKeywordTool,
)


class KeywordResearchAgent(BaseSearchOptimizationAgent):
    """
    Specialized agent for keyword research and optimization.

    This agent focuses on:
    - Keyword research and discovery
    - Semantic keyword expansion
    - Keyword density analysis
    - AI-optimized keyword strategies
    - Long-tail keyword opportunities
    """

    def __init__(
        self,
        additional_tools: Optional[List[BaseTool]] = None,
        **kwargs
    ):
        """
        Initialize the Keyword Research Agent.

        Args:
            additional_tools: Extra tools to add to the agent
            **kwargs: Additional arguments passed to BaseSearchOptimizationAgent
        """
        # Initialize default tools
        tools = [
            KeywordResearchTool(),
            KeywordDensityTool(),
            SemanticKeywordTool(),
        ]

        # Add any additional tools
        if additional_tools:
            tools.extend(additional_tools)

        super().__init__(
            name="Keyword Researcher",
            description="Expert keyword researcher specializing in AI search optimization",
            tools=tools,
            **kwargs
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the keyword research agent."""
        return """You are an expert Keyword Researcher specializing in AI search optimization. Your role is to:

1. RESEARCH keywords that are effective for both traditional search engines and AI-powered search systems like ChatGPT, Perplexity, Claude, and Google AI Overview.

2. IDENTIFY keyword opportunities including:
   - Primary keywords with high relevance
   - Long-tail keywords for specific queries
   - Question-based keywords (crucial for AI search)
   - Semantic variations and related terms
   - Intent-based keyword clusters

3. ANALYZE keyword characteristics:
   - Search intent (informational, commercial, transactional, navigational)
   - AI query patterns (how users ask AI assistants)
   - Conversational keyword phrases
   - Natural language variations

4. PROVIDE AI-OPTIMIZED keyword strategies:
   - Keywords that align with how AI systems process queries
   - Question-answer keyword pairs
   - Contextual keyword clusters
   - Entity-based keywords

5. RECOMMEND keyword placement strategies:
   - Title and header keywords
   - Body content keyword density
   - FAQ and Q&A keyword integration
   - Schema and structured data keywords

Focus on keywords that help content get discovered AND cited by AI systems. Consider both traditional search volume and AI query patterns.

Be thorough in your research and provide actionable keyword recommendations with clear prioritization."""

    def research_keywords(self, topic: str, industry: str = None) -> dict:
        """
        Research keywords for a topic.

        Args:
            topic: The topic to research keywords for
            industry: Optional industry context

        Returns:
            Keyword research results
        """
        industry_context = f" in the {industry} industry" if industry else ""

        query = f"""Perform comprehensive keyword research for: "{topic}"{industry_context}

Please provide:
1. Primary keyword variations
2. Long-tail keyword opportunities
3. Question-based keywords (for AI search)
4. Semantic and related keywords
5. Intent-based keyword clusters
6. AI-optimized keyword recommendations

Prioritize keywords that work well for both traditional search and AI assistants."""

        return self.run(query)

    def analyze_keyword_density(
        self,
        content: str,
        keywords: List[str]
    ) -> dict:
        """
        Analyze keyword density in content.

        Args:
            content: The content to analyze
            keywords: List of keywords to check

        Returns:
            Density analysis results
        """
        keywords_str = ", ".join(keywords)

        query = f"""Analyze keyword density for these keywords: {keywords_str}

CONTENT:
{content[:3000]}

Please analyze:
1. Current keyword density for each keyword
2. Keyword placement (title, headers, body, conclusion)
3. Whether density is optimal, too low, or too high
4. Recommendations for optimization
5. Natural keyword integration suggestions"""

        return self.run(query)

    def expand_semantic_keywords(self, primary_keyword: str) -> dict:
        """
        Expand a keyword into semantic variations.

        Args:
            primary_keyword: The primary keyword to expand

        Returns:
            Semantic keyword expansion results
        """
        query = f"""Expand this keyword into semantic variations: "{primary_keyword}"

Please provide:
1. Synonyms and related terms
2. LSI (Latent Semantic Indexing) keywords
3. Co-occurring keywords
4. Entity-based variations
5. Action-oriented keywords
6. Question format variations

Focus on semantic variations that help AI systems understand the topic comprehensively."""

        return self.run(query)

    def generate_ai_query_keywords(self, topic: str) -> dict:
        """
        Generate keywords based on how users query AI assistants.

        Args:
            topic: The topic to generate AI query keywords for

        Returns:
            AI-optimized keyword suggestions
        """
        query = f"""Generate keywords optimized for AI assistant queries about: "{topic}"

Consider how users typically ask AI assistants (ChatGPT, Claude, Perplexity):
1. Conversational query patterns
2. "Explain to me..." style queries
3. "What is the best..." style queries
4. Comparison queries
5. How-to queries
6. Definition and explanation queries

Provide keywords that align with these AI query patterns and help content get cited by AI systems."""

        return self.run(query)

    def create_keyword_strategy(
        self,
        business_type: str,
        target_audience: str,
        goals: List[str]
    ) -> dict:
        """
        Create a comprehensive keyword strategy.

        Args:
            business_type: Type of business
            target_audience: Description of target audience
            goals: List of marketing goals

        Returns:
            Keyword strategy results
        """
        goals_str = "\n".join(f"- {g}" for g in goals)

        query = f"""Create a comprehensive keyword strategy for:

BUSINESS TYPE: {business_type}
TARGET AUDIENCE: {target_audience}

GOALS:
{goals_str}

Please provide:
1. Primary keyword themes
2. Supporting keyword clusters
3. Content pillar keyword mapping
4. AI search optimization keywords
5. Competitive keyword opportunities
6. Implementation prioritization
7. Measurement recommendations"""

        return self.run(query)
