"""
Cache management
"""

from typing import Any, Dict, Optional, Callable
from functools import wraps
import hashlib
import pickle
import time


class Cache:
    """Simple cache implementation"""
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self._max_size = max_size
        self._ttl = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            return None
        
        if self._is_expired(key):
            self.remove(key)
            return None
        
        return self._cache[key]
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        if len(self._cache) >= self._max_size:
            self._evict_oldest()
        
        self._cache[key] = value
        self._timestamps[key] = time.time()
    
    def remove(self, key: str):
        """Remove value from cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._timestamps:
            del self._timestamps[key]
    
    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        self._timestamps.clear()
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired"""
        if key not in self._timestamps:
            return True
        
        age = time.time() - self._timestamps[key]
        return age > self._ttl
    
    def _evict_oldest(self):
        """Evict oldest cache entry"""
        if not self._timestamps:
            return
        
        oldest_key = min(self._timestamps, key=self._timestamps.get)
        self.remove(oldest_key)
    
    def size(self) -> int:
        """Get cache size"""
        return len(self._cache)
    
    def keys(self):
        """Get all cache keys"""
        return list(self._cache.keys())


class LRUCache:
    """Least Recently Used cache"""
    
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._order: Dict[str, int] = {}
        self._max_size = max_size
        self._counter = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            return None
        
        self._order[key] = self._counter
        self._counter += 1
        return self._cache[key]
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        if len(self._cache) >= self._max_size and key not in self._cache:
            self._evict_lru()
        
        self._cache[key] = value
        self._order[key] = self._counter
        self._counter += 1
    
    def remove(self, key: str):
        """Remove value from cache"""
        if key in self._cache:
            del self._cache[key]
        if key in self._order:
            del self._order[key]
    
    def clear(self):
        """Clear all cache entries"""
        self._cache.clear()
        self._order.clear()
        self._counter = 0
    
    def _evict_lru(self):
        """Evict least recently used entry"""
        if not self._order:
            return
        
        lru_key = min(self._order, key=self._order.get)
        self.remove(lru_key)
    
    def size(self) -> int:
        """Get cache size"""
        return len(self._cache)


def memoize(max_size: int = 128):
    """Memoization decorator"""
    cache = LRUCache(max_size)
    
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = _make_cache_key(func.__name__, args, kwargs)
            result = cache.get(key)
            
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result)
            
            return result
        
        wrapper.cache_clear = cache.clear
        wrapper.cache_info = lambda: {"size": cache.size()}
        return wrapper
    
    return decorator


def _make_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """Make cache key from function arguments"""
    key_data = {
        "func": func_name,
        "args": args,
        "kwargs": kwargs,
    }
    
    key_str = pickle.dumps(key_data, protocol=pickle.HIGHEST_PROTOCOL)
    return hashlib.md5(key_str).hexdigest()