"""
Main Orchestrator for AI Search Optimization.

This module coordinates multiple specialized agents to provide
comprehensive AI search optimization solutions.
"""

from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from ai_search_optimizer.config import settings
from ai_search_optimizer.agents import (
    SEOAgent,
    KeywordResearchAgent,
    ContentOptimizationAgent,
    CompetitorAnalysisAgent,
    MarketingStrategyAgent,
)
from ai_search_optimizer.utils.cache import cache


class TaskType(Enum):
    """Types of optimization tasks."""
    SEO_ANALYSIS = "seo_analysis"
    KEYWORD_RESEARCH = "keyword_research"
    CONTENT_OPTIMIZATION = "content_optimization"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    MARKETING_STRATEGY = "marketing_strategy"
    COMPREHENSIVE = "comprehensive"


@dataclass
class OptimizationTask:
    """Represents an optimization task."""
    task_type: TaskType
    input_data: Dict[str, Any]
    priority: int = 1
    completed: bool = False
    result: Optional[Dict[str, Any]] = None


class SearchOptimizationOrchestrator:
    """
    Orchestrates multiple AI search optimization agents.

    This class coordinates specialized agents to provide comprehensive
    AI search optimization solutions for marketing platforms.
    """

    def __init__(self, verbose: bool = None):
        """
        Initialize the orchestrator.

        Args:
            verbose: Enable verbose output (default from settings)
        """
        self.verbose = verbose if verbose is not None else settings.verbose

        # Initialize the coordinator LLM
        self.coordinator_llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # Lower temperature for coordination
        )

        # Initialize specialized agents
        self.agents = {
            TaskType.SEO_ANALYSIS: SEOAgent(verbose=self.verbose),
            TaskType.KEYWORD_RESEARCH: KeywordResearchAgent(verbose=self.verbose),
            TaskType.CONTENT_OPTIMIZATION: ContentOptimizationAgent(verbose=self.verbose),
            TaskType.COMPETITOR_ANALYSIS: CompetitorAnalysisAgent(verbose=self.verbose),
            TaskType.MARKETING_STRATEGY: MarketingStrategyAgent(verbose=self.verbose),
        }

        # Task history
        self.task_history: List[OptimizationTask] = []

    def _log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[Orchestrator] {message}")

    def analyze_task(self, task_description: str) -> List[TaskType]:
        """
        Analyze a task and determine which agents should handle it.

        Args:
            task_description: Natural language task description

        Returns:
            List of TaskType values indicating which agents to use
        """
        system_message = SystemMessage(content="""
You are a task analyzer for an AI search optimization system.
Analyze the given task and determine which specialized agents should handle it.

Available agents:
1. SEO_ANALYSIS - For technical SEO, on-page optimization, meta tags
2. KEYWORD_RESEARCH - For keyword discovery, analysis, and strategy
3. CONTENT_OPTIMIZATION - For content structure, readability, AI visibility
4. COMPETITOR_ANALYSIS - For competitive analysis and market positioning
5. MARKETING_STRATEGY - For overall marketing strategy and planning

Return ONLY the agent names (comma-separated) that should handle this task.
For comprehensive requests, include multiple agents in the order they should execute.

Examples:
- "Analyze my website for SEO" -> SEO_ANALYSIS
- "Research keywords for my product" -> KEYWORD_RESEARCH
- "Optimize my content for AI search" -> CONTENT_OPTIMIZATION
- "Analyze my competitors" -> COMPETITOR_ANALYSIS
- "Create a marketing strategy" -> MARKETING_STRATEGY
- "Help me rank better in AI search" -> SEO_ANALYSIS, KEYWORD_RESEARCH, CONTENT_OPTIMIZATION
""")

        human_message = HumanMessage(content=f"Task: {task_description}")

        response = self.coordinator_llm.invoke([system_message, human_message])

        # Parse response to extract agent types
        response_text = response.content.upper()
        agent_types = []

        type_mapping = {
            "SEO_ANALYSIS": TaskType.SEO_ANALYSIS,
            "KEYWORD_RESEARCH": TaskType.KEYWORD_RESEARCH,
            "CONTENT_OPTIMIZATION": TaskType.CONTENT_OPTIMIZATION,
            "COMPETITOR_ANALYSIS": TaskType.COMPETITOR_ANALYSIS,
            "MARKETING_STRATEGY": TaskType.MARKETING_STRATEGY,
        }

        for type_name, task_type in type_mapping.items():
            if type_name in response_text:
                agent_types.append(task_type)

        # Default to comprehensive if no specific type identified
        if not agent_types:
            agent_types = [TaskType.SEO_ANALYSIS, TaskType.CONTENT_OPTIMIZATION]

        return agent_types

    def run_agent(
        self,
        task_type: TaskType,
        query: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run a specific agent with the given query.

        Args:
            task_type: Type of task/agent to use
            query: Query to pass to the agent
            **kwargs: Additional arguments

        Returns:
            Agent execution result
        """
        if task_type not in self.agents:
            return {
                "success": False,
                "error": f"Unknown task type: {task_type}",
            }

        agent = self.agents[task_type]
        self._log(f"Running {agent.name} agent...")

        result = agent.run(query)

        # Track task
        task = OptimizationTask(
            task_type=task_type,
            input_data={"query": query, **kwargs},
            completed=result.get("success", False),
            result=result,
        )
        self.task_history.append(task)

        return result

    def optimize_url(
        self,
        url: str,
        keywords: List[str] = None,
        include_competitors: List[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive optimization analysis on a URL.

        Args:
            url: URL to analyze
            keywords: Target keywords (optional)
            include_competitors: Competitor URLs to analyze (optional)

        Returns:
            Comprehensive optimization results
        """
        self._log(f"Starting comprehensive URL optimization for: {url}")

        results = {
            "url": url,
            "keywords": keywords or [],
            "analyses": {},
            "recommendations": [],
        }

        # 1. SEO Analysis
        self._log("Running SEO analysis...")
        seo_query = f"Analyze this URL for SEO optimization: {url}"
        if keywords:
            seo_query += f"\nTarget keywords: {', '.join(keywords)}"
        results["analyses"]["seo"] = self.run_agent(TaskType.SEO_ANALYSIS, seo_query)

        # 2. Content Optimization Analysis
        self._log("Running content optimization analysis...")
        content_query = f"Analyze content optimization opportunities for: {url}"
        if keywords:
            content_query += f"\nOptimize for these keywords: {', '.join(keywords)}"
        results["analyses"]["content"] = self.run_agent(
            TaskType.CONTENT_OPTIMIZATION, content_query
        )

        # 3. Keyword Analysis (if keywords provided)
        if keywords:
            self._log("Running keyword analysis...")
            keyword_query = f"Analyze keyword strategy for these keywords: {', '.join(keywords)}"
            results["analyses"]["keywords"] = self.run_agent(
                TaskType.KEYWORD_RESEARCH, keyword_query
            )

        # 4. Competitor Analysis (if competitors provided)
        if include_competitors:
            self._log("Running competitor analysis...")
            competitor_query = f"""Analyze these competitors and compare to {url}:
            {chr(10).join('- ' + c for c in include_competitors)}"""
            results["analyses"]["competitors"] = self.run_agent(
                TaskType.COMPETITOR_ANALYSIS, competitor_query
            )

        # Synthesize results
        results["summary"] = self._synthesize_results(results["analyses"])

        return results

    def create_marketing_plan(
        self,
        business_info: Dict[str, Any],
        goals: List[str],
        budget: str = "medium"
    ) -> Dict[str, Any]:
        """
        Create a comprehensive AI search marketing plan.

        Args:
            business_info: Dictionary with business details
            goals: List of marketing goals
            budget: Budget level (low, medium, high)

        Returns:
            Marketing plan with strategy and tactics
        """
        self._log("Creating comprehensive marketing plan...")

        # Format business info
        business_desc = f"""
Business Name: {business_info.get('name', 'Unknown')}
Industry: {business_info.get('industry', 'Unknown')}
Target Audience: {business_info.get('target_audience', 'Unknown')}
Current Website: {business_info.get('website', 'Not provided')}
"""

        goals_str = "\n".join(f"- {g}" for g in goals)

        # Run marketing strategy agent
        strategy_query = f"""Create a comprehensive AI search marketing strategy:

{business_desc}

Goals:
{goals_str}

Budget Level: {budget}

Include content strategy, keyword strategy, competitive positioning, and implementation timeline."""

        strategy_result = self.run_agent(TaskType.MARKETING_STRATEGY, strategy_query)

        # Get keyword recommendations
        keyword_query = f"Research keywords for {business_info.get('industry', 'business')} targeting {business_info.get('target_audience', 'general audience')}"
        keyword_result = self.run_agent(TaskType.KEYWORD_RESEARCH, keyword_query)

        return {
            "business_info": business_info,
            "goals": goals,
            "budget": budget,
            "strategy": strategy_result,
            "keyword_recommendations": keyword_result,
        }

    def optimize_content(
        self,
        content: str,
        keywords: List[str] = None,
        target_platform: str = "all"
    ) -> Dict[str, Any]:
        """
        Optimize content for AI search visibility.

        Args:
            content: Content to optimize
            keywords: Target keywords
            target_platform: Target AI platform

        Returns:
            Content optimization recommendations
        """
        self._log("Optimizing content for AI search...")

        keywords_str = ", ".join(keywords) if keywords else "general relevance"

        # Content optimization
        content_query = f"""Optimize this content for AI search visibility:

Target Keywords: {keywords_str}
Target Platform: {target_platform}

Content:
{content[:5000]}
"""
        content_result = self.run_agent(TaskType.CONTENT_OPTIMIZATION, content_query)

        # Keyword density analysis
        if keywords:
            density_query = f"Analyze keyword density for keywords: {keywords_str}\n\nContent:\n{content[:3000]}"
            keyword_result = self.run_agent(TaskType.KEYWORD_RESEARCH, density_query)
        else:
            keyword_result = None

        return {
            "original_content_length": len(content),
            "target_keywords": keywords or [],
            "target_platform": target_platform,
            "optimization_analysis": content_result,
            "keyword_analysis": keyword_result,
        }

    def _synthesize_results(self, analyses: Dict[str, Any]) -> str:
        """
        Synthesize multiple analysis results into a summary.

        Args:
            analyses: Dictionary of analysis results

        Returns:
            Synthesized summary string
        """
        system_message = SystemMessage(content="""
You are an AI search optimization expert. Synthesize the following analysis results
into a concise, prioritized summary with top recommendations.

Focus on:
1. Most impactful quick wins
2. Critical issues to address
3. Long-term strategic priorities
4. Specific action items

Keep the summary focused and actionable.
""")

        # Format analyses for synthesis
        analyses_text = ""
        for analysis_type, result in analyses.items():
            if result and result.get("success"):
                analyses_text += f"\n\n=== {analysis_type.upper()} ANALYSIS ===\n"
                analyses_text += str(result.get("output", ""))[:2000]

        if not analyses_text:
            return "No successful analyses to synthesize."

        human_message = HumanMessage(content=f"Synthesize these analyses:\n{analyses_text}")

        response = self.coordinator_llm.invoke([system_message, human_message])

        return response.content

    def get_task_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of executed tasks.

        Returns:
            List of task history records
        """
        return [
            {
                "task_type": task.task_type.value,
                "completed": task.completed,
                "input_data": task.input_data,
                "has_result": task.result is not None,
            }
            for task in self.task_history
        ]

    def clear_history(self):
        """Clear the task history."""
        self.task_history = []

    def run(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        Run a natural language optimization task.

        Args:
            task: Natural language task description
            **kwargs: Additional context

        Returns:
            Task execution results
        """
        self._log(f"Processing task: {task}")

        # Analyze what agents to use
        agent_types = self.analyze_task(task)
        self._log(f"Using agents: {[t.value for t in agent_types]}")

        results = {
            "task": task,
            "agents_used": [t.value for t in agent_types],
            "results": {},
        }

        # Run each agent
        for task_type in agent_types:
            result = self.run_agent(task_type, task, **kwargs)
            results["results"][task_type.value] = result

        # Synthesize if multiple agents used
        if len(agent_types) > 1:
            results["summary"] = self._synthesize_results(results["results"])

        return results
