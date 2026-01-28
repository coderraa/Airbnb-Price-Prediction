"""
SEO Analysis Agent for AI Search Optimization.
"""

from typing import List, Optional
from langchain.tools import BaseTool

from ai_search_optimizer.agents.base_agent import BaseSearchOptimizationAgent
from ai_search_optimizer.tools.seo_tools import (
    SEOAnalyzerTool,
    MetaTagAnalyzerTool,
    ContentStructureAnalyzerTool,
)


class SEOAgent(BaseSearchOptimizationAgent):
    """
    Specialized agent for SEO analysis and optimization.

    This agent focuses on:
    - Technical SEO analysis
    - On-page SEO optimization
    - Meta tag optimization
    - Content structure analysis
    - AI-specific SEO recommendations
    """

    def __init__(
        self,
        additional_tools: Optional[List[BaseTool]] = None,
        **kwargs
    ):
        """
        Initialize the SEO Agent.

        Args:
            additional_tools: Extra tools to add to the agent
            **kwargs: Additional arguments passed to BaseSearchOptimizationAgent
        """
        # Initialize default tools
        tools = [
            SEOAnalyzerTool(),
            MetaTagAnalyzerTool(),
            ContentStructureAnalyzerTool(),
        ]

        # Add any additional tools
        if additional_tools:
            tools.extend(additional_tools)

        super().__init__(
            name="SEO Analyst",
            description="Expert SEO analyst specializing in AI search optimization",
            tools=tools,
            **kwargs
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the SEO agent."""
        return """You are an expert SEO Analyst specializing in AI search optimization. Your role is to:

1. ANALYZE websites and content for SEO factors that affect visibility in both traditional search and AI-powered search systems (ChatGPT, Perplexity, Claude, Google AI Overview).

2. IDENTIFY technical SEO issues and opportunities including:
   - Title tag and meta description optimization
   - Header structure and hierarchy
   - Content quality signals
   - Internal/external linking
   - Image optimization
   - Schema markup and structured data

3. PROVIDE AI-SPECIFIC SEO recommendations:
   - Content formatting that AI systems can easily parse and cite
   - Structured data that helps AI understand context
   - FAQ sections and Q&A formatting
   - Clear definitions and explanations

4. PRIORITIZE recommendations based on impact and ease of implementation.

5. EXPLAIN the reasoning behind each recommendation and how it affects AI search visibility.

When analyzing, always consider both traditional search engine factors AND how modern AI assistants consume and cite content. Your goal is to help content rank well and be cited by AI systems.

Be thorough but concise. Focus on actionable insights that can immediately improve search visibility."""

    def analyze_url(self, url: str) -> dict:
        """
        Analyze a URL for SEO factors.

        Args:
            url: The URL to analyze

        Returns:
            Analysis results
        """
        query = f"""Perform a comprehensive SEO analysis of this URL: {url}

Please analyze:
1. Title tag and meta description
2. Header structure
3. Content quality and length
4. Internal/external links
5. Image optimization
6. Schema markup
7. AI search visibility factors

Provide specific recommendations for improvement, prioritized by impact."""

        return self.run(query)

    def analyze_content(self, content: str, keywords: List[str] = None) -> dict:
        """
        Analyze content for SEO optimization.

        Args:
            content: The content to analyze
            keywords: Target keywords to check

        Returns:
            Analysis results
        """
        keywords_str = ", ".join(keywords) if keywords else "not specified"

        query = f"""Analyze this content for SEO optimization:

CONTENT:
{content[:3000]}...

TARGET KEYWORDS: {keywords_str}

Please analyze:
1. Content structure and organization
2. Keyword usage and density
3. Readability for AI systems
4. Suggestions for improvement
5. AI-specific optimization opportunities"""

        return self.run(query)

    def compare_with_competitors(
        self,
        url: str,
        competitor_urls: List[str]
    ) -> dict:
        """
        Compare SEO performance against competitors.

        Args:
            url: Your URL to analyze
            competitor_urls: List of competitor URLs

        Returns:
            Comparison results
        """
        competitors_str = "\n".join(f"- {u}" for u in competitor_urls)

        query = f"""Compare the SEO performance of this URL against competitors:

YOUR URL: {url}

COMPETITOR URLs:
{competitors_str}

Please analyze and compare:
1. Technical SEO factors
2. Content quality and structure
3. AI optimization tactics
4. Identify gaps and opportunities
5. Prioritized recommendations to outperform competitors"""

        return self.run(query)
