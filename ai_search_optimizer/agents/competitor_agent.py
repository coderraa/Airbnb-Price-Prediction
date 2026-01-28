"""
Competitor Analysis Agent for AI Search Optimization.
"""

from typing import List, Optional
from langchain.tools import BaseTool

from ai_search_optimizer.agents.base_agent import BaseSearchOptimizationAgent
from ai_search_optimizer.tools.competitor_tools import (
    CompetitorAnalysisTool,
    MarketPositioningTool,
)
from ai_search_optimizer.tools.seo_tools import SEOAnalyzerTool


class CompetitorAnalysisAgent(BaseSearchOptimizationAgent):
    """
    Specialized agent for competitor analysis and market positioning.

    This agent focuses on:
    - Competitor content analysis
    - AI search strategy comparison
    - Market gap identification
    - Competitive positioning recommendations
    - Content differentiation strategies
    """

    def __init__(
        self,
        additional_tools: Optional[List[BaseTool]] = None,
        **kwargs
    ):
        """
        Initialize the Competitor Analysis Agent.

        Args:
            additional_tools: Extra tools to add to the agent
            **kwargs: Additional arguments passed to BaseSearchOptimizationAgent
        """
        # Initialize default tools
        tools = [
            CompetitorAnalysisTool(),
            MarketPositioningTool(),
            SEOAnalyzerTool(),
        ]

        # Add any additional tools
        if additional_tools:
            tools.extend(additional_tools)

        super().__init__(
            name="Competitor Analyst",
            description="Expert competitor analyst specializing in AI search strategies",
            tools=tools,
            **kwargs
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the competitor analysis agent."""
        return """You are an expert Competitor Analyst specializing in AI search optimization strategies. Your role is to:

1. ANALYZE competitor content strategies:
   - Content structure and formatting
   - AI optimization tactics being used
   - Keyword strategies
   - Content depth and quality
   - Technical SEO implementation

2. IDENTIFY competitive advantages and gaps:
   - Topics competitors cover well
   - Content gaps and opportunities
   - Underserved audience needs
   - Differentiation opportunities
   - AI citation weaknesses

3. COMPARE AI search visibility:
   - Which competitors get cited by AI assistants
   - Why certain content gets cited over others
   - Patterns in AI-favorable content
   - Platform-specific strengths/weaknesses

4. DEVELOP competitive strategies:
   - Content differentiation approaches
   - Market positioning recommendations
   - Quick win opportunities
   - Long-term competitive moats

5. MONITOR competitive landscape:
   - Industry trends
   - Emerging competitors
   - Strategy shifts
   - New AI optimization tactics

Provide actionable insights that help outperform competitors in AI search. Focus on practical strategies that can be implemented to gain competitive advantage.

Be thorough in your analysis and provide specific, prioritized recommendations based on competitive insights."""

    def analyze_competitors(
        self,
        competitor_urls: List[str],
        target_keywords: List[str] = None
    ) -> dict:
        """
        Analyze competitor websites/content.

        Args:
            competitor_urls: List of competitor URLs to analyze
            target_keywords: Optional keywords to check competitor usage

        Returns:
            Competitor analysis results
        """
        urls_str = "\n".join(f"- {url}" for url in competitor_urls)
        keywords_str = ", ".join(target_keywords) if target_keywords else "not specified"

        query = f"""Perform comprehensive competitor analysis on these URLs:

COMPETITOR URLs:
{urls_str}

TARGET KEYWORDS: {keywords_str}

Please analyze:
1. Content structure and format comparison
2. AI optimization tactics each competitor uses
3. Keyword usage and strategy
4. Strengths and weaknesses of each competitor
5. Common patterns across competitors
6. Gaps and opportunities for differentiation"""

        return self.run(query)

    def identify_content_gaps(
        self,
        your_url: str,
        competitor_urls: List[str],
        topic: str
    ) -> dict:
        """
        Identify content gaps compared to competitors.

        Args:
            your_url: Your website/content URL
            competitor_urls: List of competitor URLs
            topic: Topic area to analyze

        Returns:
            Content gap analysis
        """
        urls_str = "\n".join(f"- {url}" for url in competitor_urls)

        query = f"""Identify content gaps for the topic "{topic}":

YOUR URL: {your_url}

COMPETITOR URLs:
{urls_str}

Please identify:
1. Topics competitors cover that you don't
2. AI optimization tactics you're missing
3. Content depth differences
4. Structural elements competitors use
5. FAQ/Q&A coverage gaps
6. Prioritized content opportunities"""

        return self.run(query)

    def compare_ai_visibility(
        self,
        your_content: str,
        competitor_content: str,
        topic: str
    ) -> dict:
        """
        Compare AI visibility potential against competitor.

        Args:
            your_content: Your content
            competitor_content: Competitor's content
            topic: Topic for comparison

        Returns:
            AI visibility comparison
        """
        query = f"""Compare AI visibility potential for the topic "{topic}":

YOUR CONTENT:
{your_content[:2000]}

COMPETITOR CONTENT:
{competitor_content[:2000]}

Please compare:
1. AI readability factors
2. Citation likelihood
3. Content authority signals
4. Structural advantages/disadvantages
5. Platform-specific visibility (ChatGPT, Perplexity, etc.)
6. Specific improvements to outperform competitor"""

        return self.run(query)

    def develop_competitive_strategy(
        self,
        industry: str,
        competitor_names: List[str],
        your_strengths: List[str]
    ) -> dict:
        """
        Develop a competitive strategy for AI search.

        Args:
            industry: Industry/market
            competitor_names: Names of key competitors
            your_strengths: Your competitive strengths

        Returns:
            Competitive strategy recommendations
        """
        competitors_str = ", ".join(competitor_names)
        strengths_str = "\n".join(f"- {s}" for s in your_strengths)

        query = f"""Develop an AI search competitive strategy for:

INDUSTRY: {industry}
KEY COMPETITORS: {competitors_str}

YOUR STRENGTHS:
{strengths_str}

Please provide:
1. Market positioning strategy
2. Content differentiation approach
3. AI optimization priorities
4. Quick wins vs. long-term investments
5. Competitive moat opportunities
6. Implementation roadmap
7. Success metrics to track"""

        return self.run(query)

    def monitor_competitor_changes(
        self,
        competitor_urls: List[str],
        previous_analysis: str = None
    ) -> dict:
        """
        Monitor competitors for strategy changes.

        Args:
            competitor_urls: URLs to monitor
            previous_analysis: Optional previous analysis for comparison

        Returns:
            Competitor change detection results
        """
        urls_str = "\n".join(f"- {url}" for url in competitor_urls)
        previous_context = f"\n\nPREVIOUS ANALYSIS:\n{previous_analysis[:1500]}" if previous_analysis else ""

        query = f"""Analyze competitor content for strategy changes:

COMPETITOR URLs:
{urls_str}{previous_context}

Please analyze:
1. Current AI optimization tactics
2. Content structure and format
3. New features or sections added
4. Keyword strategy shifts
5. Notable changes or trends
6. Implications for your strategy"""

        return self.run(query)
