"""
Dataset Management Module
Handle switching, deleting, and renaming datasets
"""
from typing import List, Tuple, Optional, Dict, Any
from database.db import Database


class DatasetManager:
    """Manage multiple datasets in the system"""
    
    def __init__(self):
        """Initialize dataset manager"""
        self.db = Database()
    
    def list_all_datasets(self) -> Tuple[List[str], str]:
        """
        List all tables in the database (datasets)
        
        Returns:
            Tuple of (table_names, error_message)
        """
        try:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            results = self.db.execute(query)
            
            tables = [row[0] for row in results] if results else []
            
            return tables, ""
        
        except Exception as e:
            return [], f"❌ Error listing datasets: {str(e)}"
    
    def get_dataset_info(self, table_name: str) -> Tuple[Optional[Dict[str, Any]], str]:
        """
        Get information about a dataset
        
        Args:
            table_name: Dataset name
            
        Returns:
            Tuple of (info_dict, error_message)
        """
        try:
            # Check if table exists
            if not self.table_exists(table_name):
                return None, f"❌ Dataset '{table_name}' not found"
            
            # Get row count
            count_result = self.db.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = count_result[0][0] if count_result else 0
            
            # Get columns
            cursor_info = self.db._connection.execute(f"PRAGMA table_info({table_name})")
            columns = [(row[1], row[2]) for row in cursor_info.fetchall()]  # name, type
            
            info = {
                'name': table_name,
                'row_count': row_count,
                'column_count': len(columns),
                'columns': columns
            }
            
            return info, ""
        
        except Exception as e:
            return None, f"❌ Error getting dataset info: {str(e)}"
    
    def delete_dataset(self, table_name: str) -> Tuple[bool, str]:
        """
        Delete a dataset
        
        Args:
            table_name: Dataset to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if table exists
            if not self.table_exists(table_name):
                return False, f"❌ Dataset '{table_name}' not found"
            
            # Don't delete special tables
            if table_name == 'financial_data':
                return False, "❌ Cannot delete sample data table"
            
            # Drop table
            self.db._connection.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.db._connection.commit()
            
            return True, f"✅ Dataset '{table_name}' deleted successfully"
        
        except Exception as e:
            return False, f"❌ Error deleting dataset: {str(e)}"
    
    def rename_dataset(self, old_name: str, new_name: str) -> Tuple[bool, str]:
        """
        Rename a dataset
        
        Args:
            old_name: Current dataset name
            new_name: New dataset name
            
        Returns:
            Tuple of (success, message)
        """
        try:
            # Check if old table exists
            if not self.table_exists(old_name):
                return False, f"❌ Dataset '{old_name}' not found"
            
            # Check if new name is available
            if self.table_exists(new_name):
                return False, f"❌ Dataset '{new_name}' already exists"
            
            # Validate new name
            if not self._validate_table_name(new_name):
                return False, "❌ Invalid dataset name. Use letters, numbers, underscores only"
            
            # Rename table
            self.db._connection.execute(f"ALTER TABLE {old_name} RENAME TO {new_name}")
            self.db._connection.commit()
            
            return True, f"✅ Dataset renamed from '{old_name}' to '{new_name}'"
        
        except Exception as e:
            return False, f"❌ Error renaming dataset: {str(e)}"
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists
        
        Args:
            table_name: Table name to check
            
        Returns:
            True if exists, False otherwise
        """
        try:
            result = self.db.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
            )
            return len(result) > 0 if result else False
        except:
            return False
    
    def _validate_table_name(self, name: str) -> bool:
        """
        Validate table name format
        
        Args:
            name: Table name to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not name or len(name) == 0:
            return False
        
        # Allow only alphanumeric and underscores
        import re
        return bool(re.match(r'^[a-zA-Z0-9_]+$', name))
    
    def get_dataset_summary(self, table_name: str) -> Dict[str, Any]:
        """
        Get comprehensive summary of a dataset
        
        Args:
            table_name: Dataset name
            
        Returns:
            Summary dictionary
        """
        try:
            import pandas as pd
            
            # Get data
            results = self.db.execute(f"SELECT * FROM {table_name}")
            if not results:
                return {'error': 'No data found'}
            
            # Get columns
            cursor_info = self.db._connection.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor_info.fetchall()]
            
            # Create DataFrame
            df = pd.DataFrame(results, columns=columns)
            
            summary = {
                'name': table_name,
                'rows': len(df),
                'columns': len(df.columns),
                'memory_usage': df.memory_usage(deep=True).sum() / 1024,  # KB
                'numeric_cols': len(df.select_dtypes(include=['number']).columns),
                'text_cols': len(df.select_dtypes(exclude=['number']).columns),
                'missing_values': int(df.isnull().sum().sum()),
                'duplicate_rows': len(df[df.duplicated()])
            }
            
            return summary
        
        except Exception as e:
            return {'error': str(e)}
