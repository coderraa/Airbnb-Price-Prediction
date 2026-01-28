"""
Basic Usage Examples for AI Search Optimization Agent.

This file demonstrates the core functionality of the AI Search
Optimization Agent using LangChain and Gemini LLM.

Before running, ensure you have set your Google API key:
    export AI_SEARCH_GOOGLE_API_KEY="your-api-key"

Or create a .env file with:
    AI_SEARCH_GOOGLE_API_KEY=your-api-key
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Verify API key is set
if not os.getenv("AI_SEARCH_GOOGLE_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
    print("Warning: No Google API key found. Set AI_SEARCH_GOOGLE_API_KEY environment variable.")
    print("Example: export AI_SEARCH_GOOGLE_API_KEY='your-api-key'")


def example_1_seo_analysis():
    """
    Example 1: Analyze a URL for SEO optimization.
    """
    print("\n" + "="*60)
    print("Example 1: SEO Analysis")
    print("="*60)

    from ai_search_optimizer.agents import SEOAgent

    # Initialize the SEO agent
    agent = SEOAgent(verbose=True)

    # Analyze a URL
    result = agent.analyze_url(
        url="https://example.com",
    )

    if result["success"]:
        print("\nSEO Analysis Results:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


def example_2_keyword_research():
    """
    Example 2: Research keywords for a topic.
    """
    print("\n" + "="*60)
    print("Example 2: Keyword Research")
    print("="*60)

    from ai_search_optimizer.agents import KeywordResearchAgent

    # Initialize the keyword research agent
    agent = KeywordResearchAgent(verbose=True)

    # Research keywords for a topic
    result = agent.research_keywords(
        topic="AI marketing automation",
        industry="SaaS"
    )

    if result["success"]:
        print("\nKeyword Research Results:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


def example_3_content_optimization():
    """
    Example 3: Optimize content for AI search.
    """
    print("\n" + "="*60)
    print("Example 3: Content Optimization")
    print("="*60)

    from ai_search_optimizer.agents import ContentOptimizationAgent

    # Sample content to optimize
    sample_content = """
    Marketing automation is a technology that manages marketing processes
    and campaigns across multiple channels. It helps businesses target
    customers with automated messages across email, web, social, and text.

    Benefits of marketing automation include improved efficiency, better
    lead nurturing, and increased revenue. Many companies use marketing
    automation to streamline their marketing efforts.
    """

    # Initialize the content optimization agent
    agent = ContentOptimizationAgent(verbose=True)

    # Optimize the content
    result = agent.optimize_content(
        content=sample_content,
        keywords=["marketing automation", "lead nurturing"],
        target_platform="chatgpt"
    )

    if result["success"]:
        print("\nContent Optimization Results:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


def example_4_competitor_analysis():
    """
    Example 4: Analyze competitor content.
    """
    print("\n" + "="*60)
    print("Example 4: Competitor Analysis")
    print("="*60)

    from ai_search_optimizer.agents import CompetitorAnalysisAgent

    # Initialize the competitor analysis agent
    agent = CompetitorAnalysisAgent(verbose=True)

    # Analyze competitors
    result = agent.analyze_competitors(
        competitor_urls=[
            "https://example.com/competitor1",
            "https://example.com/competitor2",
        ],
        target_keywords=["AI marketing", "automation platform"]
    )

    if result["success"]:
        print("\nCompetitor Analysis Results:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


def example_5_marketing_strategy():
    """
    Example 5: Create a marketing strategy.
    """
    print("\n" + "="*60)
    print("Example 5: Marketing Strategy")
    print("="*60)

    from ai_search_optimizer.agents import MarketingStrategyAgent

    # Initialize the marketing strategy agent
    agent = MarketingStrategyAgent(verbose=True)

    # Create a marketing strategy
    result = agent.create_ai_marketing_strategy(
        business_name="TechStartup AI",
        business_description="AI-powered analytics platform for e-commerce",
        target_audience="E-commerce business owners and marketers",
        goals=[
            "Increase organic traffic by 50%",
            "Get cited by AI assistants",
            "Establish thought leadership"
        ],
        budget_level="medium"
    )

    if result["success"]:
        print("\nMarketing Strategy Results:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


def example_6_orchestrator():
    """
    Example 6: Use the orchestrator for comprehensive analysis.
    """
    print("\n" + "="*60)
    print("Example 6: Orchestrator (Comprehensive Analysis)")
    print("="*60)

    from ai_search_optimizer.orchestrator import SearchOptimizationOrchestrator

    # Initialize the orchestrator
    orchestrator = SearchOptimizationOrchestrator(verbose=True)

    # Run a natural language task
    result = orchestrator.run(
        "Help me optimize my SaaS product page for AI search visibility"
    )

    print("\nAgents Used:", result.get("agents_used"))

    for agent_type, agent_result in result.get("results", {}).items():
        if agent_result.get("success"):
            print(f"\n--- {agent_type} ---")
            print(agent_result.get("output", "")[:500] + "...")

    if "summary" in result:
        print("\n--- SUMMARY ---")
        print(result["summary"])


def example_7_url_optimization():
    """
    Example 7: Comprehensive URL optimization with the orchestrator.
    """
    print("\n" + "="*60)
    print("Example 7: Comprehensive URL Optimization")
    print("="*60)

    from ai_search_optimizer.orchestrator import SearchOptimizationOrchestrator

    # Initialize the orchestrator
    orchestrator = SearchOptimizationOrchestrator(verbose=True)

    # Perform comprehensive URL optimization
    result = orchestrator.optimize_url(
        url="https://example.com/product",
        keywords=["AI analytics", "e-commerce insights"],
        include_competitors=["https://competitor1.com", "https://competitor2.com"]
    )

    print("\nAnalyses performed:")
    for analysis_type in result.get("analyses", {}).keys():
        print(f"  - {analysis_type}")

    if "summary" in result:
        print("\n--- SUMMARY ---")
        print(result["summary"])


if __name__ == "__main__":
    print("AI Search Optimization - Basic Usage Examples")
    print("=" * 60)

    # Run examples (comment out ones you don't want to run)
    # Note: These require a valid Google API key

    print("\nSelect an example to run:")
    print("1. SEO Analysis")
    print("2. Keyword Research")
    print("3. Content Optimization")
    print("4. Competitor Analysis")
    print("5. Marketing Strategy")
    print("6. Orchestrator (Natural Language)")
    print("7. Comprehensive URL Optimization")
    print("0. Run all examples")

    choice = input("\nEnter choice (0-7): ").strip()

    examples = {
        "1": example_1_seo_analysis,
        "2": example_2_keyword_research,
        "3": example_3_content_optimization,
        "4": example_4_competitor_analysis,
        "5": example_5_marketing_strategy,
        "6": example_6_orchestrator,
        "7": example_7_url_optimization,
    }

    if choice == "0":
        for func in examples.values():
            try:
                func()
            except Exception as e:
                print(f"Error running example: {e}")
    elif choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error running example: {e}")
    else:
        print("Invalid choice")
