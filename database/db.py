"""
Database module with encapsulated SQLite access.
Demonstrates encapsulation principle.
"""
import sqlite3
from pathlib import Path
from typing import List, Tuple, Any, Dict


class Database:
    """
    Encapsulated SQLite database interface.
    Private connection ensures controlled data access.
    """

    def __init__(self, db_path: str = "analytics.db"):
        """
        Initialize database with path.
        
        Args:
            db_path: Path to SQLite database file
        """
        self._db_path = db_path
        self._connection = None
        self._initialize()

    def _initialize(self):
        """Private method to initialize database connection and schema."""
        self._connection = sqlite3.connect(self._db_path)
        self._create_schema()

    def _create_schema(self):
        """Private method to create default database schema."""
        schema = """
        CREATE TABLE IF NOT EXISTS financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            revenue REAL NOT NULL,
            cost REAL NOT NULL,
            profit REAL NOT NULL,
            UNIQUE(date)
        )
        """
        self._connection.execute(schema)
        self._connection.commit()

    def create_table_from_columns(self, table_name: str, columns: Dict[str, str]):
        """
        Create a new table with specified columns.
        
        Args:
            table_name: Name of the table
            columns: Dictionary of column_name: data_type
        """
        try:
            col_definitions = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {col_definitions})"
            self._connection.execute(query)
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def execute(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """
        Execute SQL query (read-only intended).
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of result tuples
        """
        try:
            cursor = self._connection.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def insert_data(self, query: str, params: Tuple = ()):
        """
        Execute insert/update/delete query.
        
        Args:
            query: SQL query string
            params: Query parameters
        """
        try:
            self._connection.execute(query, params)
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def insert_many(self, query: str, data: List[Tuple]):
        """
        Insert multiple rows.
        
        Args:
            query: SQL query string
            data: List of tuples containing row data
        """
        try:
            self._connection.executemany(query, data)
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def clear_data(self, table_name: str = "financial_data"):
        """
        Clear all data from specified table.
        
        Args:
            table_name: Table to clear
        """
        try:
            self._connection.execute(f"DELETE FROM {table_name}")
            self._connection.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def table_exists(self, table_name: str) -> bool:
        """
        Check if table exists.
        
        Args:
            table_name: Table name to check
            
        Returns:
            True if table exists
        """
        try:
            result = self._connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            return bool(result.fetchone())
        except sqlite3.Error:
            return False

    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()

    def __del__(self):
        """Cleanup on object destruction."""
        try:
            self.close()
        except:
            pass
