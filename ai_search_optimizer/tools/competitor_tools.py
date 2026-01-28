"""
Competitor Analysis Tools for AI Search Optimization.
"""

import re
from typing import Optional, Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup


class CompetitorInput(BaseModel):
    """Input schema for competitor analysis."""
    competitor_urls: List[str] = Field(
        ...,
        description="List of competitor URLs to analyze"
    )
    target_keywords: Optional[List[str]] = Field(
        None,
        description="Target keywords for comparison"
    )


class CompetitorAnalysisTool(BaseTool):
    """
    Tool for analyzing competitor content strategies.
    """

    name: str = "competitor_analyzer"
    description: str = """
    Analyzes competitor content for AI search optimization insights:
    - Content structure and format analysis
    - Keyword usage comparison
    - AI optimization tactics identification
    - Content gap analysis
    - Competitive positioning insights

    Input: List of competitor URLs and optional target keywords.
    Output: Comprehensive competitor analysis with strategic recommendations.
    """
    args_schema: type = CompetitorInput

    def _run(
        self,
        competitor_urls: List[str],
        target_keywords: Optional[List[str]] = None
    ) -> str:
        """Execute competitor analysis."""
        analyses = []

        for url in competitor_urls[:5]:  # Limit to 5 URLs
            try:
                analysis = self._analyze_competitor(url, target_keywords)
                analyses.append(analysis)
            except Exception as e:
                analyses.append({
                    "url": url,
                    "error": str(e)
                })

        summary = self._generate_summary(analyses)
        return self._format_competitor_report(analyses, summary)

    def _analyze_competitor(
        self,
        url: str,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze a single competitor."""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; CompetitorBot/1.0)'
            })
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()

            analysis = {
                "url": url,
                "title": self._extract_title(soup),
                "meta_description": self._extract_meta(soup),
                "content_stats": self._analyze_content_stats(text_content),
                "structure": self._analyze_structure(soup),
                "ai_optimization": self._detect_ai_optimization(soup, text_content),
                "schema_markup": self._check_schema(soup),
            }

            if keywords:
                analysis["keyword_usage"] = self._analyze_keyword_usage(
                    text_content, keywords
                )

            return analysis

        except requests.RequestException as e:
            return {"url": url, "error": f"Failed to fetch: {str(e)}"}

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title = soup.find('title')
        return title.get_text().strip() if title else ""

    def _extract_meta(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else ""

    def _analyze_content_stats(self, content: str) -> Dict[str, Any]:
        """Analyze content statistics."""
        words = content.split()
        sentences = [s for s in re.split(r'[.!?]+', content) if s.strip()]

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
        }

    def _analyze_structure(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze content structure."""
        headers = {f'h{i}': len(soup.find_all(f'h{i}')) for i in range(1, 7)}
        lists = {
            "unordered": len(soup.find_all('ul')),
            "ordered": len(soup.find_all('ol')),
        }

        # Check for FAQ structure
        faq_patterns = soup.find_all(['details', 'summary']) + \
                      soup.find_all(class_=re.compile(r'faq|accordion', re.I))

        return {
            "headers": headers,
            "lists": lists,
            "images": len(soup.find_all('img')),
            "videos": len(soup.find_all(['video', 'iframe'])),
            "has_faq": len(faq_patterns) > 0,
            "tables": len(soup.find_all('table')),
        }

    def _detect_ai_optimization(
        self,
        soup: BeautifulSoup,
        content: str
    ) -> Dict[str, bool]:
        """Detect AI optimization tactics."""
        return {
            "clear_definitions": bool(re.search(
                r'(is defined as|refers to|is a type of|means)',
                content, re.I
            )),
            "question_headers": bool(soup.find_all(
                ['h1', 'h2', 'h3', 'h4'],
                string=re.compile(r'\?$')
            )),
            "step_by_step": bool(re.search(
                r'step \d|step-by-step|how to',
                content, re.I
            )),
            "lists_for_features": bool(soup.find_all('ul')),
            "comparison_tables": bool(soup.find_all('table')),
            "faq_section": bool(re.search(
                r'frequently asked|faq|common questions',
                content, re.I
            )),
            "structured_data": bool(soup.find_all(
                'script',
                type='application/ld+json'
            )),
        }

    def _check_schema(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Check for schema markup."""
        json_ld = soup.find_all('script', type='application/ld+json')
        schemas_found = []

        for script in json_ld:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict):
                    schema_type = data.get('@type', 'Unknown')
                    schemas_found.append(schema_type)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            schemas_found.append(item.get('@type', 'Unknown'))
            except:
                pass

        return {
            "count": len(json_ld),
            "types": schemas_found,
        }

    def _analyze_keyword_usage(
        self,
        content: str,
        keywords: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze keyword usage in content."""
        content_lower = content.lower()
        word_count = len(content.split())

        results = {}
        for keyword in keywords:
            count = content_lower.count(keyword.lower())
            density = (count / word_count * 100) if word_count > 0 else 0

            results[keyword] = {
                "count": count,
                "density": round(density, 2),
                "in_title": keyword.lower() in content_lower[:200],
            }

        return results

    def _generate_summary(
        self,
        analyses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summary insights from all analyses."""
        valid_analyses = [a for a in analyses if 'error' not in a]

        if not valid_analyses:
            return {"error": "No valid analyses to summarize"}

        # Aggregate statistics
        avg_word_count = sum(
            a['content_stats']['word_count']
            for a in valid_analyses
        ) / len(valid_analyses)

        # Common tactics
        tactics_count = {
            "clear_definitions": 0,
            "question_headers": 0,
            "step_by_step": 0,
            "faq_section": 0,
            "structured_data": 0,
        }

        for analysis in valid_analyses:
            ai_opt = analysis.get('ai_optimization', {})
            for tactic in tactics_count:
                if ai_opt.get(tactic):
                    tactics_count[tactic] += 1

        # Find content gaps
        common_tactics = [
            t for t, c in tactics_count.items()
            if c >= len(valid_analyses) / 2
        ]

        return {
            "competitor_count": len(valid_analyses),
            "avg_word_count": round(avg_word_count),
            "common_tactics": common_tactics,
            "tactics_breakdown": tactics_count,
        }

    def _format_competitor_report(
        self,
        analyses: List[Dict[str, Any]],
        summary: Dict[str, Any]
    ) -> str:
        """Format competitor analysis report."""
        output = []
        output.append("=" * 60)
        output.append("COMPETITOR ANALYSIS REPORT")
        output.append("=" * 60)

        # Summary section
        output.append("\n--- SUMMARY ---")
        output.append(f"Competitors Analyzed: {summary.get('competitor_count', 0)}")
        output.append(f"Average Word Count: {summary.get('avg_word_count', 0)}")

        output.append("\nCommon AI Optimization Tactics:")
        for tactic in summary.get('common_tactics', []):
            output.append(f"  ✓ {tactic.replace('_', ' ').title()}")

        output.append("\nTactics Breakdown:")
        for tactic, count in summary.get('tactics_breakdown', {}).items():
            output.append(f"  {tactic.replace('_', ' ').title()}: {count}/{summary.get('competitor_count', 0)}")

        # Individual analyses
        output.append("\n" + "=" * 60)
        output.append("INDIVIDUAL COMPETITOR ANALYSIS")
        output.append("=" * 60)

        for i, analysis in enumerate(analyses, 1):
            output.append(f"\n--- Competitor {i} ---")
            output.append(f"URL: {analysis.get('url', 'N/A')}")

            if 'error' in analysis:
                output.append(f"Error: {analysis['error']}")
                continue

            output.append(f"Title: {analysis.get('title', 'N/A')[:60]}...")

            stats = analysis.get('content_stats', {})
            output.append(f"\nContent Stats:")
            output.append(f"  Word Count: {stats.get('word_count', 0)}")
            output.append(f"  Sentences: {stats.get('sentence_count', 0)}")

            structure = analysis.get('structure', {})
            output.append(f"\nStructure:")
            headers = structure.get('headers', {})
            for h, count in headers.items():
                if count > 0:
                    output.append(f"  {h.upper()}: {count}")
            output.append(f"  Images: {structure.get('images', 0)}")
            output.append(f"  Has FAQ: {'Yes' if structure.get('has_faq') else 'No'}")

            ai_opt = analysis.get('ai_optimization', {})
            output.append(f"\nAI Optimization Tactics:")
            for tactic, present in ai_opt.items():
                status = "✓" if present else "✗"
                output.append(f"  {status} {tactic.replace('_', ' ').title()}")

            schema = analysis.get('schema_markup', {})
            if schema.get('types'):
                output.append(f"\nSchema Types: {', '.join(schema['types'])}")

            if 'keyword_usage' in analysis:
                output.append(f"\nKeyword Usage:")
                for kw, data in analysis['keyword_usage'].items():
                    output.append(
                        f"  '{kw}': {data['count']} times "
                        f"({data['density']}% density)"
                    )

        return "\n".join(output)


class MarketPositioningTool(BaseTool):
    """Tool for analyzing market positioning and differentiation."""

    name: str = "market_positioning"
    description: str = """
    Analyzes market positioning for AI search differentiation:
    - Unique value proposition analysis
    - Content differentiation opportunities
    - Market gap identification
    - Positioning recommendations

    Input: Your content/URL and competitor content/URLs.
    Output: Market positioning analysis with differentiation strategies.
    """

    def _run(self, your_content: str, competitor_content: str = "") -> str:
        """Analyze market positioning."""
        your_analysis = self._analyze_positioning(your_content)
        competitor_analysis = self._analyze_positioning(competitor_content) if competitor_content else None

        gaps = self._identify_gaps(your_analysis, competitor_analysis)
        opportunities = self._identify_opportunities(your_analysis, gaps)

        return self._format_positioning_report(
            your_analysis,
            competitor_analysis,
            gaps,
            opportunities
        )

    def _analyze_positioning(self, content: str) -> Dict[str, Any]:
        """Analyze content positioning."""
        return {
            "word_count": len(content.split()),
            "unique_angles": self._detect_angles(content),
            "expertise_signals": self._detect_expertise(content),
            "differentiation": self._detect_differentiation(content),
            "content_depth": self._assess_depth(content),
        }

    def _detect_angles(self, content: str) -> List[str]:
        """Detect unique content angles."""
        angles = []

        angle_patterns = {
            "data_driven": r'data shows|statistics|research|study found|survey',
            "expert_opinion": r'expert|professional|specialist|industry leader',
            "case_study": r'case study|real-world|example|success story',
            "tutorial": r'how to|step-by-step|guide|tutorial|learn',
            "comparison": r'vs|versus|compared to|comparison|alternative',
            "trend_analysis": r'trend|future|prediction|forecast|emerging',
        }

        for angle, pattern in angle_patterns.items():
            if re.search(pattern, content, re.I):
                angles.append(angle)

        return angles

    def _detect_expertise(self, content: str) -> List[str]:
        """Detect expertise signals."""
        signals = []

        expertise_patterns = {
            "citations": r'according to|cited|reference|source',
            "credentials": r'years of experience|certified|qualified|degree',
            "original_research": r'our research|we found|our analysis|our study',
            "industry_knowledge": r'industry|market|sector|field',
            "practical_experience": r'in practice|real-world|hands-on',
        }

        for signal, pattern in expertise_patterns.items():
            if re.search(pattern, content, re.I):
                signals.append(signal)

        return signals

    def _detect_differentiation(self, content: str) -> Dict[str, bool]:
        """Detect differentiation factors."""
        return {
            "unique_methodology": bool(re.search(
                r'our (unique|proprietary|exclusive)',
                content, re.I
            )),
            "specific_niche": bool(re.search(
                r'specifically for|designed for|tailored to',
                content, re.I
            )),
            "actionable_advice": bool(re.search(
                r'actionable|practical|immediately|right now',
                content, re.I
            )),
            "comprehensive_coverage": len(content.split()) > 1500,
        }

    def _assess_depth(self, content: str) -> str:
        """Assess content depth."""
        word_count = len(content.split())
        if word_count > 2500:
            return "Comprehensive"
        elif word_count > 1500:
            return "Detailed"
        elif word_count > 800:
            return "Moderate"
        else:
            return "Brief"

    def _identify_gaps(
        self,
        your_analysis: Dict[str, Any],
        competitor_analysis: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Identify content gaps."""
        gaps = []

        if not competitor_analysis:
            # General gaps based on best practices
            if "data_driven" not in your_analysis['unique_angles']:
                gaps.append("Add data-driven insights and statistics")
            if "case_study" not in your_analysis['unique_angles']:
                gaps.append("Include case studies or real-world examples")
            if your_analysis['content_depth'] in ['Brief', 'Moderate']:
                gaps.append("Expand content depth for comprehensive coverage")
        else:
            # Comparative gaps
            missing_angles = set(competitor_analysis['unique_angles']) - set(your_analysis['unique_angles'])
            for angle in missing_angles:
                gaps.append(f"Add {angle.replace('_', ' ')} content angle")

            missing_signals = set(competitor_analysis['expertise_signals']) - set(your_analysis['expertise_signals'])
            for signal in missing_signals:
                gaps.append(f"Include {signal.replace('_', ' ')} signals")

        return gaps

    def _identify_opportunities(
        self,
        analysis: Dict[str, Any],
        gaps: List[str]
    ) -> List[str]:
        """Identify differentiation opportunities."""
        opportunities = []

        # Based on what's NOT being done
        differentiation = analysis['differentiation']
        if not differentiation['unique_methodology']:
            opportunities.append("Develop and highlight a unique methodology or framework")
        if not differentiation['specific_niche']:
            opportunities.append("Target a specific niche or audience segment")
        if not differentiation['actionable_advice']:
            opportunities.append("Add more actionable, practical recommendations")

        # AI-specific opportunities
        opportunities.extend([
            "Create FAQ section for AI assistant queries",
            "Add comparison tables for easy AI parsing",
            "Include clear definitions that AI can cite",
            "Structure content with question-based headers",
        ])

        return opportunities[:8]

    def _format_positioning_report(
        self,
        your_analysis: Dict[str, Any],
        competitor_analysis: Optional[Dict[str, Any]],
        gaps: List[str],
        opportunities: List[str]
    ) -> str:
        """Format positioning report."""
        output = []
        output.append("=" * 60)
        output.append("MARKET POSITIONING ANALYSIS")
        output.append("=" * 60)

        output.append("\n--- Your Content Analysis ---")
        output.append(f"Content Depth: {your_analysis['content_depth']}")
        output.append(f"Word Count: {your_analysis['word_count']}")

        output.append("\nContent Angles Present:")
        for angle in your_analysis['unique_angles']:
            output.append(f"  ✓ {angle.replace('_', ' ').title()}")
        if not your_analysis['unique_angles']:
            output.append("  None detected")

        output.append("\nExpertise Signals:")
        for signal in your_analysis['expertise_signals']:
            output.append(f"  ✓ {signal.replace('_', ' ').title()}")
        if not your_analysis['expertise_signals']:
            output.append("  None detected")

        output.append("\nDifferentiation Factors:")
        for factor, present in your_analysis['differentiation'].items():
            status = "✓" if present else "✗"
            output.append(f"  {status} {factor.replace('_', ' ').title()}")

        if competitor_analysis:
            output.append("\n--- Competitor Comparison ---")
            output.append(f"Competitor Content Depth: {competitor_analysis['content_depth']}")
            output.append(f"Competitor Angles: {', '.join(competitor_analysis['unique_angles'])}")

        output.append("\n--- Content Gaps to Address ---")
        for i, gap in enumerate(gaps, 1):
            output.append(f"  {i}. {gap}")

        output.append("\n--- Differentiation Opportunities ---")
        for i, opp in enumerate(opportunities, 1):
            output.append(f"  {i}. {opp}")

        return "\n".join(output)
