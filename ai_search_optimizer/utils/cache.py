"""
Cache Manager for AI Search Optimization.
"""

import os
import json
import hashlib
import time
from typing import Any, Optional
from pathlib import Path

from ai_search_optimizer.config import settings


class CacheManager:
    """
    Simple file-based cache manager for storing analysis results.
    """

    def __init__(self, cache_dir: str = None, ttl: int = None):
        """
        Initialize the cache manager.

        Args:
            cache_dir: Directory for cache files (default from settings)
            ttl: Time-to-live in seconds (default from settings)
        """
        self.cache_dir = Path(cache_dir or settings.cache_dir)
        self.ttl = ttl or settings.cache_ttl
        self.enabled = settings.cache_enabled

        # Create cache directory if it doesn't exist
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_key(self, *args, **kwargs) -> str:
        """
        Generate a cache key from arguments.

        Args:
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            MD5 hash string as cache key
        """
        # Create a string representation of all arguments
        key_parts = [str(arg) for arg in args]
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_string = "|".join(key_parts)

        # Generate MD5 hash
        return hashlib.md5(key_string.encode()).hexdigest()

    def _get_cache_path(self, key: str) -> Path:
        """
        Get the file path for a cache key.

        Args:
            key: Cache key

        Returns:
            Path to cache file
        """
        return self.cache_dir / f"{key}.json"

    def get(self, *args, **kwargs) -> Optional[Any]:
        """
        Get a cached value.

        Args:
            *args: Arguments used to generate cache key
            **kwargs: Keyword arguments used to generate cache key

        Returns:
            Cached value or None if not found/expired
        """
        if not self.enabled:
            return None

        key = self._generate_key(*args, **kwargs)
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)

            # Check if expired
            if time.time() - cached_data.get('timestamp', 0) > self.ttl:
                # Remove expired cache
                cache_path.unlink(missing_ok=True)
                return None

            return cached_data.get('value')

        except (json.JSONDecodeError, IOError):
            return None

    def set(self, value: Any, *args, **kwargs) -> bool:
        """
        Set a cached value.

        Args:
            value: Value to cache
            *args: Arguments used to generate cache key
            **kwargs: Keyword arguments used to generate cache key

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False

        key = self._generate_key(*args, **kwargs)
        cache_path = self._get_cache_path(key)

        try:
            cached_data = {
                'timestamp': time.time(),
                'value': value,
            }

            with open(cache_path, 'w') as f:
                json.dump(cached_data, f)

            return True

        except (IOError, TypeError):
            return False

    def delete(self, *args, **kwargs) -> bool:
        """
        Delete a cached value.

        Args:
            *args: Arguments used to generate cache key
            **kwargs: Keyword arguments used to generate cache key

        Returns:
            True if deleted, False otherwise
        """
        if not self.enabled:
            return False

        key = self._generate_key(*args, **kwargs)
        cache_path = self._get_cache_path(key)

        try:
            cache_path.unlink(missing_ok=True)
            return True
        except IOError:
            return False

    def clear(self) -> int:
        """
        Clear all cached values.

        Returns:
            Number of cache files deleted
        """
        if not self.enabled:
            return 0

        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                count += 1
            except IOError:
                pass

        return count

    def cleanup_expired(self) -> int:
        """
        Remove all expired cache entries.

        Returns:
            Number of expired entries removed
        """
        if not self.enabled:
            return 0

        count = 0
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)

                if current_time - cached_data.get('timestamp', 0) > self.ttl:
                    cache_file.unlink()
                    count += 1

            except (json.JSONDecodeError, IOError):
                # Remove corrupted cache files
                try:
                    cache_file.unlink()
                    count += 1
                except IOError:
                    pass

        return count

    def get_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        if not self.enabled:
            return {'enabled': False}

        total_files = 0
        total_size = 0
        expired_count = 0
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            total_files += 1
            total_size += cache_file.stat().st_size

            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)
                if current_time - cached_data.get('timestamp', 0) > self.ttl:
                    expired_count += 1
            except:
                expired_count += 1

        return {
            'enabled': True,
            'cache_dir': str(self.cache_dir),
            'ttl_seconds': self.ttl,
            'total_entries': total_files,
            'expired_entries': expired_count,
            'valid_entries': total_files - expired_count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
        }


# Global cache instance
cache = CacheManager()
