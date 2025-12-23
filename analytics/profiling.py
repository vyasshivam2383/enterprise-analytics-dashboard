"""
Data Profiling Module
Provides comprehensive column-wise statistical analysis
"""
import pandas as pd
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod


class ProfileAnalyzer(ABC):
    """Abstract base class for column profiling"""
    
    @abstractmethod
    def analyze(self, series: pd.Series) -> Dict[str, Any]:
        """Analyze a data series and return statistics"""
        pass
    
    def _safe_operation(self, func, series: pd.Series, default: Any = None):
        """Safely execute operations on series with error handling"""
        try:
            return func(series)
        except:
            return default


class NumericProfiler(ProfileAnalyzer):
    """Profile numeric columns"""
    
    def analyze(self, series: pd.Series) -> Dict[str, Any]:
        """
        Analyze numeric column
        
        Args:
            series: Pandas Series with numeric data
            
        Returns:
            Dictionary with statistics
        """
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {
                'type': 'numeric',
                'count': 0,
                'missing': len(series),
                'mean': None,
                'median': None,
                'std': None,
                'min': None,
                'max': None,
                'q25': None,
                'q75': None
            }
        
        return {
            'type': 'numeric',
            'count': len(clean_series),
            'missing': len(series) - len(clean_series),
            'mean': self._safe_operation(lambda s: float(s.mean()), clean_series),
            'median': self._safe_operation(lambda s: float(s.median()), clean_series),
            'std': self._safe_operation(lambda s: float(s.std()), clean_series, 0.0),
            'min': self._safe_operation(lambda s: float(s.min()), clean_series),
            'max': self._safe_operation(lambda s: float(s.max()), clean_series),
            'q25': self._safe_operation(lambda s: float(s.quantile(0.25)), clean_series),
            'q75': self._safe_operation(lambda s: float(s.quantile(0.75)), clean_series)
        }


class TextProfiler(ProfileAnalyzer):
    """Profile text/categorical columns"""
    
    def analyze(self, series: pd.Series) -> Dict[str, Any]:
        """
        Analyze text column
        
        Args:
            series: Pandas Series with text data
            
        Returns:
            Dictionary with statistics
        """
        clean_series = series.dropna()
        
        if len(clean_series) == 0:
            return {
                'type': 'text',
                'count': 0,
                'missing': len(series),
                'unique': 0,
                'most_frequent': None,
                'frequency': 0
            }
        
        value_counts = clean_series.value_counts()
        
        return {
            'type': 'text',
            'count': len(clean_series),
            'missing': len(series) - len(clean_series),
            'unique': clean_series.nunique(),
            'most_frequent': value_counts.index[0] if len(value_counts) > 0 else None,
            'frequency': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0
        }


class DataProfiler:
    """Main data profiling service"""
    
    def __init__(self):
        """Initialize profiler"""
        self.numeric_profiler = NumericProfiler()
        self.text_profiler = TextProfiler()
    
    def profile_dataframe(self, df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Profile all columns in a DataFrame
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with profiles for each column
        """
        profiles = {}
        
        for column in df.columns:
            series = df[column]
            
            # Infer type
            if pd.api.types.is_numeric_dtype(series):
                profiles[column] = self.numeric_profiler.analyze(series)
            else:
                profiles[column] = self.text_profiler.analyze(series)
        
        return profiles
    
    def profile_column(self, series: pd.Series) -> Dict[str, Any]:
        """
        Profile a single column
        
        Args:
            series: Input Series
            
        Returns:
            Profile dictionary
        """
        if pd.api.types.is_numeric_dtype(series):
            return self.numeric_profiler.analyze(series)
        else:
            return self.text_profiler.analyze(series)
    
    def get_summary_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get high-level summary statistics
        
        Args:
            df: Input DataFrame
            
        Returns:
            Summary statistics
        """
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'total_missing': int(df.isnull().sum().sum()),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'text_columns': len(df.select_dtypes(exclude=['number']).columns),
            'duplicate_rows': len(df[df.duplicated()])
        }
    
    def get_column_stats_for_display(self, df: pd.DataFrame, column: str) -> str:
        """
        Get formatted column statistics for UI display
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            Formatted statistics string
        """
        if column not in df.columns:
            return "❌ Column not found"
        
        profile = self.profile_column(df[column])
        
        if profile['type'] == 'numeric':
            return f"""
📊 **{column}** (Numeric)
- Count: {profile['count']}
- Missing: {profile['missing']}
- Mean: {profile['mean']:.2f}
- Median: {profile['median']:.2f}
- Std Dev: {profile['std']:.2f}
- Min: {profile['min']:.2f}
- Max: {profile['max']:.2f}
- Q1 (25%): {profile['q25']:.2f}
- Q3 (75%): {profile['q75']:.2f}
            """
        else:
            return f"""
📋 **{column}** (Text/Categorical)
- Count: {profile['count']}
- Missing: {profile['missing']}
- Unique Values: {profile['unique']}
- Most Frequent: '{profile['most_frequent']}'
- Frequency: {profile['frequency']}
            """
