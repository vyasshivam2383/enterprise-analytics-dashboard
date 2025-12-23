"""
Error handling utilities for Enterprise Analytics Dashboard
Provides robust error handling for data validation, file processing, and analytics operations
"""
import pandas as pd
from typing import Optional, Tuple, Dict, Any


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class DataProcessingError(Exception):
    """Custom exception for data processing errors"""
    pass


class AnalyticsError(Exception):
    """Custom exception for analytics computation errors"""
    pass


class ErrorHandler:
    """Central error handling and validation service"""
    
    @staticmethod
    def validate_csv_upload(df: pd.DataFrame, max_rows: int = 100000) -> Tuple[bool, str]:
        """
        Validate uploaded CSV file
        
        Args:
            df: DataFrame to validate
            max_rows: Maximum allowed rows
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if empty
            if df.empty:
                return False, "❌ CSV file is empty. Please upload a file with data."
            
            # Check row count
            if len(df) > max_rows:
                return False, f"❌ File exceeds {max_rows} rows. Please use a smaller file."
            
            # Check columns
            if len(df.columns) == 0:
                return False, "❌ CSV has no columns. Please check your file format."
            
            # Check for completely null columns
            null_cols = df.columns[df.isnull().all()].tolist()
            if null_cols:
                return False, f"❌ Columns are completely empty: {', '.join(null_cols)}"
            
            return True, ""
        
        except Exception as e:
            return False, f"❌ Error validating file: {str(e)}"
    
    @staticmethod
    def validate_column_exists(table_name: str, column_name: str, available_columns: list) -> Tuple[bool, str]:
        """
        Validate that a column exists in the data
        
        Args:
            table_name: Name of the table
            column_name: Column to check
            available_columns: List of available columns
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if column_name not in available_columns:
            return False, f"❌ Column '{column_name}' not found in {table_name}. Available: {', '.join(available_columns)}"
        return True, ""
    
    @staticmethod
    def validate_numeric_column(df: pd.DataFrame, column_name: str) -> Tuple[bool, str]:
        """
        Validate that a column contains numeric data
        
        Args:
            df: DataFrame
            column_name: Column to check
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if column_name not in df.columns:
                return False, f"❌ Column '{column_name}' not found in data."
            
            # Try to convert to numeric
            numeric_data = pd.to_numeric(df[column_name], errors='coerce')
            
            # Check if all values became NaN (meaning column is not numeric)
            if numeric_data.isnull().all():
                return False, f"❌ Column '{column_name}' contains non-numeric data. Cannot perform numeric operations."
            
            # Warn if some values are NaN
            if numeric_data.isnull().any():
                return True, f"⚠️ Column '{column_name}' has some missing values. They will be ignored in calculations."
            
            return True, ""
        
        except Exception as e:
            return False, f"❌ Error validating numeric column: {str(e)}"
    
    @staticmethod
    def validate_filter_query(filter_string: str) -> Tuple[bool, str]:
        """
        Validate filter query syntax
        
        Args:
            filter_string: Filter query (e.g., "revenue > 500")
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not filter_string or not filter_string.strip():
                return True, ""  # Empty filter is valid (no filtering)
            
            # Check for basic syntax
            operators = ['>', '<', '>=', '<=', '==', '!=', 'between']
            has_operator = any(op in filter_string.lower() for op in operators)
            
            if not has_operator:
                return False, "❌ Invalid filter syntax. Use operators like: >, <, >=, <=, ==, !="
            
            return True, ""
        
        except Exception as e:
            return False, f"❌ Error validating filter: {str(e)}"
    
    @staticmethod
    def safe_numeric_operation(data: list, operation: str) -> Tuple[Optional[float], str]:
        """
        Safely perform numeric operations with error handling
        
        Args:
            data: List of numbers
            operation: 'sum', 'mean', 'min', 'max', 'std'
            
        Returns:
            Tuple of (result, error_message)
        """
        try:
            if not data:
                return None, "❌ No data available for operation"
            
            # Filter out None and NaN
            valid_data = [x for x in data if x is not None and str(x) != 'nan']
            
            if not valid_data:
                return None, "❌ All data values are missing or invalid"
            
            # Convert to float
            numeric_data = [float(x) for x in valid_data]
            
            if operation == 'sum':
                return sum(numeric_data), ""
            elif operation == 'mean':
                return sum(numeric_data) / len(numeric_data), ""
            elif operation == 'min':
                return min(numeric_data), ""
            elif operation == 'max':
                return max(numeric_data), ""
            elif operation == 'std':
                import statistics
                return statistics.stdev(numeric_data) if len(numeric_data) > 1 else 0.0, ""
            else:
                return None, f"❌ Unknown operation: {operation}"
        
        except ValueError as e:
            return None, f"❌ Non-numeric data encountered: {str(e)}"
        except Exception as e:
            return None, f"❌ Error in {operation}: {str(e)}"
    
    @staticmethod
    def handle_analytics_error(error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle analytics errors gracefully
        
        Args:
            error: Exception object
            context: What operation was being performed
            
        Returns:
            Dictionary with error info and user message
        """
        error_msg = f"❌ Analytics error"
        if context:
            error_msg += f" ({context})"
        error_msg += f": {str(error)}"
        
        return {
            'success': False,
            'error_type': type(error).__name__,
            'error_message': error_msg,
            'user_message': f"Unable to compute analytics. Please check your data and filters."
        }
