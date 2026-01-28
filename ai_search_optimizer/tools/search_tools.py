"""
LangChain Search Tools for AI Search Optimization.
Uses DuckDuckGo and other free search providers instead of paid APIs.
"""

import re
from typing import Optional, Dict, Any, List, ClassVar
from langchain_core.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup


class SearchInput(BaseModel):
    """Input schema for search."""
    query: str = Field(..., description="Search query")
    num_results: int = Field(default=5, description="Number of results to return")


class LangChainSearchTool(BaseTool):
    """
    LangChain-powered search tool using DuckDuckGo.
    Free alternative to paid search APIs.
    """

    name: str = "web_search"
    description: str = """
    Searches the web using DuckDuckGo through LangChain.
    Returns relevant search results for any query.

    Input: Search query string.
    Output: Search results with titles, snippets, and URLs.
    """
    args_schema: type = SearchInput

    def _run(self, query: str, num_results: int = 5) -> str:
        """Execute web search."""
        try:
            # Use DuckDuckGo search
            search = DuckDuckGoSearchRun()
            results = search.run(query)

            return f"""
=== WEB SEARCH RESULTS ===
Query: {query}

{results}
"""
        except Exception as e:
            return f"Search error: {str(e)}"


class WebsiteAnalyzerTool(BaseTool):
    """
    Comprehensive website analyzer for AI search optimization.
    Fetches and analyzes any website URL.
    """

    name: str = "website_analyzer"
    description: str = """
    Analyzes any website URL for AI search optimization:
    - Fetches live website content
    - Analyzes SEO factors
    - Evaluates AI search visibility
    - Provides optimization recommendations
    - Suggests MCP server configuration

    Input: Website URL to analyze.
    Output: Comprehensive optimization report with MCP recommendations.
    """

    def _run(self, url: str) -> str:
        """Analyze a website for AI search optimization."""
        try:
            # Fetch website content
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AISearchOptimizer/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract key elements
            analysis = self._analyze_website(soup, url)

            # Generate optimization recommendations
            recommendations = self._generate_recommendations(analysis)

            # Generate MCP server suggestion
            mcp_config = self._generate_mcp_suggestion(analysis, url)

            return self._format_report(analysis, recommendations, mcp_config)

        except requests.RequestException as e:
            return f"Error fetching website: {str(e)}"
        except Exception as e:
            return f"Analysis error: {str(e)}"

    def _analyze_website(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Analyze website structure and content."""

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""

        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else ""

        # Extract headers
        headers = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headers[f'h{i}'] = [h.get_text().strip()[:100] for h in h_tags[:5]]

        # Extract main content
        # Remove script, style, nav, footer
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            tag.decompose()

        text_content = soup.get_text(separator=' ', strip=True)
        words = text_content.split()

        # Check for structured data
        json_ld = soup.find_all('script', type='application/ld+json')

        # Check for FAQ sections
        faq_elements = soup.find_all(['details', 'summary'])
        faq_classes = soup.find_all(class_=re.compile(r'faq|accordion|question', re.I))

        # Check for lists
        lists = {
            'ul': len(soup.find_all('ul')),
            'ol': len(soup.find_all('ol')),
        }

        # Extract links
        links = soup.find_all('a', href=True)
        internal_links = sum(1 for l in links if url.split('/')[2] in l.get('href', ''))
        external_links = len(links) - internal_links

        # Check for images
        images = soup.find_all('img')
        images_with_alt = sum(1 for img in images if img.get('alt'))

        # Detect key patterns for AI optimization
        ai_patterns = {
            'has_definitions': bool(re.search(
                r'(is defined as|refers to|is a type of|means that)',
                text_content, re.I
            )),
            'has_questions': bool(re.search(r'\?', text_content)),
            'has_step_by_step': bool(re.search(
                r'(step \d|step-by-step|first,|second,|third,)',
                text_content, re.I
            )),
            'has_examples': bool(re.search(
                r'(for example|such as|for instance|e\.g\.|i\.e\.)',
                text_content, re.I
            )),
            'has_statistics': bool(re.search(
                r'\d+%|\d+ percent|\d+\s*(million|billion|thousand)',
                text_content, re.I
            )),
        }

        return {
            'url': url,
            'title': title,
            'title_length': len(title),
            'description': description,
            'description_length': len(description),
            'headers': headers,
            'word_count': len(words),
            'structured_data_count': len(json_ld),
            'has_faq': len(faq_elements) > 0 or len(faq_classes) > 0,
            'lists': lists,
            'internal_links': internal_links,
            'external_links': external_links,
            'total_images': len(images),
            'images_with_alt': images_with_alt,
            'ai_patterns': ai_patterns,
        }

    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate optimization recommendations."""
        recommendations = []

        # Title optimization
        if analysis['title_length'] < 30:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Title Tag',
                'issue': f"Title too short ({analysis['title_length']} chars)",
                'recommendation': "Expand title to 50-60 characters with primary keyword",
                'impact': "Improves click-through and AI understanding"
            })
        elif analysis['title_length'] > 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Title Tag',
                'issue': f"Title too long ({analysis['title_length']} chars)",
                'recommendation': "Shorten title to under 60 characters",
                'impact': "Prevents truncation in search results"
            })

        # Meta description
        if analysis['description_length'] < 120:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Meta Description',
                'issue': f"Description too short ({analysis['description_length']} chars)",
                'recommendation': "Expand to 150-160 characters with compelling copy",
                'impact': "Better click-through and AI context"
            })

        # Content length
        if analysis['word_count'] < 500:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Content Depth',
                'issue': f"Thin content ({analysis['word_count']} words)",
                'recommendation': "Expand content to 1500+ words for comprehensive coverage",
                'impact': "AI systems prefer detailed, authoritative content"
            })

        # Structured data
        if analysis['structured_data_count'] == 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Structured Data',
                'issue': "No JSON-LD structured data found",
                'recommendation': "Add schema.org markup (Article, FAQ, HowTo, etc.)",
                'impact': "Critical for AI understanding and rich results"
            })

        # FAQ section
        if not analysis['has_faq']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'FAQ Section',
                'issue': "No FAQ section detected",
                'recommendation': "Add FAQ section with common questions",
                'impact': "FAQs are heavily indexed by AI assistants"
            })

        # AI patterns
        patterns = analysis['ai_patterns']
        if not patterns['has_definitions']:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'AI Readability',
                'issue': "No clear definitions found",
                'recommendation': "Add explicit definitions using 'X is defined as' patterns",
                'impact': "AI systems cite clear definitions"
            })

        if not patterns['has_examples']:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'AI Readability',
                'issue': "No examples found",
                'recommendation': "Add examples using 'for example' or 'such as'",
                'impact': "Examples help AI provide better answers"
            })

        # Images
        if analysis['total_images'] > 0:
            alt_ratio = analysis['images_with_alt'] / analysis['total_images']
            if alt_ratio < 0.9:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Image Optimization',
                    'issue': f"Only {alt_ratio*100:.0f}% of images have alt text",
                    'recommendation': "Add descriptive alt text to all images",
                    'impact': "Improves accessibility and image search"
                })

        # Headers
        h1_count = len(analysis['headers'].get('h1', []))
        if h1_count == 0:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Header Structure',
                'issue': "No H1 tag found",
                'recommendation': "Add a single H1 tag with primary keyword",
                'impact': "Essential for page structure and SEO"
            })
        elif h1_count > 1:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Header Structure',
                'issue': f"Multiple H1 tags found ({h1_count})",
                'recommendation': "Use only one H1 tag per page",
                'impact': "Clearer page hierarchy for AI"
            })

        return recommendations

    def _generate_mcp_suggestion(self, analysis: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Generate MCP server configuration suggestion."""

        domain = url.split('/')[2]
        domain_name = domain.replace('www.', '').split('.')[0]

        # Determine content type based on analysis
        content_types = []
        if analysis['has_faq']:
            content_types.append('faq')
        if analysis['ai_patterns']['has_step_by_step']:
            content_types.append('tutorials')
        if analysis['structured_data_count'] > 0:
            content_types.append('structured_content')
        if analysis['word_count'] > 1000:
            content_types.append('articles')

        return {
            'server_name': f"{domain_name}-mcp-server",
            'description': f"MCP server for {domain} content optimization",
            'suggested_tools': [
                {
                    'name': f'search_{domain_name}',
                    'description': f'Search {domain} content and documentation',
                    'endpoint': f'{url}/search' if '/search' not in url else url
                },
                {
                    'name': f'get_{domain_name}_content',
                    'description': f'Fetch specific content from {domain}',
                    'endpoint': url
                },
                {
                    'name': f'get_{domain_name}_faq',
                    'description': f'Get FAQ content from {domain}',
                    'endpoint': f'{url}/faq'
                }
            ],
            'resources': [
                {
                    'name': f'{domain_name}://sitemap',
                    'description': 'Website sitemap for content discovery'
                },
                {
                    'name': f'{domain_name}://content/{{path}}',
                    'description': 'Dynamic content resource'
                }
            ],
            'content_types': content_types,
            'optimization_features': [
                'Content caching for faster AI queries',
                'Structured data extraction',
                'FAQ indexing for AI assistants',
                'Real-time content updates'
            ]
        }

    def _format_report(
        self,
        analysis: Dict[str, Any],
        recommendations: List[Dict[str, str]],
        mcp_config: Dict[str, Any]
    ) -> str:
        """Format the complete analysis report."""
        output = []

        output.append("=" * 70)
        output.append("WEBSITE AI SEARCH OPTIMIZATION REPORT")
        output.append("=" * 70)

        # Basic Info
        output.append(f"\nURL: {analysis['url']}")
        output.append(f"Title: {analysis['title'][:60]}...")
        output.append(f"Word Count: {analysis['word_count']}")

        # Score calculation
        score = self._calculate_score(analysis)
        output.append(f"\n{'='*30}")
        output.append(f"AI OPTIMIZATION SCORE: {score}/100")
        output.append(f"{'='*30}")

        # Current State Analysis
        output.append("\n--- CURRENT STATE ---")
        output.append(f"Title Length: {analysis['title_length']} chars " +
                     ("✓" if 50 <= analysis['title_length'] <= 60 else "⚠"))
        output.append(f"Meta Description: {analysis['description_length']} chars " +
                     ("✓" if 150 <= analysis['description_length'] <= 160 else "⚠"))
        output.append(f"Content Depth: {analysis['word_count']} words " +
                     ("✓" if analysis['word_count'] >= 1000 else "⚠"))
        output.append(f"Structured Data: {analysis['structured_data_count']} schemas " +
                     ("✓" if analysis['structured_data_count'] > 0 else "✗"))
        output.append(f"FAQ Section: {'Yes ✓' if analysis['has_faq'] else 'No ✗'}")

        # AI Patterns
        output.append("\n--- AI READABILITY PATTERNS ---")
        for pattern, present in analysis['ai_patterns'].items():
            status = "✓" if present else "✗"
            output.append(f"  {status} {pattern.replace('_', ' ').title()}")

        # Recommendations
        output.append("\n--- OPTIMIZATION RECOMMENDATIONS ---")
        high_priority = [r for r in recommendations if r['priority'] == 'HIGH']
        medium_priority = [r for r in recommendations if r['priority'] == 'MEDIUM']

        if high_priority:
            output.append("\n[HIGH PRIORITY]")
            for i, rec in enumerate(high_priority, 1):
                output.append(f"\n{i}. {rec['category']}")
                output.append(f"   Issue: {rec['issue']}")
                output.append(f"   Action: {rec['recommendation']}")
                output.append(f"   Impact: {rec['impact']}")

        if medium_priority:
            output.append("\n[MEDIUM PRIORITY]")
            for i, rec in enumerate(medium_priority, 1):
                output.append(f"\n{i}. {rec['category']}")
                output.append(f"   Issue: {rec['issue']}")
                output.append(f"   Action: {rec['recommendation']}")

        # MCP Server Configuration
        output.append("\n" + "=" * 70)
        output.append("MCP SERVER CONFIGURATION")
        output.append("=" * 70)
        output.append(f"\nServer Name: {mcp_config['server_name']}")
        output.append(f"Description: {mcp_config['description']}")

        output.append("\nSuggested Tools:")
        for tool in mcp_config['suggested_tools']:
            output.append(f"  • {tool['name']}: {tool['description']}")

        output.append("\nResources:")
        for resource in mcp_config['resources']:
            output.append(f"  • {resource['name']}: {resource['description']}")

        output.append("\nOptimization Features:")
        for feature in mcp_config['optimization_features']:
            output.append(f"  • {feature}")

        return "\n".join(output)

    def _calculate_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall AI optimization score."""
        score = 0

        # Title (15 points)
        if 50 <= analysis['title_length'] <= 60:
            score += 15
        elif 30 <= analysis['title_length'] <= 70:
            score += 10
        elif analysis['title_length'] > 0:
            score += 5

        # Description (15 points)
        if 150 <= analysis['description_length'] <= 160:
            score += 15
        elif 100 <= analysis['description_length'] <= 200:
            score += 10
        elif analysis['description_length'] > 0:
            score += 5

        # Content (20 points)
        if analysis['word_count'] >= 1500:
            score += 20
        elif analysis['word_count'] >= 800:
            score += 15
        elif analysis['word_count'] >= 300:
            score += 10

        # Structured data (15 points)
        if analysis['structured_data_count'] >= 2:
            score += 15
        elif analysis['structured_data_count'] >= 1:
            score += 10

        # FAQ (10 points)
        if analysis['has_faq']:
            score += 10

        # AI patterns (25 points, 5 each)
        for present in analysis['ai_patterns'].values():
            if present:
                score += 5

        return min(score, 100)
