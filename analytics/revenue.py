"""
Revenue analytics module.
Demonstrates inheritance and polymorphism.
"""
from typing import Dict, Any
from analytics.base import BaseAnalytics


class RevenueAnalytics(BaseAnalytics):
    """
    Revenue analytics computation.
    Inherits from BaseAnalytics and implements compute() method.
    """

    def compute(self) -> Dict[str, Any]:
        """
        Compute revenue metrics including total, average, and trend.
        
        Returns:
            Dictionary with revenue metrics
        """
        if not self._validate_data():
            return {"total_revenue": 0, "avg_revenue": 0, "daily_revenue": []}

        # Total and average revenue
        total_result = self.db.execute(
            "SELECT SUM(revenue) FROM financial_data"
        )
        total_revenue = total_result[0][0] if total_result and total_result[0][0] else 0

        avg_result = self.db.execute(
            "SELECT AVG(revenue) FROM financial_data"
        )
        avg_revenue = avg_result[0][0] if avg_result and avg_result[0][0] else 0

        # Daily revenue data for trending
        daily_result = self.db.execute(
            """
            SELECT date, SUM(revenue) as daily_revenue 
            FROM financial_data 
            GROUP BY date 
            ORDER BY date
            """
        )
        daily_revenue = [
            {"date": row[0], "revenue": row[1]} for row in daily_result
        ] if daily_result else []

        return {
            "total_revenue": round(total_revenue, 2),
            "avg_revenue": round(avg_revenue, 2),
            "daily_revenue": daily_revenue,
        }
