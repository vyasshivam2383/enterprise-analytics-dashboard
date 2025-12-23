"""
Performance Optimization Module
Caches computations and optimizes database queries
"""
import hashlib
import json
from typing import Any, Dict, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta


class CacheManager:
    """
    Safe caching system for expensive computations
    Does NOT cache database objects - only computation results
    """
    
    def __init__(self, ttl_minutes: int = 60):
        """
        Initialize cache manager
        
        Args:
            ttl_minutes: Time-to-live for cached items in minutes
        """
        self.cache = {}
        self.ttl = ttl_minutes * 60  # Convert to seconds
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate cache key from function and arguments"""
        key_data = f"{func_name}:{str(args)}:{json.dumps(kwargs, default=str, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value if exists and not expired
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key in self.cache:
            value, timestamp = self.cache[key]
            
            # Check if expired
            if (datetime.now() - timestamp).total_seconds() < self.ttl:
                return value
            else:
                del self.cache[key]  # Remove expired
        
        return None
    
    def set(self, key: str, value: Any):
        """
        Set cache value with current timestamp
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = (value, datetime.now())
    
    def clear(self):
        """Clear all cached values"""
        self.cache.clear()
    
    def cleanup_expired(self):
        """Remove expired entries"""
        current_time = datetime.now()
        expired_keys = [
            k for k, (v, ts) in self.cache.items()
            if (current_time - ts).total_seconds() >= self.ttl
        ]
        
        for key in expired_keys:
            del self.cache[key]


class QueryOptimizer:
    """Optimize SQL queries for better performance"""
    
    @staticmethod
    def optimize_select_query(table_name: str, columns: list = None) -> str:
        """
        Generate optimized SELECT query
        
        Args:
            table_name: Table name
            columns: Columns to select (None = all)
            
        Returns:
            Optimized SQL query
        """
        if columns:
            cols_str = ', '.join(columns)
        else:
            cols_str = '*'
        
        return f"SELECT {cols_str} FROM {table_name}"
    
    @staticmethod
    def optimize_aggregation_query(
        table_name: str,
        column: str,
        operation: str
    ) -> str:
        """
        Generate optimized aggregation query
        
        Args:
            table_name: Table name
            column: Column to aggregate
            operation: Operation (sum, avg, min, max, count)
            
        Returns:
            Optimized SQL query
        """
        op_map = {
            'sum': 'SUM',
            'avg': 'AVG',
            'mean': 'AVG',
            'min': 'MIN',
            'max': 'MAX',
            'count': 'COUNT'
        }
        
        sql_op = op_map.get(operation.lower(), 'COUNT')
        
        if operation.lower() == 'count':
            return f"SELECT {sql_op}(*) FROM {table_name}"
        
        return f"SELECT {sql_op}({column}) FROM {table_name}"
    
    @staticmethod
    def optimize_filter_query(
        table_name: str,
        column: str,
        operator: str,
        value: Any
    ) -> str:
        """
        Generate optimized filtered query
        
        Args:
            table_name: Table name
            column: Column to filter
            operator: Comparison operator (>, <, >=, <=, ==, !=)
            value: Filter value
            
        Returns:
            Optimized SQL query
        """
        if isinstance(value, str):
            value = f"'{value}'"
        
        return f"SELECT * FROM {table_name} WHERE {column} {operator} {value}"


class ComputationCache:
    """Cache manager for analytics computations"""
    
    _cache_instance = CacheManager()
    
    @classmethod
    def cached_computation(cls, ttl_minutes: int = 60):
        """
        Decorator for caching expensive computations
        
        Args:
            ttl_minutes: Cache time-to-live in minutes
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                key = cls._cache_instance._generate_key(func.__name__, args, kwargs)
                
                # Check cache
                cached_result = cls._cache_instance.get(key)
                if cached_result is not None:
                    return cached_result
                
                # Compute and cache
                result = func(*args, **kwargs)
                cls._cache_instance.set(key, result)
                
                return result
            
            return wrapper
        
        return decorator
    
    @classmethod
    def clear_cache(cls):
        """Clear all computations cache"""
        cls._cache_instance.clear()
    
    @classmethod
    def cleanup_expired(cls):
        """Remove expired cache entries"""
        cls._cache_instance.cleanup_expired()
