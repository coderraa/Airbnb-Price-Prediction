"""
Helper Utilities for AI Search Optimization.
"""

import re
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from collections import Counter


def extract_text_from_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    Extract text content from a URL.

    Args:
        url: The URL to extract text from
        timeout: Request timeout in seconds

    Returns:
        Extracted text content or None if failed
    """
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={'User-Agent': 'Mozilla/5.0 (compatible; AISearchOptimizer/1.0)'}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()

        # Get text
        text = soup.get_text(separator=' ', strip=True)

        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)

        return text

    except Exception as e:
        print(f"Error extracting text from URL: {e}")
        return None


def calculate_word_count(text: str) -> Dict[str, int]:
    """
    Calculate word count statistics for text.

    Args:
        text: The text to analyze

    Returns:
        Dictionary with word count statistics
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    return {
        'total_words': len(words),
        'total_sentences': len(sentences),
        'total_paragraphs': len(paragraphs),
        'avg_words_per_sentence': len(words) / len(sentences) if sentences else 0,
        'avg_words_per_paragraph': len(words) / len(paragraphs) if paragraphs else 0,
        'unique_words': len(set(word.lower() for word in words)),
    }


def extract_keywords_from_text(
    text: str,
    max_keywords: int = 20,
    min_word_length: int = 3
) -> List[Dict[str, Any]]:
    """
    Extract keywords from text using frequency analysis.

    Args:
        text: The text to extract keywords from
        max_keywords: Maximum number of keywords to return
        min_word_length: Minimum word length to consider

    Returns:
        List of keyword dictionaries with word and frequency
    """
    # Common stop words to exclude
    stop_words = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
        'into', 'through', 'during', 'before', 'after', 'above', 'below',
        'between', 'under', 'again', 'further', 'then', 'once', 'and', 'but',
        'or', 'nor', 'so', 'yet', 'both', 'either', 'neither', 'not', 'only',
        'own', 'same', 'than', 'too', 'very', 'just', 'also', 'now', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both',
        'few', 'more', 'most', 'other', 'some', 'such', 'no', 'any', 'this',
        'that', 'these', 'those', 'what', 'which', 'who', 'whom', 'whose',
    }

    # Extract words
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    # Filter and count
    filtered_words = [
        word for word in words
        if len(word) >= min_word_length and word not in stop_words
    ]

    word_freq = Counter(filtered_words)

    # Return top keywords
    return [
        {'keyword': word, 'frequency': count, 'density': count / len(words) * 100}
        for word, count in word_freq.most_common(max_keywords)
    ]


def format_report(
    title: str,
    sections: List[Dict[str, Any]],
    width: int = 60
) -> str:
    """
    Format a report with sections.

    Args:
        title: Report title
        sections: List of section dictionaries with 'heading' and 'content'
        width: Report width in characters

    Returns:
        Formatted report string
    """
    output = []

    # Header
    output.append("=" * width)
    output.append(title.center(width))
    output.append("=" * width)

    # Sections
    for section in sections:
        heading = section.get('heading', 'Section')
        content = section.get('content', '')

        output.append(f"\n--- {heading} ---")

        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    for key, value in item.items():
                        output.append(f"  {key}: {value}")
                else:
                    output.append(f"  • {item}")
        elif isinstance(content, dict):
            for key, value in content.items():
                output.append(f"  {key}: {value}")
        else:
            output.append(f"  {content}")

    output.append("\n" + "=" * width)

    return "\n".join(output)


def validate_url(url: str) -> Dict[str, Any]:
    """
    Validate a URL and return information about it.

    Args:
        url: The URL to validate

    Returns:
        Dictionary with validation results
    """
    result = {
        'valid': False,
        'url': url,
        'scheme': None,
        'domain': None,
        'path': None,
        'errors': [],
    }

    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in ('http', 'https'):
            result['errors'].append('Invalid or missing scheme (must be http or https)')
        else:
            result['scheme'] = parsed.scheme

        # Check domain
        if not parsed.netloc:
            result['errors'].append('Missing domain')
        else:
            result['domain'] = parsed.netloc

        # Store path
        result['path'] = parsed.path or '/'

        # URL is valid if no errors
        result['valid'] = len(result['errors']) == 0

    except Exception as e:
        result['errors'].append(f'URL parsing error: {str(e)}')

    return result


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """
    Sanitize input text for processing.

    Args:
        text: The text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."

    # Remove potentially harmful content
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL | re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.I)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def merge_analysis_results(*results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple analysis results into one.

    Args:
        *results: Variable number of result dictionaries

    Returns:
        Merged results dictionary
    """
    merged = {
        'success': all(r.get('success', True) for r in results),
        'analyses': [],
        'combined_recommendations': [],
        'errors': [],
    }

    for i, result in enumerate(results):
        if result.get('success', True):
            merged['analyses'].append({
                'index': i,
                'output': result.get('output', ''),
            })
            # Extract recommendations if present
            if 'recommendations' in result:
                merged['combined_recommendations'].extend(result['recommendations'])
        else:
            merged['errors'].append({
                'index': i,
                'error': result.get('error', 'Unknown error'),
            })

    return merged


def calculate_readability_score(text: str) -> Dict[str, float]:
    """
    Calculate readability scores for text.

    Args:
        text: The text to analyze

    Returns:
        Dictionary with readability scores
    """
    words = text.split()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

    if not words or not sentences:
        return {
            'flesch_ease': 0,
            'flesch_grade': 0,
            'avg_sentence_length': 0,
        }

    # Count syllables (simple approximation)
    def count_syllables(word: str) -> int:
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_vowel = False
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith('e'):
            count -= 1
        return max(1, count)

    total_syllables = sum(count_syllables(word) for word in words)
    word_count = len(words)
    sentence_count = len(sentences)

    # Flesch Reading Ease
    flesch_ease = (
        206.835
        - 1.015 * (word_count / sentence_count)
        - 84.6 * (total_syllables / word_count)
    )

    # Flesch-Kincaid Grade Level
    flesch_grade = (
        0.39 * (word_count / sentence_count)
        + 11.8 * (total_syllables / word_count)
        - 15.59
    )

    return {
        'flesch_ease': round(max(0, min(100, flesch_ease)), 1),
        'flesch_grade': round(max(0, flesch_grade), 1),
        'avg_sentence_length': round(word_count / sentence_count, 1),
        'avg_syllables_per_word': round(total_syllables / word_count, 2),
    }
