"""
Advanced Filter Engine
Supports dynamic filtering on any column with various operators
"""
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd


class FilterParser:
    """Parse and validate filter queries"""
    
    # Supported operators
    OPERATORS = {
        '>=': 'gte',
        '<=': 'lte',
        '>': 'gt',
        '<': 'lt',
        '==': 'eq',
        '!=': 'ne'
    }
    
    OPERATOR_SYMBOLS = {v: k for k, v in OPERATORS.items()}
    
    @staticmethod
    def parse_filter(filter_string: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Parse a filter string into components
        
        Args:
            filter_string: Filter query (e.g., "revenue > 500")
            
        Returns:
            Tuple of (is_valid, filter_dict, error_message)
        """
        if not filter_string or not filter_string.strip():
            return True, None, ""
        
        try:
            # Match pattern: "column operator value"
            pattern = r'(\w+)\s*(>=|<=|>|<|==|!=)\s*(.+)'
            match = re.match(pattern, filter_string.strip())
            
            if not match:
                return False, None, "❌ Invalid filter format. Use: column operator value (e.g., revenue > 500)"
            
            column, operator, value = match.groups()
            
            # Try to parse value
            try:
                # Try numeric
                numeric_value = float(value.strip())
                value_type = 'numeric'
            except:
                # Try date
                try:
                    datetime.strptime(value.strip(), '%Y-%m-%d')
                    numeric_value = value.strip()
                    value_type = 'date'
                except:
                    # String value
                    numeric_value = value.strip()
                    value_type = 'string'
            
            filter_dict = {
                'column': column.strip(),
                'operator': FilterParser.OPERATORS[operator],
                'operator_symbol': operator,
                'value': numeric_value,
                'value_type': value_type
            }
            
            return True, filter_dict, ""
        
        except Exception as e:
            return False, None, f"❌ Error parsing filter: {str(e)}"
    
    @staticmethod
    def parse_between_filter(filter_string: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        """
        Parse a between filter
        
        Args:
            filter_string: Filter query (e.g., "revenue between 100 and 500")
            
        Returns:
            Tuple of (is_valid, filter_dict, error_message)
        """
        if 'between' not in filter_string.lower():
            return False, None, "Not a between filter"
        
        try:
            pattern = r'(\w+)\s+between\s+(.+?)\s+and\s+(.+)'
            match = re.match(pattern, filter_string.strip(), re.IGNORECASE)
            
            if not match:
                return False, None, "❌ Invalid between format. Use: column between value1 and value2"
            
            column, value1, value2 = match.groups()
            
            try:
                v1 = float(value1.strip())
                v2 = float(value2.strip())
            except:
                return False, None, "❌ Between values must be numeric"
            
            # Ensure v1 <= v2
            if v1 > v2:
                v1, v2 = v2, v1
            
            filter_dict = {
                'column': column.strip(),
                'operator': 'between',
                'value1': v1,
                'value2': v2
            }
            
            return True, filter_dict, ""
        
        except Exception as e:
            return False, None, f"❌ Error parsing between filter: {str(e)}"


class FilterEngine:
    """Apply filters to DataFrames dynamically"""
    
    @staticmethod
    def apply_filter(df: pd.DataFrame, filter_dict: Dict[str, Any]) -> Tuple[pd.DataFrame, str]:
        """
        Apply a single filter to DataFrame
        
        Args:
            df: Input DataFrame
            filter_dict: Filter specification
            
        Returns:
            Tuple of (filtered_df, error_message)
        """
        try:
            if not filter_dict:
                return df, ""
            
            column = filter_dict['column']
            
            # Check column exists
            if column not in df.columns:
                return df, f"❌ Column '{column}' not found"
            
            if filter_dict['operator'] == 'between':
                # Between filter
                v1 = filter_dict['value1']
                v2 = filter_dict['value2']
                result = df[(df[column] >= v1) & (df[column] <= v2)]
            else:
                operator = filter_dict['operator']
                value = filter_dict['value']
                
                if operator == 'gte':
                    result = df[df[column] >= value]
                elif operator == 'lte':
                    result = df[df[column] <= value]
                elif operator == 'gt':
                    result = df[df[column] > value]
                elif operator == 'lt':
                    result = df[df[column] < value]
                elif operator == 'eq':
                    result = df[df[column] == value]
                elif operator == 'ne':
                    result = df[df[column] != value]
                else:
                    return df, f"❌ Unknown operator: {operator}"
            
            if result.empty:
                return result, f"⚠️ No records match filter: {column} {filter_dict.get('operator_symbol', '')} {value}"
            
            return result, ""
        
        except Exception as e:
            return df, f"❌ Error applying filter: {str(e)}"
    
    @staticmethod
    def apply_multiple_filters(df: pd.DataFrame, filters: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, str]:
        """
        Apply multiple filters (AND logic)
        
        Args:
            df: Input DataFrame
            filters: List of filter specifications
            
        Returns:
            Tuple of (filtered_df, error_message)
        """
        result = df.copy()
        errors = []
        
        for filter_dict in filters:
            result, error = FilterEngine.apply_filter(result, filter_dict)
            if error:
                errors.append(error)
        
        error_msg = " | ".join(errors) if errors else ""
        return result, error_msg
    
    @staticmethod
    def get_filter_sql(filter_dict: Dict[str, Any]) -> str:
        """
        Convert filter to SQL WHERE clause
        
        Args:
            filter_dict: Filter specification
            
        Returns:
            SQL WHERE clause
        """
        if not filter_dict:
            return ""
        
        column = filter_dict['column']
        
        if filter_dict['operator'] == 'between':
            return f"WHERE {column} BETWEEN {filter_dict['value1']} AND {filter_dict['value2']}"
        
        operator_symbol = filter_dict.get('operator_symbol', '=')
        value = filter_dict['value']
        
        # Quote string values
        if filter_dict.get('value_type') == 'string':
            value = f"'{value}'"
        
        return f"WHERE {column} {operator_symbol} {value}"
