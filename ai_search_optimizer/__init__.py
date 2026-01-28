"""
AI Search Optimization Agent
============================

An agentic solution for AI search optimization using LangChain and Gemini LLM.
Designed for marketing platform optimization with intelligent SEO, content,
and keyword analysis capabilities.
"""

__version__ = "1.0.0"
__author__ = "AI Search Optimizer"

from ai_search_optimizer.config import Settings
from ai_search_optimizer.orchestrator import SearchOptimizationOrchestrator

__all__ = [
    "Settings",
    "SearchOptimizationOrchestrator",
]
