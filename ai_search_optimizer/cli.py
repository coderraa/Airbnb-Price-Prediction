"""
Command Line Interface for AI Search Optimization.

Usage:
    python -m ai_search_optimizer.cli analyze-url https://example.com
    python -m ai_search_optimizer.cli research-keywords "AI marketing"
    python -m ai_search_optimizer.cli optimize-content content.txt
"""

import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from ai_search_optimizer.orchestrator import SearchOptimizationOrchestrator
from ai_search_optimizer.agents import (
    SEOAgent,
    KeywordResearchAgent,
    ContentOptimizationAgent,
    CompetitorAnalysisAgent,
    MarketingStrategyAgent,
)
from ai_search_optimizer.config import settings

# Initialize CLI app
app = typer.Typer(
    name="ai-search-optimizer",
    help="AI Search Optimization CLI - Optimize your content for AI-powered search",
    add_completion=False,
)

console = Console()


def print_header():
    """Print the CLI header."""
    console.print(Panel.fit(
        "[bold blue]AI Search Optimization Agent[/bold blue]\n"
        "[dim]Powered by LangChain & Gemini[/dim]",
        border_style="blue"
    ))


def print_result(result: dict, title: str = "Results"):
    """Print formatted results."""
    if result.get("success"):
        console.print(f"\n[green]✓ {title}[/green]")
        output = result.get("output", "")
        if output:
            console.print(Panel(output, title=title, border_style="green"))
    else:
        console.print(f"\n[red]✗ Error[/red]")
        console.print(f"[red]{result.get('error', 'Unknown error')}[/red]")


@app.command()
def analyze_url(
    url: str = typer.Argument(..., help="URL to analyze"),
    keywords: Optional[str] = typer.Option(
        None, "--keywords", "-k",
        help="Comma-separated target keywords"
    ),
    competitors: Optional[str] = typer.Option(
        None, "--competitors", "-c",
        help="Comma-separated competitor URLs"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """
    Analyze a URL for AI search optimization.

    Performs comprehensive SEO and content analysis optimized for
    AI-powered search platforms.
    """
    print_header()

    keyword_list = [k.strip() for k in keywords.split(",")] if keywords else None
    competitor_list = [c.strip() for c in competitors.split(",")] if competitors else None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Analyzing URL...", total=None)

        orchestrator = SearchOptimizationOrchestrator(verbose=verbose)
        results = orchestrator.optimize_url(
            url=url,
            keywords=keyword_list,
            include_competitors=competitor_list,
        )

    # Display results
    console.print(f"\n[bold]Analysis Results for: {url}[/bold]")

    for analysis_type, result in results.get("analyses", {}).items():
        print_result(result, f"{analysis_type.upper()} Analysis")

    if "summary" in results:
        console.print(Panel(
            results["summary"],
            title="[bold]Summary & Recommendations[/bold]",
            border_style="cyan"
        ))


@app.command()
def research_keywords(
    topic: str = typer.Argument(..., help="Topic for keyword research"),
    industry: Optional[str] = typer.Option(
        None, "--industry", "-i",
        help="Industry context"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """
    Research keywords for AI search optimization.

    Generates keyword suggestions optimized for AI-powered search
    platforms including ChatGPT, Perplexity, and Claude.
    """
    print_header()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Researching keywords...", total=None)

        agent = KeywordResearchAgent(verbose=verbose)
        result = agent.research_keywords(topic=topic, industry=industry)

    print_result(result, "Keyword Research")


@app.command()
def optimize_content(
    content_file: Path = typer.Argument(
        ...,
        help="Path to content file",
        exists=True,
    ),
    keywords: Optional[str] = typer.Option(
        None, "--keywords", "-k",
        help="Comma-separated target keywords"
    ),
    platform: str = typer.Option(
        "all", "--platform", "-p",
        help="Target platform (chatgpt, perplexity, claude, google, all)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """
    Optimize content for AI search visibility.

    Analyzes and provides recommendations for optimizing content
    to be discovered and cited by AI assistants.
    """
    print_header()

    # Read content file
    content = content_file.read_text()
    keyword_list = [k.strip() for k in keywords.split(",")] if keywords else None

    console.print(f"[dim]Content length: {len(content)} characters[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Optimizing content...", total=None)

        agent = ContentOptimizationAgent(verbose=verbose)
        result = agent.optimize_content(
            content=content,
            keywords=keyword_list,
            target_platform=platform,
        )

    print_result(result, "Content Optimization")


@app.command()
def analyze_competitors(
    urls: str = typer.Argument(..., help="Comma-separated competitor URLs"),
    keywords: Optional[str] = typer.Option(
        None, "--keywords", "-k",
        help="Comma-separated target keywords"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """
    Analyze competitor content strategies.

    Provides insights into competitor AI optimization tactics
    and identifies differentiation opportunities.
    """
    print_header()

    url_list = [u.strip() for u in urls.split(",")]
    keyword_list = [k.strip() for k in keywords.split(",")] if keywords else None

    console.print(f"[dim]Analyzing {len(url_list)} competitors[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Analyzing competitors...", total=None)

        agent = CompetitorAnalysisAgent(verbose=verbose)
        result = agent.analyze_competitors(
            competitor_urls=url_list,
            target_keywords=keyword_list,
        )

    print_result(result, "Competitor Analysis")


@app.command()
def create_strategy(
    business_name: str = typer.Argument(..., help="Business name"),
    industry: str = typer.Option(
        ..., "--industry", "-i",
        help="Business industry"
    ),
    audience: str = typer.Option(
        ..., "--audience", "-a",
        help="Target audience description"
    ),
    goals: str = typer.Option(
        ..., "--goals", "-g",
        help="Comma-separated marketing goals"
    ),
    budget: str = typer.Option(
        "medium", "--budget", "-b",
        help="Budget level (low, medium, high)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v",
        help="Enable verbose output"
    ),
):
    """
    Create an AI search marketing strategy.

    Develops a comprehensive marketing strategy optimized for
    AI-powered search discovery and citation.
    """
    print_header()

    goal_list = [g.strip() for g in goals.split(",")]

    console.print(f"[dim]Creating strategy for: {business_name}[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task("Creating marketing strategy...", total=None)

        orchestrator = SearchOptimizationOrchestrator(verbose=verbose)
        results = orchestrator.create_marketing_plan(
            business_info={
                "name": business_name,
                "industry": industry,
                "target_audience": audience,
            },
            goals=goal_list,
            budget=budget,
        )

    # Display results
    print_result(results.get("strategy", {}), "Marketing Strategy")
    print_result(results.get("keyword_recommendations", {}), "Keyword Recommendations")


@app.command()
def interactive():
    """
    Start interactive mode.

    Allows natural language queries to the AI search optimization system.
    """
    print_header()

    console.print("\n[bold]Interactive Mode[/bold]")
    console.print("[dim]Enter your queries or 'quit' to exit[/dim]\n")

    orchestrator = SearchOptimizationOrchestrator(verbose=False)

    while True:
        try:
            query = console.input("[bold blue]> [/bold blue]")

            if query.lower() in ("quit", "exit", "q"):
                console.print("\n[dim]Goodbye![/dim]")
                break

            if not query.strip():
                continue

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                progress.add_task("Processing...", total=None)
                result = orchestrator.run(query)

            # Display results
            for agent_type, agent_result in result.get("results", {}).items():
                if agent_result.get("success"):
                    console.print(Panel(
                        agent_result.get("output", ""),
                        title=f"[bold]{agent_type}[/bold]",
                        border_style="green"
                    ))

            if "summary" in result:
                console.print(Panel(
                    result["summary"],
                    title="[bold]Summary[/bold]",
                    border_style="cyan"
                ))

            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Goodbye![/dim]")
            break


@app.command()
def version():
    """Show version information."""
    from ai_search_optimizer import __version__
    console.print(f"AI Search Optimizer v{__version__}")
    console.print(f"Model: {settings.gemini_model}")


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
