"""
Keyword Research and Analysis Tools for AI Search Optimization.
"""

import re
from typing import Optional, Dict, Any, List, ClassVar
from collections import Counter
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class KeywordInput(BaseModel):
    """Input schema for keyword research."""
    topic: str = Field(..., description="Topic or seed keyword for research")
    content: Optional[str] = Field(None, description="Content to analyze")
    competitors: Optional[List[str]] = Field(
        None,
        description="Competitor keywords or URLs"
    )


class KeywordResearchTool(BaseTool):
    """
    AI-powered keyword research tool for search optimization.
    Generates keyword suggestions optimized for AI search platforms.
    """

    name: str = "keyword_researcher"
    description: str = """
    Performs keyword research for AI search optimization:
    - Generates semantic keyword variations
    - Identifies long-tail keyword opportunities
    - Suggests question-based keywords (ideal for AI)
    - Provides keyword clusters and topic mapping
    - Analyzes search intent categories

    Input: Topic or seed keyword.
    Output: Comprehensive keyword research report with AI-optimized suggestions.
    """
    args_schema: type = KeywordInput

    # Common question words for AI-optimized keywords
    QUESTION_PREFIXES: ClassVar[List[str]] = [
        "what is", "what are", "how to", "how does", "why is",
        "why do", "when to", "when should", "where to", "where can",
        "which", "who", "can you", "should I", "is it"
    ]

    # Intent modifiers
    INTENT_MODIFIERS: ClassVar[Dict[str, List[str]]] = {
        "informational": ["guide", "tutorial", "explained", "definition", "meaning", "examples"],
        "commercial": ["best", "top", "review", "comparison", "vs", "alternative"],
        "transactional": ["buy", "price", "cost", "discount", "deal", "cheap"],
        "navigational": ["login", "website", "official", "app", "download"]
    }

    def _run(
        self,
        topic: str,
        content: Optional[str] = None,
        competitors: Optional[List[str]] = None
    ) -> str:
        """Execute keyword research."""
        research = {
            "seed_keyword": topic,
            "variations": self._generate_variations(topic),
            "long_tail": self._generate_long_tail(topic),
            "questions": self._generate_questions(topic),
            "intent_keywords": self._generate_intent_keywords(topic),
            "semantic_clusters": self._generate_clusters(topic),
            "ai_optimized": self._generate_ai_optimized(topic),
        }

        if content:
            research["content_analysis"] = self._analyze_content_keywords(
                content, topic
            )

        return self._format_research(research)

    def _generate_variations(self, topic: str) -> List[str]:
        """Generate keyword variations."""
        variations = [topic]

        # Plural/singular
        if topic.endswith('s'):
            variations.append(topic[:-1])
        else:
            variations.append(topic + 's')

        # Word order variations
        words = topic.split()
        if len(words) >= 2:
            variations.append(' '.join(reversed(words)))

        # Common suffixes
        suffixes = ['ing', 'tion', 'ment', 'ness']
        for suffix in suffixes:
            variations.append(f"{topic} {suffix}")

        return list(set(variations))[:10]

    def _generate_long_tail(self, topic: str) -> List[str]:
        """Generate long-tail keyword variations."""
        long_tail = []

        # Add modifiers
        modifiers_before = [
            "best", "top", "free", "cheap", "professional",
            "online", "easy", "quick", "complete", "ultimate"
        ]

        modifiers_after = [
            "guide", "tutorial", "tips", "strategies", "examples",
            "tools", "software", "services", "for beginners", "in 2024"
        ]

        for mod in modifiers_before[:5]:
            long_tail.append(f"{mod} {topic}")

        for mod in modifiers_after[:5]:
            long_tail.append(f"{topic} {mod}")

        # Combinations
        long_tail.append(f"how to use {topic}")
        long_tail.append(f"{topic} for small business")
        long_tail.append(f"{topic} best practices")

        return long_tail

    def _generate_questions(self, topic: str) -> List[str]:
        """Generate question-based keywords (ideal for AI search)."""
        questions = []

        for prefix in self.QUESTION_PREFIXES:
            questions.append(f"{prefix} {topic}")

        # Add specific question patterns
        questions.extend([
            f"what is {topic} and how does it work",
            f"how to get started with {topic}",
            f"what are the benefits of {topic}",
            f"how much does {topic} cost",
            f"{topic} vs alternatives",
        ])

        return questions[:15]

    def _generate_intent_keywords(self, topic: str) -> Dict[str, List[str]]:
        """Generate keywords by search intent."""
        intent_keywords = {}

        for intent, modifiers in self.INTENT_MODIFIERS.items():
            keywords = []
            for mod in modifiers:
                keywords.append(f"{mod} {topic}")
                keywords.append(f"{topic} {mod}")
            intent_keywords[intent] = keywords[:5]

        return intent_keywords

    def _generate_clusters(self, topic: str) -> List[Dict[str, Any]]:
        """Generate semantic keyword clusters."""
        clusters = [
            {
                "cluster_name": f"{topic.title()} Fundamentals",
                "keywords": [
                    f"what is {topic}",
                    f"{topic} definition",
                    f"{topic} basics",
                    f"{topic} introduction",
                    f"{topic} 101"
                ]
            },
            {
                "cluster_name": f"{topic.title()} How-To",
                "keywords": [
                    f"how to {topic}",
                    f"{topic} tutorial",
                    f"{topic} step by step",
                    f"{topic} guide",
                    f"learn {topic}"
                ]
            },
            {
                "cluster_name": f"{topic.title()} Tools & Resources",
                "keywords": [
                    f"{topic} tools",
                    f"{topic} software",
                    f"{topic} platforms",
                    f"best {topic} tools",
                    f"free {topic} resources"
                ]
            },
            {
                "cluster_name": f"{topic.title()} Strategy",
                "keywords": [
                    f"{topic} strategy",
                    f"{topic} tips",
                    f"{topic} best practices",
                    f"{topic} techniques",
                    f"improve {topic}"
                ]
            }
        ]

        return clusters

    def _generate_ai_optimized(self, topic: str) -> List[Dict[str, str]]:
        """Generate AI search optimized keywords with context."""
        return [
            {
                "keyword": f"explain {topic} simply",
                "context": "Conversational query for AI assistants",
                "ai_platform": "ChatGPT, Claude, Perplexity"
            },
            {
                "keyword": f"summarize {topic}",
                "context": "Summary request query",
                "ai_platform": "All AI platforms"
            },
            {
                "keyword": f"compare {topic} options",
                "context": "Comparison query for AI analysis",
                "ai_platform": "ChatGPT, Perplexity"
            },
            {
                "keyword": f"{topic} pros and cons",
                "context": "Balanced analysis query",
                "ai_platform": "All AI platforms"
            },
            {
                "keyword": f"recommend {topic} for beginners",
                "context": "Recommendation query",
                "ai_platform": "ChatGPT, Claude"
            },
            {
                "keyword": f"what should I know about {topic}",
                "context": "Educational overview query",
                "ai_platform": "All AI platforms"
            }
        ]

    def _analyze_content_keywords(
        self,
        content: str,
        topic: str
    ) -> Dict[str, Any]:
        """Analyze keywords in existing content."""
        words = re.findall(r'\b\w+\b', content.lower())
        word_freq = Counter(words)

        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may',
            'might', 'must', 'shall', 'can', 'need', 'dare',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
            'from', 'as', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'under', 'again',
            'further', 'then', 'once', 'and', 'but', 'or', 'nor',
            'so', 'yet', 'both', 'either', 'neither', 'not', 'only'
        }

        filtered_freq = {
            k: v for k, v in word_freq.items()
            if k not in stop_words and len(k) > 2
        }

        top_keywords = sorted(
            filtered_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )[:20]

        topic_presence = topic.lower() in content.lower()
        topic_count = content.lower().count(topic.lower())

        return {
            "top_keywords": top_keywords,
            "topic_present": topic_presence,
            "topic_frequency": topic_count,
            "total_words": len(words),
            "unique_words": len(set(words))
        }

    def _format_research(self, research: Dict[str, Any]) -> str:
        """Format keyword research results."""
        output = []
        output.append("=" * 60)
        output.append("KEYWORD RESEARCH REPORT")
        output.append("=" * 60)
        output.append(f"\nSeed Keyword: {research['seed_keyword']}")

        output.append("\n--- Keyword Variations ---")
        for kw in research['variations']:
            output.append(f"  • {kw}")

        output.append("\n--- Long-Tail Keywords ---")
        for kw in research['long_tail'][:10]:
            output.append(f"  • {kw}")

        output.append("\n--- Question Keywords (AI Optimized) ---")
        for kw in research['questions'][:10]:
            output.append(f"  • {kw}")

        output.append("\n--- Intent-Based Keywords ---")
        for intent, keywords in research['intent_keywords'].items():
            output.append(f"\n  [{intent.upper()}]")
            for kw in keywords[:3]:
                output.append(f"    • {kw}")

        output.append("\n--- Semantic Clusters ---")
        for cluster in research['semantic_clusters']:
            output.append(f"\n  {cluster['cluster_name']}:")
            for kw in cluster['keywords'][:3]:
                output.append(f"    • {kw}")

        output.append("\n--- AI Search Optimized Keywords ---")
        for item in research['ai_optimized']:
            output.append(f"\n  Keyword: {item['keyword']}")
            output.append(f"  Context: {item['context']}")
            output.append(f"  Platforms: {item['ai_platform']}")

        if 'content_analysis' in research:
            ca = research['content_analysis']
            output.append("\n--- Content Keyword Analysis ---")
            output.append(f"  Topic Present: {'Yes' if ca['topic_present'] else 'No'}")
            output.append(f"  Topic Frequency: {ca['topic_frequency']}")
            output.append(f"  Top Keywords in Content:")
            for kw, count in ca['top_keywords'][:10]:
                output.append(f"    • {kw}: {count}")

        return "\n".join(output)


class KeywordDensityTool(BaseTool):
    """Tool for analyzing keyword density in content."""

    name: str = "keyword_density"
    description: str = """
    Analyzes keyword density and distribution in content:
    - Calculates exact match density
    - Analyzes keyword placement (title, headers, body)
    - Checks for keyword stuffing
    - Provides optimal density recommendations

    Input: Content text and target keywords.
    Output: Density analysis with optimization recommendations.
    """

    def _run(self, content: str, keywords: str) -> str:
        """Analyze keyword density."""
        keyword_list = [k.strip() for k in keywords.split(',')]

        analysis = {
            "content_stats": self._content_stats(content),
            "keyword_analysis": {}
        }

        for keyword in keyword_list:
            analysis["keyword_analysis"][keyword] = self._analyze_keyword(
                content, keyword
            )

        return self._format_density_report(analysis)

    def _content_stats(self, content: str) -> Dict[str, int]:
        """Get basic content statistics."""
        words = content.split()
        return {
            "word_count": len(words),
            "character_count": len(content),
            "sentence_count": len(re.split(r'[.!?]+', content))
        }

    def _analyze_keyword(self, content: str, keyword: str) -> Dict[str, Any]:
        """Analyze a specific keyword in content."""
        content_lower = content.lower()
        keyword_lower = keyword.lower()
        words = content.split()
        word_count = len(words)

        # Exact match count
        exact_count = content_lower.count(keyword_lower)

        # Density calculation
        keyword_words = len(keyword.split())
        density = (exact_count * keyword_words / word_count * 100) if word_count > 0 else 0

        # Position analysis
        first_100_words = ' '.join(words[:100]).lower()
        last_100_words = ' '.join(words[-100:]).lower() if len(words) > 100 else first_100_words

        # Determine if density is optimal
        optimal_range = (1.0, 2.5)
        is_optimal = optimal_range[0] <= density <= optimal_range[1]
        is_stuffed = density > 3.0

        return {
            "count": exact_count,
            "density": round(density, 2),
            "in_first_100_words": keyword_lower in first_100_words,
            "in_last_100_words": keyword_lower in last_100_words,
            "is_optimal": is_optimal,
            "is_stuffed": is_stuffed,
            "recommendation": self._get_recommendation(density)
        }

    def _get_recommendation(self, density: float) -> str:
        """Get density recommendation."""
        if density < 0.5:
            return "Increase keyword usage - currently underutilized"
        elif density < 1.0:
            return "Slightly increase keyword presence"
        elif density <= 2.5:
            return "Optimal density - maintain current level"
        elif density <= 3.0:
            return "Slightly high - consider reducing"
        else:
            return "WARNING: Potential keyword stuffing - reduce usage"

    def _format_density_report(self, analysis: Dict[str, Any]) -> str:
        """Format density analysis report."""
        output = []
        output.append("=" * 50)
        output.append("KEYWORD DENSITY ANALYSIS")
        output.append("=" * 50)

        stats = analysis["content_stats"]
        output.append(f"\nContent Statistics:")
        output.append(f"  Word Count: {stats['word_count']}")
        output.append(f"  Sentences: {stats['sentence_count']}")

        output.append("\n--- Keyword Analysis ---")
        for keyword, data in analysis["keyword_analysis"].items():
            output.append(f"\nKeyword: '{keyword}'")
            output.append(f"  Occurrences: {data['count']}")
            output.append(f"  Density: {data['density']}%")
            output.append(f"  In First 100 Words: {'Yes' if data['in_first_100_words'] else 'No'}")
            output.append(f"  Status: {'✓ Optimal' if data['is_optimal'] else '⚠ Needs adjustment'}")
            if data['is_stuffed']:
                output.append(f"  ⚠ WARNING: Possible keyword stuffing detected!")
            output.append(f"  Recommendation: {data['recommendation']}")

        return "\n".join(output)


class SemanticKeywordTool(BaseTool):
    """Tool for generating semantically related keywords."""

    name: str = "semantic_keywords"
    description: str = """
    Generates semantically related keywords for AI search:
    - LSI (Latent Semantic Indexing) keywords
    - Related terms and synonyms
    - Co-occurring keywords
    - Entity associations

    Input: Primary keyword or topic.
    Output: Semantic keyword map for comprehensive coverage.
    """

    # Semantic categories for expansion
    SEMANTIC_PATTERNS: ClassVar[Dict[str, List[str]]] = {
        "synonyms": ["similar to", "same as", "like", "equivalent"],
        "related_concepts": ["related to", "associated with", "connected to"],
        "subtopics": ["types of", "categories of", "kinds of"],
        "use_cases": ["used for", "application of", "purpose of"],
        "benefits": ["advantages of", "benefits of", "pros of"],
        "challenges": ["challenges of", "problems with", "cons of"]
    }

    def _run(self, keyword: str) -> str:
        """Generate semantic keywords."""
        semantic_map = {
            "primary_keyword": keyword,
            "semantic_variations": self._generate_semantic_variations(keyword),
            "contextual_keywords": self._generate_contextual(keyword),
            "entity_keywords": self._generate_entities(keyword),
            "action_keywords": self._generate_action_keywords(keyword),
        }

        return self._format_semantic_map(semantic_map)

    def _generate_semantic_variations(self, keyword: str) -> List[Dict[str, Any]]:
        """Generate semantic variations."""
        variations = []

        for category, patterns in self.SEMANTIC_PATTERNS.items():
            category_keywords = []
            for pattern in patterns:
                category_keywords.append(f"{pattern} {keyword}")
            variations.append({
                "category": category,
                "keywords": category_keywords
            })

        return variations

    def _generate_contextual(self, keyword: str) -> List[str]:
        """Generate contextual keywords."""
        contexts = [
            f"{keyword} in business",
            f"{keyword} for marketing",
            f"{keyword} strategy",
            f"{keyword} implementation",
            f"{keyword} optimization",
            f"enterprise {keyword}",
            f"{keyword} platform",
            f"{keyword} solution",
            f"automated {keyword}",
            f"AI-powered {keyword}"
        ]
        return contexts

    def _generate_entities(self, keyword: str) -> List[Dict[str, str]]:
        """Generate entity-based keywords."""
        return [
            {"entity_type": "Tool", "keyword": f"{keyword} tools"},
            {"entity_type": "Platform", "keyword": f"{keyword} platform"},
            {"entity_type": "Service", "keyword": f"{keyword} service"},
            {"entity_type": "Software", "keyword": f"{keyword} software"},
            {"entity_type": "Company", "keyword": f"{keyword} providers"},
            {"entity_type": "Expert", "keyword": f"{keyword} specialist"},
        ]

    def _generate_action_keywords(self, keyword: str) -> List[str]:
        """Generate action-oriented keywords."""
        actions = [
            f"implement {keyword}",
            f"improve {keyword}",
            f"optimize {keyword}",
            f"measure {keyword}",
            f"automate {keyword}",
            f"scale {keyword}",
            f"learn {keyword}",
            f"master {keyword}",
        ]
        return actions

    def _format_semantic_map(self, semantic_map: Dict[str, Any]) -> str:
        """Format semantic keyword map."""
        output = []
        output.append("=" * 60)
        output.append("SEMANTIC KEYWORD MAP")
        output.append("=" * 60)
        output.append(f"\nPrimary Keyword: {semantic_map['primary_keyword']}")

        output.append("\n--- Semantic Variations ---")
        for variation in semantic_map['semantic_variations']:
            output.append(f"\n  [{variation['category'].upper()}]")
            for kw in variation['keywords'][:3]:
                output.append(f"    • {kw}")

        output.append("\n--- Contextual Keywords ---")
        for kw in semantic_map['contextual_keywords']:
            output.append(f"  • {kw}")

        output.append("\n--- Entity Keywords ---")
        for entity in semantic_map['entity_keywords']:
            output.append(f"  • {entity['keyword']} ({entity['entity_type']})")

        output.append("\n--- Action Keywords ---")
        for kw in semantic_map['action_keywords']:
            output.append(f"  • {kw}")

        return "\n".join(output)
