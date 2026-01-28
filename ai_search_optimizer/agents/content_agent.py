"""
Content Optimization Agent for AI Search Optimization.
"""

from typing import List, Optional
from langchain.tools import BaseTool

from ai_search_optimizer.agents.base_agent import BaseSearchOptimizationAgent
from ai_search_optimizer.tools.content_tools import (
    ContentOptimizerTool,
    ReadabilityAnalyzerTool,
    AIVisibilityTool,
)


class ContentOptimizationAgent(BaseSearchOptimizationAgent):
    """
    Specialized agent for content optimization targeting AI search.

    This agent focuses on:
    - Content structure optimization
    - Readability improvements
    - AI visibility enhancement
    - Content formatting for AI parsing
    - Platform-specific optimization
    """

    def __init__(
        self,
        additional_tools: Optional[List[BaseTool]] = None,
        **kwargs
    ):
        """
        Initialize the Content Optimization Agent.

        Args:
            additional_tools: Extra tools to add to the agent
            **kwargs: Additional arguments passed to BaseSearchOptimizationAgent
        """
        # Initialize default tools
        tools = [
            ContentOptimizerTool(),
            ReadabilityAnalyzerTool(),
            AIVisibilityTool(),
        ]

        # Add any additional tools
        if additional_tools:
            tools.extend(additional_tools)

        super().__init__(
            name="Content Optimizer",
            description="Expert content optimizer specializing in AI search visibility",
            tools=tools,
            **kwargs
        )

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the content optimization agent."""
        return """You are an expert Content Optimizer specializing in AI search visibility. Your role is to:

1. OPTIMIZE content for maximum visibility across AI-powered search platforms (ChatGPT, Perplexity, Claude, Google AI Overview, Bing Copilot).

2. ENHANCE content structure for AI readability:
   - Clear hierarchical organization
   - Scannable formatting with headers and lists
   - Logical flow and transitions
   - FAQ sections for Q&A queries
   - Definition patterns for key terms

3. IMPROVE AI citation likelihood:
   - Authoritative language and tone
   - Factual statements with context
   - Clear, quotable passages
   - Structured data opportunities
   - Expert positioning signals

4. ADAPT content for different AI platforms:
   - ChatGPT: Conversational, practical, example-rich
   - Perplexity: Factual, well-sourced, data-driven
   - Claude: Nuanced, comprehensive, multi-perspective
   - Google AI Overview: Structured, concise, schema-optimized

5. BALANCE optimization with quality:
   - Maintain natural, readable content
   - Avoid over-optimization
   - Preserve brand voice
   - Ensure user value

Your recommendations should be specific, actionable, and prioritized by impact. Always explain WHY a change will improve AI visibility and provide examples when helpful.

Focus on creating content that AI systems will confidently cite and recommend to users."""

    def optimize_content(
        self,
        content: str,
        keywords: List[str] = None,
        target_platform: str = "all"
    ) -> dict:
        """
        Optimize content for AI search visibility.

        Args:
            content: The content to optimize
            keywords: Target keywords for optimization
            target_platform: Target AI platform (chatgpt, perplexity, claude, google, all)

        Returns:
            Optimization results and recommendations
        """
        keywords_str = ", ".join(keywords) if keywords else "not specified"

        query = f"""Optimize this content for AI search visibility:

CONTENT:
{content[:4000]}

TARGET KEYWORDS: {keywords_str}
TARGET PLATFORM: {target_platform}

Please provide:
1. Content assessment (current state)
2. AI readability analysis
3. Structure optimization recommendations
4. Specific rewrite suggestions for key sections
5. FAQ section recommendations
6. Platform-specific optimizations
7. Implementation priority list"""

        return self.run(query)

    def analyze_ai_visibility(self, content: str, topic: str = None) -> dict:
        """
        Analyze content's AI visibility potential.

        Args:
            content: The content to analyze
            topic: Optional topic context

        Returns:
            AI visibility analysis
        """
        topic_str = f" about '{topic}'" if topic else ""

        query = f"""Analyze the AI visibility potential of this content{topic_str}:

CONTENT:
{content[:4000]}

Please analyze:
1. Overall AI visibility score
2. Platform-specific scores (ChatGPT, Perplexity, Claude, Google AI)
3. Citation likelihood factors
4. Content gaps for AI optimization
5. Specific improvement recommendations
6. Quick wins for immediate improvement"""

        return self.run(query)

    def create_ai_optimized_outline(
        self,
        topic: str,
        target_audience: str,
        content_type: str = "article"
    ) -> dict:
        """
        Create an AI-optimized content outline.

        Args:
            topic: The topic for the content
            target_audience: Description of target audience
            content_type: Type of content (article, guide, tutorial, etc.)

        Returns:
            Content outline optimized for AI search
        """
        query = f"""Create an AI-optimized {content_type} outline for:

TOPIC: {topic}
TARGET AUDIENCE: {target_audience}

Please provide:
1. Recommended title (optimized for AI queries)
2. Meta description suggestion
3. Detailed section outline with headers
4. Key points to cover in each section
5. FAQ questions to include
6. Recommended word count and structure
7. AI optimization tips for each section
8. Schema markup recommendations"""

        return self.run(query)

    def improve_readability(self, content: str) -> dict:
        """
        Improve content readability for AI systems.

        Args:
            content: The content to improve

        Returns:
            Readability improvement recommendations
        """
        query = f"""Analyze and improve the readability of this content for AI systems:

CONTENT:
{content[:4000]}

Please provide:
1. Current readability assessment
2. Sentence length optimization suggestions
3. Paragraph structure improvements
4. Complex word simplification recommendations
5. Transition and flow improvements
6. Formatting enhancements
7. Before/after examples for key passages"""

        return self.run(query)

    def create_faq_section(self, topic: str, existing_content: str = None) -> dict:
        """
        Create an FAQ section optimized for AI search.

        Args:
            topic: The topic for the FAQ
            existing_content: Optional existing content to base FAQ on

        Returns:
            AI-optimized FAQ section
        """
        content_context = f"\n\nEXISTING CONTENT:\n{existing_content[:2000]}" if existing_content else ""

        query = f"""Create an FAQ section optimized for AI search about: {topic}{content_context}

Please provide:
1. 8-10 FAQ questions that users commonly ask AI assistants
2. Concise, authoritative answers for each
3. Natural keyword integration
4. Schema markup structure (FAQ schema)
5. Tips for making FAQs AI-citation friendly"""

        return self.run(query)

    def optimize_for_featured_snippets(self, content: str, query: str) -> dict:
        """
        Optimize content for featured snippets and AI citations.

        Args:
            content: The content to optimize
            query: The target query to optimize for

        Returns:
            Featured snippet optimization recommendations
        """
        optimization_query = f"""Optimize this content for featured snippets and AI citations for the query: "{query}"

CONTENT:
{content[:4000]}

Please provide:
1. Current snippet eligibility assessment
2. Recommended answer format (paragraph, list, table)
3. Optimized answer text (40-60 words)
4. Supporting content structure
5. Header optimization for the target query
6. Additional queries this content could rank for"""

        return self.run(optimization_query)
