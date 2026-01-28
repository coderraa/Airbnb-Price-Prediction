"""
Content Optimization Tools for AI Search Optimization.
"""

import re
from typing import Optional, Dict, Any, List, ClassVar
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class ContentInput(BaseModel):
    """Input schema for content analysis."""
    content: str = Field(..., description="Content to analyze or optimize")
    target_keywords: Optional[List[str]] = Field(
        None,
        description="Target keywords for optimization"
    )
    platform: Optional[str] = Field(
        default="all",
        description="Target AI platform (chatgpt, perplexity, claude, google, all)"
    )


class ContentOptimizerTool(BaseTool):
    """
    AI-powered content optimization tool for search visibility.
    """

    name: str = "content_optimizer"
    description: str = """
    Optimizes content for AI search platforms:
    - Restructures content for AI readability
    - Adds semantic markers and context
    - Optimizes for featured snippets and AI citations
    - Suggests improvements for AI comprehension
    - Formats for structured data extraction

    Input: Content text with optional target keywords and platform.
    Output: Optimization recommendations and rewritten sections.
    """
    args_schema: type = ContentInput

    # AI platform optimization patterns
    PLATFORM_PATTERNS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "chatgpt": {
            "prefer_format": "conversational with clear structure",
            "optimal_length": "comprehensive but scannable",
            "key_elements": ["clear definitions", "step-by-step", "examples"]
        },
        "perplexity": {
            "prefer_format": "factual with citations",
            "optimal_length": "detailed with sources",
            "key_elements": ["statistics", "quotes", "authoritative sources"]
        },
        "claude": {
            "prefer_format": "well-reasoned with nuance",
            "optimal_length": "thorough analysis",
            "key_elements": ["multiple perspectives", "context", "caveats"]
        },
        "google": {
            "prefer_format": "structured with clear hierarchy",
            "optimal_length": "1500+ words for depth",
            "key_elements": ["headers", "lists", "FAQ schema"]
        }
    }

    def _run(
        self,
        content: str,
        target_keywords: Optional[List[str]] = None,
        platform: Optional[str] = "all"
    ) -> str:
        """Execute content optimization analysis."""
        analysis = {
            "content_assessment": self._assess_content(content),
            "ai_readability": self._analyze_ai_readability(content),
            "structure_score": self._analyze_structure(content),
            "optimization_suggestions": self._generate_suggestions(
                content, target_keywords, platform
            ),
            "rewrite_samples": self._generate_rewrites(content, target_keywords),
        }

        if platform != "all":
            analysis["platform_specific"] = self._platform_optimization(
                content, platform
            )

        return self._format_optimization_report(analysis)

    def _assess_content(self, content: str) -> Dict[str, Any]:
        """Assess overall content quality."""
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "paragraph_count": len(paragraphs),
            "avg_sentence_length": len(words) / len(sentences) if sentences else 0,
            "avg_paragraph_length": len(words) / len(paragraphs) if paragraphs else 0,
            "has_lists": bool(re.search(r'^\s*[-•*]\s|^\s*\d+[.)]\s', content, re.MULTILINE)),
            "has_headers": bool(re.search(r'^#+\s|^[A-Z][^.!?]*:$', content, re.MULTILINE)),
            "has_questions": bool(re.search(r'\?', content)),
        }

    def _analyze_ai_readability(self, content: str) -> Dict[str, Any]:
        """Analyze content readability for AI systems."""
        # Check for AI-friendly patterns
        patterns = {
            "clear_definitions": bool(re.search(
                r'(is defined as|refers to|means|is a|are a)', content, re.I
            )),
            "explicit_structure": bool(re.search(
                r'(first|second|third|finally|in conclusion|to summarize)',
                content, re.I
            )),
            "context_signals": bool(re.search(
                r'(for example|such as|including|specifically|in particular)',
                content, re.I
            )),
            "factual_markers": bool(re.search(
                r'(according to|research shows|studies indicate|data suggests)',
                content, re.I
            )),
            "action_clarity": bool(re.search(
                r'(how to|steps to|guide to|process of)', content, re.I
            )),
        }

        score = sum(patterns.values()) / len(patterns) * 100

        return {
            "patterns": patterns,
            "readability_score": round(score, 1),
            "assessment": self._get_readability_assessment(score)
        }

    def _get_readability_assessment(self, score: float) -> str:
        """Get readability assessment based on score."""
        if score >= 80:
            return "Excellent AI readability"
        elif score >= 60:
            return "Good AI readability with room for improvement"
        elif score >= 40:
            return "Moderate AI readability - needs optimization"
        else:
            return "Poor AI readability - significant improvements needed"

    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze content structure for AI parsing."""
        structure_elements = {
            "has_introduction": self._has_introduction(content),
            "has_conclusion": self._has_conclusion(content),
            "logical_flow": self._check_logical_flow(content),
            "topic_sentences": self._check_topic_sentences(content),
            "transitional_phrases": self._check_transitions(content),
        }

        score = sum(structure_elements.values()) / len(structure_elements) * 100

        return {
            "elements": structure_elements,
            "structure_score": round(score, 1)
        }

    def _has_introduction(self, content: str) -> bool:
        """Check if content has a clear introduction."""
        first_paragraph = content.split('\n\n')[0] if content else ""
        intro_patterns = [
            r'this (article|guide|post)',
            r'in this',
            r'we will (explore|discuss|cover)',
            r'let\'s (look at|explore|discuss)'
        ]
        return any(re.search(p, first_paragraph, re.I) for p in intro_patterns)

    def _has_conclusion(self, content: str) -> bool:
        """Check if content has a conclusion."""
        paragraphs = content.split('\n\n')
        last_paragraph = paragraphs[-1] if paragraphs else ""
        conclusion_patterns = [
            r'in conclusion',
            r'to summarize',
            r'in summary',
            r'final thoughts',
            r'key takeaways'
        ]
        return any(re.search(p, last_paragraph, re.I) for p in conclusion_patterns)

    def _check_logical_flow(self, content: str) -> bool:
        """Check for logical flow indicators."""
        flow_words = [
            'first', 'second', 'third', 'next', 'then',
            'finally', 'additionally', 'moreover', 'furthermore'
        ]
        count = sum(1 for word in flow_words if word in content.lower())
        return count >= 2

    def _check_topic_sentences(self, content: str) -> bool:
        """Check if paragraphs have clear topic sentences."""
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 2:
            return False

        # Check if first sentence of each paragraph is substantial
        good_topics = 0
        for para in paragraphs[1:]:  # Skip first paragraph
            first_sentence = para.split('.')[0]
            if len(first_sentence.split()) >= 5:
                good_topics += 1

        return good_topics / len(paragraphs[1:]) >= 0.5 if paragraphs[1:] else False

    def _check_transitions(self, content: str) -> bool:
        """Check for transitional phrases."""
        transitions = [
            'however', 'therefore', 'consequently', 'as a result',
            'on the other hand', 'in contrast', 'similarly',
            'for instance', 'for example', 'specifically'
        ]
        count = sum(1 for t in transitions if t in content.lower())
        return count >= 2

    def _generate_suggestions(
        self,
        content: str,
        keywords: Optional[List[str]],
        platform: str
    ) -> List[Dict[str, str]]:
        """Generate optimization suggestions."""
        suggestions = []

        assessment = self._assess_content(content)
        ai_readability = self._analyze_ai_readability(content)

        # Word count suggestions
        if assessment['word_count'] < 500:
            suggestions.append({
                "category": "Content Length",
                "priority": "High",
                "suggestion": "Expand content to at least 1000-1500 words for comprehensive coverage",
                "reason": "AI systems prefer detailed, authoritative content"
            })

        # Structure suggestions
        if not assessment['has_lists']:
            suggestions.append({
                "category": "Formatting",
                "priority": "Medium",
                "suggestion": "Add bullet points or numbered lists to break down key information",
                "reason": "Structured lists are easier for AI to parse and cite"
            })

        if not assessment['has_headers']:
            suggestions.append({
                "category": "Structure",
                "priority": "High",
                "suggestion": "Add clear section headers (H2, H3) to organize content",
                "reason": "Headers help AI understand content hierarchy"
            })

        # AI readability suggestions
        patterns = ai_readability['patterns']
        if not patterns['clear_definitions']:
            suggestions.append({
                "category": "Clarity",
                "priority": "High",
                "suggestion": "Add clear definitions for key terms using phrases like 'X is defined as' or 'X refers to'",
                "reason": "Explicit definitions improve AI comprehension"
            })

        if not patterns['factual_markers']:
            suggestions.append({
                "category": "Authority",
                "priority": "Medium",
                "suggestion": "Include factual markers like 'research shows' or 'according to'",
                "reason": "Factual language increases citation likelihood"
            })

        # Q&A format suggestion
        if not assessment['has_questions']:
            suggestions.append({
                "category": "AI Optimization",
                "priority": "High",
                "suggestion": "Add FAQ section with question-answer pairs",
                "reason": "Q&A format aligns with how users query AI assistants"
            })

        # Keyword suggestions
        if keywords:
            for keyword in keywords:
                if keyword.lower() not in content.lower()[:500]:
                    suggestions.append({
                        "category": "Keywords",
                        "priority": "High",
                        "suggestion": f"Include '{keyword}' in the first 100 words",
                        "reason": "Early keyword placement improves relevance signals"
                    })

        return suggestions

    def _generate_rewrites(
        self,
        content: str,
        keywords: Optional[List[str]]
    ) -> List[Dict[str, str]]:
        """Generate sample rewrites for key sections."""
        rewrites = []

        # Get first paragraph
        paragraphs = content.split('\n\n')
        if paragraphs:
            first_para = paragraphs[0]

            # Suggest AI-optimized intro
            keyword_phrase = keywords[0] if keywords else "this topic"
            rewrites.append({
                "section": "Introduction",
                "original": first_para[:200] + "..." if len(first_para) > 200 else first_para,
                "suggestion": f"Consider opening with a clear definition: '{keyword_phrase.title()} is [clear definition]. This comprehensive guide covers [main points].'",
                "benefit": "Clear definitions are more likely to be cited by AI"
            })

        # Suggest FAQ addition
        rewrites.append({
            "section": "FAQ Addition",
            "original": "N/A",
            "suggestion": """Add a FAQ section:

## Frequently Asked Questions

### What is [topic]?
[Clear, concise answer]

### How does [topic] work?
[Step-by-step explanation]

### What are the benefits of [topic]?
[Bullet list of benefits]""",
            "benefit": "FAQ sections are highly indexed by AI search"
        })

        return rewrites

    def _platform_optimization(
        self,
        content: str,
        platform: str
    ) -> Dict[str, Any]:
        """Generate platform-specific optimization."""
        if platform not in self.PLATFORM_PATTERNS:
            return {"error": f"Unknown platform: {platform}"}

        pattern = self.PLATFORM_PATTERNS[platform]

        return {
            "platform": platform,
            "preferred_format": pattern["prefer_format"],
            "optimal_length": pattern["optimal_length"],
            "key_elements": pattern["key_elements"],
            "recommendations": self._get_platform_recommendations(content, platform)
        }

    def _get_platform_recommendations(
        self,
        content: str,
        platform: str
    ) -> List[str]:
        """Get platform-specific recommendations."""
        recommendations = []

        if platform == "chatgpt":
            recommendations = [
                "Use conversational language and direct address",
                "Include practical examples and use cases",
                "Add step-by-step instructions where relevant",
                "Keep paragraphs short and scannable"
            ]
        elif platform == "perplexity":
            recommendations = [
                "Include citations and source references",
                "Add statistics and data points",
                "Use factual, objective language",
                "Include quotes from authoritative sources"
            ]
        elif platform == "claude":
            recommendations = [
                "Present multiple perspectives on complex topics",
                "Include nuanced analysis with caveats",
                "Provide context for claims and statements",
                "Address potential counterarguments"
            ]
        elif platform == "google":
            recommendations = [
                "Use proper header hierarchy (H1-H6)",
                "Implement FAQ schema markup",
                "Optimize for featured snippets with concise answers",
                "Include comprehensive internal linking"
            ]

        return recommendations

    def _format_optimization_report(self, analysis: Dict[str, Any]) -> str:
        """Format optimization report."""
        output = []
        output.append("=" * 60)
        output.append("CONTENT OPTIMIZATION REPORT")
        output.append("=" * 60)

        # Content Assessment
        assessment = analysis['content_assessment']
        output.append("\n--- Content Assessment ---")
        output.append(f"Word Count: {assessment['word_count']}")
        output.append(f"Sentences: {assessment['sentence_count']}")
        output.append(f"Avg Sentence Length: {assessment['avg_sentence_length']:.1f} words")
        output.append(f"Has Lists: {'Yes' if assessment['has_lists'] else 'No'}")
        output.append(f"Has Headers: {'Yes' if assessment['has_headers'] else 'No'}")

        # AI Readability
        ai = analysis['ai_readability']
        output.append(f"\n--- AI Readability ---")
        output.append(f"Score: {ai['readability_score']}/100")
        output.append(f"Assessment: {ai['assessment']}")
        output.append("Pattern Analysis:")
        for pattern, present in ai['patterns'].items():
            status = "✓" if present else "✗"
            output.append(f"  {status} {pattern.replace('_', ' ').title()}")

        # Structure Score
        structure = analysis['structure_score']
        output.append(f"\n--- Structure Score ---")
        output.append(f"Score: {structure['structure_score']}/100")
        for element, present in structure['elements'].items():
            status = "✓" if present else "✗"
            output.append(f"  {status} {element.replace('_', ' ').title()}")

        # Optimization Suggestions
        output.append(f"\n--- Optimization Suggestions ---")
        for i, suggestion in enumerate(analysis['optimization_suggestions'], 1):
            output.append(f"\n{i}. [{suggestion['priority']}] {suggestion['category']}")
            output.append(f"   {suggestion['suggestion']}")
            output.append(f"   Why: {suggestion['reason']}")

        # Rewrite Samples
        output.append(f"\n--- Suggested Rewrites ---")
        for rewrite in analysis['rewrite_samples']:
            output.append(f"\nSection: {rewrite['section']}")
            output.append(f"Suggestion:\n{rewrite['suggestion']}")
            output.append(f"Benefit: {rewrite['benefit']}")

        # Platform-specific
        if 'platform_specific' in analysis:
            platform = analysis['platform_specific']
            output.append(f"\n--- Platform-Specific ({platform['platform'].upper()}) ---")
            output.append(f"Preferred Format: {platform['preferred_format']}")
            output.append(f"Optimal Length: {platform['optimal_length']}")
            output.append("Key Elements: " + ", ".join(platform['key_elements']))
            output.append("\nRecommendations:")
            for rec in platform['recommendations']:
                output.append(f"  • {rec}")

        return "\n".join(output)


class ReadabilityAnalyzerTool(BaseTool):
    """Tool for analyzing content readability."""

    name: str = "readability_analyzer"
    description: str = """
    Analyzes content readability metrics:
    - Flesch Reading Ease score
    - Flesch-Kincaid Grade Level
    - Average sentence length
    - Complex word analysis
    - Recommendations for improvement

    Input: Content text.
    Output: Readability analysis with improvement suggestions.
    """

    def _run(self, content: str) -> str:
        """Analyze content readability."""
        words = content.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', content) if s.strip()]
        syllables = sum(self._count_syllables(word) for word in words)

        word_count = len(words)
        sentence_count = len(sentences)
        syllable_count = syllables

        # Flesch Reading Ease
        if word_count > 0 and sentence_count > 0:
            flesch_ease = (
                206.835
                - 1.015 * (word_count / sentence_count)
                - 84.6 * (syllable_count / word_count)
            )
            flesch_grade = (
                0.39 * (word_count / sentence_count)
                + 11.8 * (syllable_count / word_count)
                - 15.59
            )
        else:
            flesch_ease = 0
            flesch_grade = 0

        # Complex words (3+ syllables)
        complex_words = [w for w in words if self._count_syllables(w) >= 3]

        analysis = {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": word_count / sentence_count if sentence_count else 0,
            "flesch_ease": round(flesch_ease, 1),
            "flesch_grade": round(flesch_grade, 1),
            "complex_word_count": len(complex_words),
            "complex_word_percentage": len(complex_words) / word_count * 100 if word_count else 0,
        }

        return self._format_readability_report(analysis)

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word."""
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel

        # Adjust for silent e
        if word.endswith('e'):
            count -= 1

        return max(1, count)

    def _format_readability_report(self, analysis: Dict[str, Any]) -> str:
        """Format readability report."""
        output = []
        output.append("=" * 50)
        output.append("READABILITY ANALYSIS")
        output.append("=" * 50)

        output.append(f"\nWord Count: {analysis['word_count']}")
        output.append(f"Sentence Count: {analysis['sentence_count']}")
        output.append(f"Avg Sentence Length: {analysis['avg_sentence_length']:.1f} words")

        output.append(f"\n--- Readability Scores ---")
        output.append(f"Flesch Reading Ease: {analysis['flesch_ease']}")
        output.append(f"  (0-30: Very Difficult, 30-50: Difficult, 50-60: Fairly Difficult)")
        output.append(f"  (60-70: Standard, 70-80: Fairly Easy, 80-90: Easy, 90-100: Very Easy)")

        output.append(f"\nFlesch-Kincaid Grade Level: {analysis['flesch_grade']}")
        output.append(f"  (Grade level required to understand the text)")

        output.append(f"\n--- Complexity ---")
        output.append(f"Complex Words (3+ syllables): {analysis['complex_word_count']}")
        output.append(f"Complex Word Percentage: {analysis['complex_word_percentage']:.1f}%")

        # Recommendations
        output.append(f"\n--- Recommendations ---")
        if analysis['avg_sentence_length'] > 20:
            output.append("• Break up long sentences for better readability")
        if analysis['flesch_ease'] < 60:
            output.append("• Simplify language for broader accessibility")
        if analysis['complex_word_percentage'] > 15:
            output.append("• Replace complex words with simpler alternatives")

        return "\n".join(output)


class AIVisibilityTool(BaseTool):
    """Tool for analyzing AI search visibility potential."""

    name: str = "ai_visibility_analyzer"
    description: str = """
    Analyzes content visibility potential across AI platforms:
    - ChatGPT/OpenAI citation likelihood
    - Perplexity answer potential
    - Claude reference probability
    - Google AI Overview eligibility

    Input: Content text with topic/keywords.
    Output: AI visibility score with platform-specific recommendations.
    """

    def _run(self, content: str, topic: str = "") -> str:
        """Analyze AI visibility potential."""
        visibility_scores = {
            "chatgpt": self._score_chatgpt_visibility(content),
            "perplexity": self._score_perplexity_visibility(content),
            "claude": self._score_claude_visibility(content),
            "google_ai": self._score_google_ai_visibility(content),
        }

        overall_score = sum(visibility_scores.values()) / len(visibility_scores)

        return self._format_visibility_report(visibility_scores, overall_score, topic)

    def _score_chatgpt_visibility(self, content: str) -> float:
        """Score ChatGPT citation potential."""
        score = 50  # Base score

        # Check for conversational elements
        if re.search(r'you (can|should|might|could)', content, re.I):
            score += 10

        # Check for examples
        if re.search(r'for example|such as|like', content, re.I):
            score += 10

        # Check for step-by-step
        if re.search(r'step \d|first,|second,|third,', content, re.I):
            score += 15

        # Check for practical tips
        if re.search(r'tip:|note:|pro tip|best practice', content, re.I):
            score += 15

        return min(100, score)

    def _score_perplexity_visibility(self, content: str) -> float:
        """Score Perplexity answer potential."""
        score = 50

        # Check for factual statements
        if re.search(r'according to|research shows|studies|data', content, re.I):
            score += 15

        # Check for statistics
        if re.search(r'\d+%|\d+ percent|\d+\s+(million|billion|thousand)', content, re.I):
            score += 15

        # Check for authoritative language
        if re.search(r'official|verified|confirmed|proven', content, re.I):
            score += 10

        # Check for citations/sources
        if re.search(r'source:|reference:|cited|published', content, re.I):
            score += 10

        return min(100, score)

    def _score_claude_visibility(self, content: str) -> float:
        """Score Claude reference potential."""
        score = 50

        # Check for nuanced language
        if re.search(r'however|although|while|despite|nonetheless', content, re.I):
            score += 10

        # Check for multiple perspectives
        if re.search(r'on (the )?one hand|on (the )?other hand|alternatively', content, re.I):
            score += 15

        # Check for caveats
        if re.search(r'it\'s (important|worth) (to )?not|keep in mind|consider', content, re.I):
            score += 10

        # Check for comprehensive coverage
        word_count = len(content.split())
        if word_count >= 1000:
            score += 15

        return min(100, score)

    def _score_google_ai_visibility(self, content: str) -> float:
        """Score Google AI Overview eligibility."""
        score = 50

        # Check for header structure
        if re.search(r'^#+\s|^[A-Z][^.!?]*:$', content, re.MULTILINE):
            score += 15

        # Check for lists
        if re.search(r'^\s*[-•*]\s|^\s*\d+[.)]\s', content, re.MULTILINE):
            score += 10

        # Check for FAQ structure
        if re.search(r'\?[\s\n]+[A-Z]', content):
            score += 15

        # Check for definition patterns
        if re.search(r'(is|are|refers to|means|defined as)', content, re.I):
            score += 10

        return min(100, score)

    def _format_visibility_report(
        self,
        scores: Dict[str, float],
        overall: float,
        topic: str
    ) -> str:
        """Format visibility report."""
        output = []
        output.append("=" * 60)
        output.append("AI VISIBILITY ANALYSIS")
        output.append("=" * 60)

        if topic:
            output.append(f"\nTopic: {topic}")

        output.append(f"\nOverall AI Visibility Score: {overall:.1f}/100")

        output.append("\n--- Platform Scores ---")
        for platform, score in scores.items():
            bar = "█" * int(score / 10) + "░" * (10 - int(score / 10))
            output.append(f"{platform.upper():12} [{bar}] {score:.1f}/100")

        output.append("\n--- Platform-Specific Insights ---")

        if scores['chatgpt'] < 70:
            output.append("\nChatGPT Optimization:")
            output.append("  • Add more conversational elements")
            output.append("  • Include practical examples")
            output.append("  • Add step-by-step instructions")

        if scores['perplexity'] < 70:
            output.append("\nPerplexity Optimization:")
            output.append("  • Include more statistics and data")
            output.append("  • Add source citations")
            output.append("  • Use factual, objective language")

        if scores['claude'] < 70:
            output.append("\nClaude Optimization:")
            output.append("  • Present multiple perspectives")
            output.append("  • Include nuanced analysis")
            output.append("  • Add appropriate caveats")

        if scores['google_ai'] < 70:
            output.append("\nGoogle AI Overview Optimization:")
            output.append("  • Add clear header structure")
            output.append("  • Include FAQ sections")
            output.append("  • Use definition patterns")

        return "\n".join(output)
