"""
Analytics service with composition pattern.
Uses Database and Analytics classes together.
"""
from typing import Dict, Any, List
from database.db import Database
from analytics.base import BaseAnalytics
from analytics.revenue import RevenueAnalytics
from analytics.trends import TrendAnalytics
from utils.csv_loader import CSVLoader


class AnalyticsService:
    """
    Service layer using composition pattern.
    Composes Database and Analytics instances.
    Demonstrates polymorphism through analytics interface.
    """

    def __init__(self, db = None):
        """
        Initialize service with database.
        
        Args:
            db: Database instance or path to SQLite database (default: "analytics.db")
        """
        if isinstance(db, Database):
            self._db = db
        else:
            db_path = db if isinstance(db, str) else "analytics.db"
            self._db = Database(db_path)
        
        self._revenue_analytics = RevenueAnalytics(self._db)
        self._trend_analytics = TrendAnalytics(self._db)

    @property
    def db(self):
        """Access the database instance."""
        return self._db

    def load_data(self, csv_path: str = None) -> bool:
        """
        Load financial data from CSV file.
        
        Args:
            csv_path: Path to CSV file (default: data/financial_data.csv)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if csv_path is None:
                csv_path = "data/financial_data.csv"
            
            data = CSVLoader.load_csv(csv_path)
            
            if not data:
                print("No valid data to load")
                return False

            self._db.clear_data()
            
            query = """
            INSERT INTO financial_data (date, revenue, cost, profit)
            VALUES (?, ?, ?, ?)
            """
            self._db.insert_many(query, data)
            print(f"Successfully loaded {len(data)} records into database")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

    def get_all_analytics(self) -> Dict[str, Any]:
        """
        Get all analytics computations.
        Demonstrates polymorphism - calls compute() on different subclasses.
        
        Returns:
            Dictionary with all analytics results
        """
        return {
            "revenue": self._compute_analytics(self._revenue_analytics),
            "trends": self._compute_analytics(self._trend_analytics),
        }

    def _compute_analytics(self, analytics: BaseAnalytics) -> Dict[str, Any]:
        """
        Helper to compute analytics polymorphically.
        Works with any BaseAnalytics subclass.
        
        Args:
            analytics: Any BaseAnalytics subclass instance
            
        Returns:
            Computed metrics dictionary
        """
        try:
            return analytics.compute()
        except Exception as e:
            print(f"Error computing analytics: {e}")
            return {}

    def get_daily_data(self) -> List[Dict[str, Any]]:
        """
        Get daily aggregated financial data.
        
        Returns:
            List of daily records
        """
        query = """
        SELECT date, revenue, cost, profit
        FROM financial_data
        ORDER BY date
        """
        results = self._db.execute(query)
        
        return [
            {
                "date": row[0],
                "revenue": round(row[1], 2),
                "cost": round(row[2], 2),
                "profit": round(row[3], 2),
            }
            for row in results
        ] if results else []

    def close(self):
        """Close database connection."""
        self._db.close()
