"""
Base abstract class for analytics modules.
Demonstrates abstraction and interface definition.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAnalytics(ABC):
    """
    Abstract base class for all analytics computations.
    Enforces contract that all analytics modules must implement compute().
    """

    def __init__(self, db_connection):
        """
        Initialize analytics with database connection.
        
        Args:
            db_connection: Database instance for data access
        """
        self.db = db_connection

    @abstractmethod
    def compute(self) -> Dict[str, Any]:
        """
        Compute analytics metrics.
        
        Must be implemented by subclasses.
        Returns dictionary with computed metrics.
        """
        pass

    def _validate_data(self) -> bool:
        """Helper method for data validation."""
        try:
            result = self.db.execute("SELECT COUNT(*) FROM financial_data")
            count = result[0][0] if result else 0
            return count > 0
        except Exception:
            return False
