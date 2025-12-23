"""
Grouping & Aggregation Engine
Supports GROUP BY operations dynamically on any column
"""
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd


class AggregationEngine:
    """Handle grouping and aggregation operations"""
    
    AGGREGATION_FUNCTIONS = {
        'sum': 'Sum',
        'mean': 'Average',
        'median': 'Median',
        'min': 'Minimum',
        'max': 'Maximum',
        'count': 'Count',
        'std': 'Std Dev'
    }
    
    @staticmethod
    def validate_grouping(df: pd.DataFrame, group_column: str, agg_column: str) -> Tuple[bool, str]:
        """
        Validate grouping parameters
        
        Args:
            df: Input DataFrame
            group_column: Column to group by
            agg_column: Column to aggregate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if group_column not in df.columns:
            return False, f"❌ Group column '{group_column}' not found"
        
        if agg_column not in df.columns:
            return False, f"❌ Aggregation column '{agg_column}' not found"
        
        return True, ""
    
    @staticmethod
    def group_and_aggregate(
        df: pd.DataFrame,
        group_column: str,
        agg_column: str,
        agg_function: str = 'sum'
    ) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Group by one column and aggregate another
        
        Args:
            df: Input DataFrame
            group_column: Column to group by
            agg_column: Column to aggregate
            agg_function: Aggregation function (sum, mean, min, max, count, std, median)
            
        Returns:
            Tuple of (result_df, error_message)
        """
        try:
            # Validate
            is_valid, error = AggregationEngine.validate_grouping(df, group_column, agg_column)
            if not is_valid:
                return None, error
            
            # Check if agg_function is valid
            if agg_function not in AggregationEngine.AGGREGATION_FUNCTIONS:
                return None, f"❌ Unknown aggregation: {agg_function}"
            
            # Group and aggregate
            if agg_function == 'count':
                result = df.groupby(group_column).size().reset_index(name=f'{agg_function}_{agg_column}')
            elif agg_function == 'median':
                result = df.groupby(group_column)[agg_column].median().reset_index()
                result.columns = [group_column, f'{agg_function}_{agg_column}']
            else:
                result = df.groupby(group_column)[agg_column].agg(agg_function).reset_index()
                result.columns = [group_column, f'{agg_function}_{agg_column}']
            
            return result, ""
        
        except Exception as e:
            return None, f"❌ Error in grouping: {str(e)}"
    
    @staticmethod
    def multi_aggregation(
        df: pd.DataFrame,
        group_column: str,
        agg_columns: Dict[str, List[str]]
    ) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Group by one column with multiple aggregations on multiple columns
        
        Args:
            df: Input DataFrame
            group_column: Column to group by
            agg_columns: Dict of {column_name: [agg_functions]}
            
        Returns:
            Tuple of (result_df, error_message)
        """
        try:
            if group_column not in df.columns:
                return None, f"❌ Group column '{group_column}' not found"
            
            # Build aggregation specification
            agg_spec = {}
            for col, funcs in agg_columns.items():
                if col not in df.columns:
                    return None, f"❌ Column '{col}' not found"
                
                for func in funcs:
                    if func not in AggregationEngine.AGGREGATION_FUNCTIONS:
                        return None, f"❌ Unknown aggregation: {func}"
                
                agg_spec[col] = funcs
            
            # Perform aggregation
            result = df.groupby(group_column).agg(agg_spec)
            result.columns = ['_'.join(col).strip() for col in result.columns.values]
            result = result.reset_index()
            
            return result, ""
        
        except Exception as e:
            return None, f"❌ Error in multi-aggregation: {str(e)}"
    
    @staticmethod
    def get_groupby_sql(
        group_column: str,
        agg_column: str,
        agg_function: str,
        table_name: str
    ) -> str:
        """
        Convert grouping to SQL query
        
        Args:
            group_column: Column to group by
            agg_column: Column to aggregate
            agg_function: SQL aggregation function
            table_name: Table name
            
        Returns:
            SQL query
        """
        agg_func_sql = {
            'sum': 'SUM',
            'mean': 'AVG',
            'min': 'MIN',
            'max': 'MAX',
            'count': 'COUNT',
            'median': 'MEDIAN',
            'std': 'STDDEV'
        }
        
        sql_func = agg_func_sql.get(agg_function, 'SUM')
        
        if agg_function == 'count':
            return f"SELECT {group_column}, COUNT(*) as count FROM {table_name} GROUP BY {group_column}"
        
        return f"SELECT {group_column}, {sql_func}({agg_column}) as {agg_function}_{agg_column} FROM {table_name} GROUP BY {group_column}"
    
    @staticmethod
    def get_unique_values(df: pd.DataFrame, column: str, limit: int = 100) -> List[Any]:
        """
        Get unique values from a column for grouping
        
        Args:
            df: Input DataFrame
            column: Column to get unique values from
            limit: Maximum values to return
            
        Returns:
            List of unique values
        """
        try:
            if column not in df.columns:
                return []
            
            return df[column].dropna().unique()[:limit].tolist()
        except:
            return []
    
    @staticmethod
    def validate_aggregations_available(df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Get available aggregations for each column
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dict of {column: [available_aggregations]}
        """
        available = {}
        
        for col in df.columns:
            available[col] = []
            
            if pd.api.types.is_numeric_dtype(df[col]):
                available[col] = ['sum', 'mean', 'min', 'max', 'median', 'std', 'count']
            else:
                available[col] = ['count']
        
        return available
