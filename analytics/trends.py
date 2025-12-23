"""
Trend analytics module.
Demonstrates inheritance and polymorphism.
"""
from typing import Dict, Any, List
from analytics.base import BaseAnalytics


class TrendAnalytics(BaseAnalytics):
    """
    Trend analytics computation.
    Inherits from BaseAnalytics and implements compute() method.
    """

    def compute(self) -> Dict[str, Any]:
        """
        Compute trend metrics including profit, cost trends, and aggregates.
        
        Returns:
            Dictionary with trend data
        """
        if not self._validate_data():
            return {
                "total_profit": 0,
                "total_cost": 0,
                "daily_metrics": [],
                "profit_margin": 0,
            }

        # Total metrics
        total_result = self.db.execute(
            "SELECT SUM(profit), SUM(cost) FROM financial_data"
        )
        total_profit = total_result[0][0] if total_result and total_result[0][0] else 0
        total_cost = total_result[0][1] if total_result and total_result[0][1] else 0
        total_revenue = self._get_total_revenue()

        # Daily metrics for trending
        daily_result = self.db.execute(
            """
            SELECT date, SUM(revenue) as revenue, SUM(cost) as cost, SUM(profit) as profit
            FROM financial_data
            GROUP BY date
            ORDER BY date
            """
        )
        daily_metrics = [
            {
                "date": row[0],
                "revenue": round(row[1], 2),
                "cost": round(row[2], 2),
                "profit": round(row[3], 2),
            }
            for row in daily_result
        ] if daily_result else []

        # Calculate profit margin
        profit_margin = (
            round((total_profit / total_revenue * 100), 2)
            if total_revenue > 0
            else 0
        )

        return {
            "total_profit": round(total_profit, 2),
            "total_cost": round(total_cost, 2),
            "daily_metrics": daily_metrics,
            "profit_margin": profit_margin,
        }

    def _get_total_revenue(self) -> float:
        """Helper to get total revenue."""
        result = self.db.execute("SELECT SUM(revenue) FROM financial_data")
        return result[0][0] if result and result[0][0] else 0


