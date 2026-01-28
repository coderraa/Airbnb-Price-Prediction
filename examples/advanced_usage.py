"""
Advanced Usage Examples for AI Search Optimization Agent.

This file demonstrates advanced features including:
- Custom agent configurations
- Tool usage
- Async operations
- Caching
- Custom workflows
"""

import asyncio
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


async def example_async_operations():
    """
    Example: Asynchronous agent operations.
    """
    print("\n" + "="*60)
    print("Async Operations Example")
    print("="*60)

    from ai_search_optimizer.agents import (
        SEOAgent,
        KeywordResearchAgent,
        ContentOptimizationAgent,
    )

    # Initialize agents
    seo_agent = SEOAgent(verbose=False)
    keyword_agent = KeywordResearchAgent(verbose=False)
    content_agent = ContentOptimizationAgent(verbose=False)

    # Run analyses in parallel
    tasks = [
        seo_agent.arun("Analyze SEO best practices for AI visibility"),
        keyword_agent.arun("Research keywords for 'AI marketing tools'"),
        content_agent.arun("What makes content AI-friendly?"),
    ]

    print("Running 3 agents in parallel...")
    results = await asyncio.gather(*tasks)

    for i, result in enumerate(results):
        agent_names = ["SEO", "Keyword", "Content"]
        if result["success"]:
            print(f"\n{agent_names[i]} Agent completed successfully")
            print(f"Output preview: {result['output'][:200]}...")
        else:
            print(f"\n{agent_names[i]} Agent failed: {result.get('error')}")


def example_custom_tools():
    """
    Example: Using individual tools directly.
    """
    print("\n" + "="*60)
    print("Direct Tool Usage Example")
    print("="*60)

    from ai_search_optimizer.tools import (
        SEOAnalyzerTool,
        KeywordResearchTool,
        ContentOptimizerTool,
        AIVisibilityTool,
    )

    # Use SEO Analyzer directly
    seo_tool = SEOAnalyzerTool()
    print("\n--- SEO Analyzer Tool ---")
    result = seo_tool._run(
        content="AI marketing automation helps businesses scale their marketing efforts efficiently.",
        target_keywords=["AI marketing", "automation"]
    )
    print(result[:500])

    # Use Keyword Research directly
    keyword_tool = KeywordResearchTool()
    print("\n--- Keyword Research Tool ---")
    result = keyword_tool._run(topic="machine learning for marketers")
    print(result[:500])

    # Use AI Visibility Tool directly
    visibility_tool = AIVisibilityTool()
    print("\n--- AI Visibility Tool ---")
    sample_content = """
    Machine learning for marketers is transforming how businesses understand
    their customers. By leveraging AI-powered analytics, marketers can predict
    customer behavior and personalize campaigns at scale.

    Key benefits include:
    - Improved targeting accuracy
    - Automated campaign optimization
    - Real-time performance insights

    How does machine learning help marketers?
    Machine learning algorithms analyze vast amounts of data to identify
    patterns that humans might miss. This enables more effective marketing
    strategies and higher ROI.
    """
    result = visibility_tool._run(content=sample_content, topic="machine learning marketing")
    print(result)


def example_caching():
    """
    Example: Using the cache manager.
    """
    print("\n" + "="*60)
    print("Caching Example")
    print("="*60)

    from ai_search_optimizer.utils import CacheManager

    # Initialize cache
    cache = CacheManager(cache_dir=".cache/examples", ttl=3600)

    # Store some data
    cache.set(
        {"analysis": "Sample SEO analysis results", "score": 85},
        "seo", "example.com"
    )
    print("Data cached successfully")

    # Retrieve data
    cached_data = cache.get("seo", "example.com")
    if cached_data:
        print(f"Retrieved from cache: {cached_data}")
    else:
        print("Cache miss")

    # Get cache stats
    stats = cache.get_stats()
    print(f"\nCache Statistics:")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Valid entries: {stats['valid_entries']}")
    print(f"  Size: {stats['total_size_mb']} MB")


def example_custom_workflow():
    """
    Example: Building a custom optimization workflow.
    """
    print("\n" + "="*60)
    print("Custom Workflow Example")
    print("="*60)

    from ai_search_optimizer.agents import (
        SEOAgent,
        KeywordResearchAgent,
        ContentOptimizationAgent,
    )
    from ai_search_optimizer.utils import format_report

    class OptimizationWorkflow:
        """Custom workflow for comprehensive optimization."""

        def __init__(self):
            self.seo_agent = SEOAgent(verbose=False)
            self.keyword_agent = KeywordResearchAgent(verbose=False)
            self.content_agent = ContentOptimizationAgent(verbose=False)
            self.results = {}

        def run_analysis(self, content: str, topic: str) -> Dict[str, Any]:
            """Run comprehensive analysis workflow."""
            print("Step 1/3: Running keyword research...")
            self.results["keywords"] = self.keyword_agent.run(
                f"Research keywords for: {topic}"
            )

            print("Step 2/3: Running content analysis...")
            self.results["content"] = self.content_agent.run(
                f"Analyze this content for AI optimization:\n\n{content[:2000]}"
            )

            print("Step 3/3: Running SEO analysis...")
            self.results["seo"] = self.seo_agent.run(
                f"Analyze SEO factors for content about: {topic}"
            )

            return self.generate_report()

        def generate_report(self) -> Dict[str, Any]:
            """Generate a combined report."""
            sections = []

            for analysis_type, result in self.results.items():
                if result.get("success"):
                    sections.append({
                        "heading": analysis_type.upper(),
                        "content": result.get("output", "")[:500] + "..."
                    })

            report = format_report(
                title="OPTIMIZATION ANALYSIS REPORT",
                sections=sections
            )

            return {
                "success": True,
                "report": report,
                "raw_results": self.results
            }

    # Run the custom workflow
    workflow = OptimizationWorkflow()
    sample_content = """
    Our AI-powered analytics platform helps e-commerce businesses
    understand customer behavior and optimize their marketing strategies.
    With machine learning algorithms, we provide real-time insights
    and predictive analytics that drive revenue growth.
    """

    result = workflow.run_analysis(
        content=sample_content,
        topic="AI analytics for e-commerce"
    )

    print("\n" + result["report"])


def example_multi_platform_optimization():
    """
    Example: Optimize content for multiple AI platforms.
    """
    print("\n" + "="*60)
    print("Multi-Platform Optimization Example")
    print("="*60)

    from ai_search_optimizer.agents import ContentOptimizationAgent

    agent = ContentOptimizationAgent(verbose=False)

    sample_content = """
    Cloud computing services enable businesses to access computing resources
    over the internet. Instead of owning and maintaining physical servers,
    companies can rent computing power from cloud providers like AWS, Azure,
    or Google Cloud.

    Benefits of cloud computing:
    - Cost savings through pay-as-you-go pricing
    - Scalability to handle varying workloads
    - Improved reliability with redundant systems
    - Access from anywhere with internet connection
    """

    platforms = ["chatgpt", "perplexity", "claude", "google"]

    print(f"\nAnalyzing content optimization for {len(platforms)} platforms...\n")

    for platform in platforms:
        print(f"\n--- Optimizing for {platform.upper()} ---")
        result = agent.optimize_content(
            content=sample_content,
            keywords=["cloud computing", "cloud services"],
            target_platform=platform
        )

        if result["success"]:
            # Show a brief summary
            output = result["output"]
            lines = output.split("\n")[:10]
            print("\n".join(lines))
            print("...")
        else:
            print(f"Error: {result.get('error')}")


def example_content_gap_analysis():
    """
    Example: Identify content gaps vs competitors.
    """
    print("\n" + "="*60)
    print("Content Gap Analysis Example")
    print("="*60)

    from ai_search_optimizer.agents import CompetitorAnalysisAgent

    agent = CompetitorAnalysisAgent(verbose=False)

    # Analyze content gaps
    result = agent.identify_content_gaps(
        your_url="https://example.com/my-product",
        competitor_urls=[
            "https://competitor1.com/product",
            "https://competitor2.com/product"
        ],
        topic="AI marketing automation"
    )

    if result["success"]:
        print("\nContent Gap Analysis Results:")
        print(result["output"][:1500])
    else:
        print(f"Error: {result.get('error')}")


def example_faq_generation():
    """
    Example: Generate AI-optimized FAQ section.
    """
    print("\n" + "="*60)
    print("FAQ Generation Example")
    print("="*60)

    from ai_search_optimizer.agents import ContentOptimizationAgent

    agent = ContentOptimizationAgent(verbose=False)

    existing_content = """
    Email marketing automation helps businesses send targeted messages
    to their subscribers based on behavior, preferences, and engagement.
    It includes features like drip campaigns, segmentation, A/B testing,
    and analytics tracking.
    """

    result = agent.create_faq_section(
        topic="email marketing automation",
        existing_content=existing_content
    )

    if result["success"]:
        print("\nGenerated FAQ Section:")
        print(result["output"])
    else:
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    print("AI Search Optimization - Advanced Usage Examples")
    print("=" * 60)

    print("\nSelect an example to run:")
    print("1. Async Operations")
    print("2. Direct Tool Usage")
    print("3. Caching")
    print("4. Custom Workflow")
    print("5. Multi-Platform Optimization")
    print("6. Content Gap Analysis")
    print("7. FAQ Generation")

    choice = input("\nEnter choice (1-7): ").strip()

    examples = {
        "1": lambda: asyncio.run(example_async_operations()),
        "2": example_custom_tools,
        "3": example_caching,
        "4": example_custom_workflow,
        "5": example_multi_platform_optimization,
        "6": example_content_gap_analysis,
        "7": example_faq_generation,
    }

    if choice in examples:
        try:
            examples[choice]()
        except Exception as e:
            print(f"Error running example: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice")
