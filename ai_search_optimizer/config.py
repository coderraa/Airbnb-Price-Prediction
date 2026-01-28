"""
Configuration settings for AI Search Optimization Agent.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Gemini Configuration
    google_api_key: str = Field(
        default="",
        description="Google API key for Gemini LLM"
    )
    gemini_model: str = Field(
        default="gemini-1.5-pro",
        description="Gemini model to use"
    )
    gemini_temperature: float = Field(
        default=0.7,
        description="Temperature for Gemini responses"
    )
    gemini_max_tokens: int = Field(
        default=4096,
        description="Maximum tokens for Gemini responses"
    )

    # Search API Configuration
    serpapi_key: Optional[str] = Field(
        default=None,
        description="SerpAPI key for search results"
    )

    # Agent Configuration
    max_iterations: int = Field(
        default=10,
        description="Maximum iterations for agent loops"
    )
    verbose: bool = Field(
        default=True,
        description="Enable verbose logging"
    )

    # Caching Configuration
    cache_enabled: bool = Field(
        default=True,
        description="Enable response caching"
    )
    cache_ttl: int = Field(
        default=3600,
        description="Cache TTL in seconds"
    )
    cache_dir: str = Field(
        default=".cache/ai_search_optimizer",
        description="Cache directory path"
    )

    # Rate Limiting
    requests_per_minute: int = Field(
        default=60,
        description="Rate limit for API requests"
    )

    # Content Analysis
    min_content_length: int = Field(
        default=100,
        description="Minimum content length for analysis"
    )
    max_keywords: int = Field(
        default=20,
        description="Maximum keywords to extract"
    )

    # Target Platforms for Optimization
    target_platforms: List[str] = Field(
        default=["google", "bing", "chatgpt", "perplexity", "claude"],
        description="AI platforms to optimize for"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "AI_SEARCH_"
        extra = "ignore"


class AgentConfig:
    """Configuration for individual agents."""

    SEO_AGENT = {
        "name": "SEO Analyst",
        "description": "Analyzes and optimizes content for search engines",
        "max_iterations": 5,
    }

    KEYWORD_AGENT = {
        "name": "Keyword Researcher",
        "description": "Researches and suggests optimal keywords",
        "max_iterations": 5,
    }

    CONTENT_AGENT = {
        "name": "Content Optimizer",
        "description": "Optimizes content for AI search visibility",
        "max_iterations": 5,
    }

    COMPETITOR_AGENT = {
        "name": "Competitor Analyst",
        "description": "Analyzes competitor strategies and positioning",
        "max_iterations": 5,
    }

    MARKETING_AGENT = {
        "name": "Marketing Strategist",
        "description": "Develops AI-optimized marketing strategies",
        "max_iterations": 5,
    }


# Global settings instance
settings = Settings()
