"""
SEO Analysis Tools for AI Search Optimization.
"""

import re
from typing import Optional, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup


class SEOAnalysisInput(BaseModel):
    """Input schema for SEO analysis."""
    url: Optional[str] = Field(None, description="URL to analyze")
    content: Optional[str] = Field(None, description="Content to analyze")
    target_keywords: Optional[List[str]] = Field(
        default=None,
        description="Target keywords to check"
    )


class SEOAnalyzerTool(BaseTool):
    """
    Comprehensive SEO analysis tool that evaluates content
    for search engine optimization factors.
    """

    name: str = "seo_analyzer"
    description: str = """
    Analyzes content or URL for SEO factors including:
    - Title tag optimization
    - Meta description quality
    - Header structure (H1-H6)
    - Keyword presence and density
    - Content length and quality signals
    - Internal/external link analysis
    - Image alt text optimization

    Input: URL or content text with optional target keywords.
    Output: Detailed SEO analysis report with scores and recommendations.
    """
    args_schema: type = SEOAnalysisInput

    def _run(
        self,
        url: Optional[str] = None,
        content: Optional[str] = None,
        target_keywords: Optional[List[str]] = None
    ) -> str:
        """Execute SEO analysis."""
        try:
            if url:
                analysis = self._analyze_url(url, target_keywords)
            elif content:
                analysis = self._analyze_content(content, target_keywords)
            else:
                return "Error: Please provide either a URL or content to analyze."

            return self._format_analysis(analysis)
        except Exception as e:
            return f"Error during SEO analysis: {str(e)}"

    def _analyze_url(
        self,
        url: str,
        target_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze a URL for SEO factors."""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; SEOBot/1.0)'
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            analysis = {
                "url": url,
                "status_code": response.status_code,
                "title": self._extract_title(soup),
                "meta_description": self._extract_meta_description(soup),
                "headers": self._analyze_headers(soup),
                "word_count": self._count_words(soup),
                "links": self._analyze_links(soup, url),
                "images": self._analyze_images(soup),
                "keyword_analysis": self._keyword_analysis(
                    soup.get_text(), target_keywords
                ) if target_keywords else None,
            }

            analysis["score"] = self._calculate_seo_score(analysis)
            return analysis

        except requests.RequestException as e:
            return {"error": f"Failed to fetch URL: {str(e)}"}

    def _analyze_content(
        self,
        content: str,
        target_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze raw content for SEO factors."""
        word_count = len(content.split())

        analysis = {
            "content_type": "raw_text",
            "word_count": word_count,
            "sentence_count": len(re.findall(r'[.!?]+', content)),
            "paragraph_count": len(content.split('\n\n')),
            "keyword_analysis": self._keyword_analysis(
                content, target_keywords
            ) if target_keywords else None,
            "readability": self._basic_readability(content),
        }

        analysis["score"] = self._calculate_content_score(analysis)
        return analysis

    def _extract_title(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract and analyze title tag."""
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""
        return {
            "text": title,
            "length": len(title),
            "optimal": 50 <= len(title) <= 60,
        }

    def _extract_meta_description(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract and analyze meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        description = meta['content'].strip() if meta and meta.get('content') else ""
        return {
            "text": description,
            "length": len(description),
            "optimal": 150 <= len(description) <= 160,
        }

    def _analyze_headers(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze header structure."""
        headers = {}
        for i in range(1, 7):
            h_tags = soup.find_all(f'h{i}')
            headers[f'h{i}'] = {
                "count": len(h_tags),
                "texts": [h.get_text().strip()[:100] for h in h_tags[:5]]
            }
        return headers

    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in page content."""
        text = soup.get_text()
        return len(text.split())

    def _analyze_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Analyze internal and external links."""
        from urllib.parse import urlparse

        links = soup.find_all('a', href=True)
        base_domain = urlparse(base_url).netloc

        internal = 0
        external = 0

        for link in links:
            href = link['href']
            if href.startswith('/') or base_domain in href:
                internal += 1
            elif href.startswith('http'):
                external += 1

        return {
            "total": len(links),
            "internal": internal,
            "external": external,
        }

    def _analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze images and alt text."""
        images = soup.find_all('img')
        with_alt = sum(1 for img in images if img.get('alt'))

        return {
            "total": len(images),
            "with_alt": with_alt,
            "without_alt": len(images) - with_alt,
            "alt_ratio": with_alt / len(images) if images else 1.0,
        }

    def _keyword_analysis(
        self,
        text: str,
        keywords: List[str]
    ) -> Dict[str, Any]:
        """Analyze keyword presence and density."""
        text_lower = text.lower()
        word_count = len(text.split())

        results = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            density = (count / word_count * 100) if word_count > 0 else 0

            results[keyword] = {
                "count": count,
                "density": round(density, 2),
                "in_first_100_words": keyword_lower in ' '.join(
                    text.split()[:100]
                ).lower(),
            }

        return results

    def _basic_readability(self, text: str) -> Dict[str, Any]:
        """Calculate basic readability metrics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip()]

        avg_word_length = sum(len(w) for w in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0

        return {
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2),
            "complexity": "high" if avg_sentence_length > 20 else "medium" if avg_sentence_length > 15 else "low",
        }

    def _calculate_seo_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate overall SEO score."""
        score = 0
        max_score = 100

        # Title optimization (20 points)
        if analysis.get("title", {}).get("optimal"):
            score += 20
        elif analysis.get("title", {}).get("text"):
            score += 10

        # Meta description (20 points)
        if analysis.get("meta_description", {}).get("optimal"):
            score += 20
        elif analysis.get("meta_description", {}).get("text"):
            score += 10

        # Headers (15 points)
        headers = analysis.get("headers", {})
        if headers.get("h1", {}).get("count") == 1:
            score += 10
        if headers.get("h2", {}).get("count", 0) >= 2:
            score += 5

        # Content length (15 points)
        word_count = analysis.get("word_count", 0)
        if word_count >= 1500:
            score += 15
        elif word_count >= 800:
            score += 10
        elif word_count >= 300:
            score += 5

        # Images (15 points)
        images = analysis.get("images", {})
        if images.get("alt_ratio", 0) >= 0.9:
            score += 15
        elif images.get("alt_ratio", 0) >= 0.7:
            score += 10

        # Links (15 points)
        links = analysis.get("links", {})
        if links.get("internal", 0) >= 3:
            score += 8
        if links.get("external", 0) >= 1:
            score += 7

        return min(score, max_score)

    def _calculate_content_score(self, analysis: Dict[str, Any]) -> int:
        """Calculate content quality score."""
        score = 50  # Base score

        word_count = analysis.get("word_count", 0)
        if word_count >= 1000:
            score += 20
        elif word_count >= 500:
            score += 10

        readability = analysis.get("readability", {})
        if readability.get("complexity") == "medium":
            score += 15
        elif readability.get("complexity") == "low":
            score += 10

        if analysis.get("keyword_analysis"):
            score += 15

        return min(score, 100)

    def _format_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format analysis results as readable string."""
        if "error" in analysis:
            return f"Analysis Error: {analysis['error']}"

        output = []
        output.append("=" * 50)
        output.append("SEO ANALYSIS REPORT")
        output.append("=" * 50)

        if "url" in analysis:
            output.append(f"\nURL: {analysis['url']}")
            output.append(f"Status: {analysis.get('status_code', 'N/A')}")

        output.append(f"\nOverall SEO Score: {analysis.get('score', 'N/A')}/100")

        if "title" in analysis:
            title = analysis["title"]
            output.append(f"\n--- Title Tag ---")
            output.append(f"Text: {title.get('text', 'N/A')[:60]}...")
            output.append(f"Length: {title.get('length', 0)} chars")
            output.append(f"Optimal: {'Yes' if title.get('optimal') else 'No'}")

        if "meta_description" in analysis:
            meta = analysis["meta_description"]
            output.append(f"\n--- Meta Description ---")
            output.append(f"Length: {meta.get('length', 0)} chars")
            output.append(f"Optimal: {'Yes' if meta.get('optimal') else 'No'}")

        output.append(f"\nWord Count: {analysis.get('word_count', 'N/A')}")

        if "keyword_analysis" in analysis and analysis["keyword_analysis"]:
            output.append(f"\n--- Keyword Analysis ---")
            for kw, data in analysis["keyword_analysis"].items():
                output.append(
                    f"  {kw}: {data['count']} occurrences "
                    f"({data['density']}% density)"
                )

        return "\n".join(output)


class MetaTagAnalyzerTool(BaseTool):
    """Tool for analyzing meta tags for AI search optimization."""

    name: str = "meta_tag_analyzer"
    description: str = """
    Analyzes meta tags for AI search optimization including:
    - Open Graph tags for social/AI sharing
    - Twitter Card meta tags
    - Schema.org structured data
    - Canonical URLs
    - Robot directives

    Input: URL to analyze.
    Output: Meta tag analysis with AI optimization recommendations.
    """

    def _run(self, url: str) -> str:
        """Analyze meta tags for the given URL."""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; MetaBot/1.0)'
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            meta_analysis = {
                "open_graph": self._analyze_og_tags(soup),
                "twitter_cards": self._analyze_twitter_cards(soup),
                "canonical": self._get_canonical(soup),
                "robots": self._get_robots_meta(soup),
                "structured_data": self._check_structured_data(soup),
            }

            return self._format_meta_analysis(url, meta_analysis)

        except Exception as e:
            return f"Error analyzing meta tags: {str(e)}"

    def _analyze_og_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Open Graph tags."""
        og_tags = {}
        for tag in soup.find_all('meta', property=re.compile(r'^og:')):
            og_tags[tag.get('property')] = tag.get('content', '')
        return og_tags

    def _analyze_twitter_cards(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract Twitter Card tags."""
        twitter_tags = {}
        for tag in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            twitter_tags[tag.get('name')] = tag.get('content', '')
        return twitter_tags

    def _get_canonical(self, soup: BeautifulSoup) -> Optional[str]:
        """Get canonical URL."""
        canonical = soup.find('link', rel='canonical')
        return canonical.get('href') if canonical else None

    def _get_robots_meta(self, soup: BeautifulSoup) -> Optional[str]:
        """Get robots meta directive."""
        robots = soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else None

    def _check_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Check for structured data."""
        json_ld = soup.find_all('script', type='application/ld+json')
        return {
            "json_ld_count": len(json_ld),
            "has_structured_data": len(json_ld) > 0,
        }

    def _format_meta_analysis(
        self,
        url: str,
        analysis: Dict[str, Any]
    ) -> str:
        """Format meta analysis results."""
        output = []
        output.append("=" * 50)
        output.append("META TAG ANALYSIS")
        output.append("=" * 50)
        output.append(f"\nURL: {url}")

        output.append("\n--- Open Graph Tags ---")
        og = analysis.get("open_graph", {})
        if og:
            for key, value in og.items():
                output.append(f"  {key}: {value[:80]}...")
        else:
            output.append("  No Open Graph tags found (RECOMMENDED)")

        output.append("\n--- Twitter Cards ---")
        twitter = analysis.get("twitter_cards", {})
        if twitter:
            for key, value in twitter.items():
                output.append(f"  {key}: {value[:80]}...")
        else:
            output.append("  No Twitter Card tags found")

        output.append(f"\nCanonical URL: {analysis.get('canonical', 'Not set')}")
        output.append(f"Robots: {analysis.get('robots', 'Not specified')}")

        sd = analysis.get("structured_data", {})
        output.append(
            f"\nStructured Data: "
            f"{'Yes' if sd.get('has_structured_data') else 'No'} "
            f"({sd.get('json_ld_count', 0)} JSON-LD blocks)"
        )

        return "\n".join(output)


class ContentStructureAnalyzerTool(BaseTool):
    """Tool for analyzing content structure for AI readability."""

    name: str = "content_structure_analyzer"
    description: str = """
    Analyzes content structure for AI search optimization:
    - Heading hierarchy and organization
    - Paragraph structure and length
    - List usage (bullet points, numbered)
    - Content sections and flow
    - FAQ and Q&A structure detection

    Input: URL or content text.
    Output: Structure analysis with AI-readability recommendations.
    """

    def _run(self, content: str) -> str:
        """Analyze content structure."""
        # Check if input is URL
        if content.startswith('http'):
            try:
                response = requests.get(content, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                text_content = soup.get_text()
            except Exception as e:
                return f"Error fetching URL: {str(e)}"
        else:
            text_content = content

        analysis = self._analyze_structure(text_content)
        return self._format_structure_analysis(analysis)

    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze content structure."""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Detect lists
        bullet_points = len(re.findall(r'^\s*[-•*]\s', content, re.MULTILINE))
        numbered_items = len(re.findall(r'^\s*\d+[.)]\s', content, re.MULTILINE))

        # Detect Q&A patterns
        questions = re.findall(r'[^.!?]*\?', content)

        return {
            "paragraph_count": len(paragraphs),
            "avg_paragraph_length": sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0,
            "sentence_count": len(sentences),
            "bullet_points": bullet_points,
            "numbered_items": numbered_items,
            "questions_found": len(questions),
            "has_faq_structure": len(questions) >= 3,
            "total_words": len(content.split()),
        }

    def _format_structure_analysis(self, analysis: Dict[str, Any]) -> str:
        """Format structure analysis."""
        output = []
        output.append("=" * 50)
        output.append("CONTENT STRUCTURE ANALYSIS")
        output.append("=" * 50)

        output.append(f"\nTotal Words: {analysis['total_words']}")
        output.append(f"Paragraphs: {analysis['paragraph_count']}")
        output.append(
            f"Avg Paragraph Length: {analysis['avg_paragraph_length']:.1f} words"
        )
        output.append(f"Sentences: {analysis['sentence_count']}")

        output.append(f"\n--- List Usage ---")
        output.append(f"Bullet Points: {analysis['bullet_points']}")
        output.append(f"Numbered Items: {analysis['numbered_items']}")

        output.append(f"\n--- Q&A Detection ---")
        output.append(f"Questions Found: {analysis['questions_found']}")
        output.append(
            f"FAQ Structure: "
            f"{'Detected' if analysis['has_faq_structure'] else 'Not detected'}"
        )

        # Recommendations
        output.append(f"\n--- AI Optimization Recommendations ---")
        if analysis['avg_paragraph_length'] > 100:
            output.append("• Consider shorter paragraphs for better AI parsing")
        if analysis['bullet_points'] + analysis['numbered_items'] < 3:
            output.append("• Add more lists for structured information")
        if not analysis['has_faq_structure']:
            output.append("• Consider adding FAQ section for AI assistants")

        return "\n".join(output)
