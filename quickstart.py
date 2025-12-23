#!/usr/bin/env python3
"""
Quick Start Script for Enterprise Analytics Dashboard
Demonstrates all OOPS concepts and functionality
"""

from services.analytics_service import AnalyticsService
import json


def print_section(title):
    """Print formatted section title."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    """Run quick start demonstration."""
    
    print_section("ENTERPRISE ANALYTICS DASHBOARD - QUICK START")
    
    # 1. Initialize Service (COMPOSITION)
    print("\n[1] Initializing Analytics Service (COMPOSITION Pattern)")
    print("    - Service COMPOSES Database and Analytics instances")
    service = AnalyticsService("demo.db")
    print("    [OK] Service initialized with Database instance")
    
    # 2. Load Data
    print("\n[2] Loading Financial Data")
    print("    - CSV file: data/financial_data.csv")
    print("    - CSV loader validates rows during import")
    success = service.load_data("data/financial_data.csv")
    print(f"    [OK] Data loaded successfully: {success}")
    
    # 3. Compute Analytics (POLYMORPHISM)
    print("\n[3] Computing Analytics (POLYMORPHISM Pattern)")
    print("    - Service calls compute() on different subclasses")
    print("    - Works with RevenueAnalytics AND TrendAnalytics")
    print("    - Without knowing concrete type!")
    analytics = service.get_all_analytics()
    print("    [OK] Analytics computed")
    
    # 4. Display Results
    print("\n[4] RESULTS")
    print("\n  REVENUE ANALYTICS (RevenueAnalytics inherits from BaseAnalytics):")
    revenue = analytics.get("revenue", {})
    print(f"    - Total Revenue:    ${revenue.get('total_revenue', 0):,.2f}")
    print(f"    - Average Revenue:  ${revenue.get('avg_revenue', 0):,.2f}")
    print(f"    - Days tracked:     {len(revenue.get('daily_revenue', []))}")
    
    print("\n  TREND ANALYTICS (TrendAnalytics inherits from BaseAnalytics):")
    trends = analytics.get("trends", {})
    print(f"    - Total Profit:     ${trends.get('total_profit', 0):,.2f}")
    print(f"    - Total Cost:       ${trends.get('total_cost', 0):,.2f}")
    print(f"    - Profit Margin:    {trends.get('profit_margin', 0):.1f}%")
    print(f"    - Days tracked:     {len(trends.get('daily_metrics', []))}")
    
    # 5. Show OOPS Principles
    print("\n[5] OOPS PRINCIPLES DEMONSTRATED")
    print("\n  [ABSTRACTION]")
    print("    - BaseAnalytics abstract class defines interface")
    print("    - @abstractmethod compute() forces implementation")
    
    print("\n  [INHERITANCE]")
    print("    - RevenueAnalytics extends BaseAnalytics")
    print("    - TrendAnalytics extends BaseAnalytics")
    
    print("\n  [ENCAPSULATION]")
    print("    - Database._connection is PRIVATE (protected)")
    print("    - Database._initialize() is PRIVATE method")
    print("    - Public interface: execute(), insert_data()")
    
    print("\n  [POLYMORPHISM]")
    print("    - _compute_analytics(analytics: BaseAnalytics)")
    print("    - Works with ANY BaseAnalytics subclass")
    print("    - Extensible for future analytics types")
    
    print("\n  [COMPOSITION]")
    print("    - AnalyticsService COMPOSES Database")
    print("    - AnalyticsService COMPOSES RevenueAnalytics")
    print("    - AnalyticsService COMPOSES TrendAnalytics")
    print("    - Uses 'has-a' relationship, not inheritance")
    
    # 6. Show SQL Features
    print("\n[6] SQL FEATURES USED")
    daily_data = service.get_daily_data()
    if daily_data:
        print(f"    - Table: financial_data with {len(daily_data)} records")
        print("    - SQL: SUM(), AVG() aggregation")
        print("    - SQL: GROUP BY date")
        print("    - SQL: ORDER BY date")
        print("\n    Sample daily record:")
        sample = daily_data[0]
        print(f"      Date: {sample['date']}")
        print(f"      Revenue: ${sample['revenue']:,.2f}")
        print(f"      Cost: ${sample['cost']:,.2f}")
        print(f"      Profit: ${sample['profit']:,.2f}")
    
    # 7. Cleanup
    print("\n[7] Cleanup")
    service.close()
    print("    [OK] Database connection closed")
    
    # 8. Summary
    print_section("SUMMARY")
    print("\n[OK] All OOPS Principles Demonstrated")
    print("[OK] SQL Analytics Working")
    print("[OK] Data Processing Complete")
    print("[OK] Ready for Streamlit UI")
    print("\nRun with: streamlit run app.py")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
