"""
Utilities for CSV data loading and validation.
"""
import csv
from pathlib import Path
from typing import List, Tuple
from datetime import datetime


class CSVLoader:
    """Handle CSV loading with validation."""

    @staticmethod
    def validate_row(row: dict) -> bool:
        """
        Validate a CSV row has required fields and correct types.
        
        Args:
            row: Dictionary row from CSV
            
        Returns:
            True if valid, False otherwise
        """
        required_fields = {"date", "revenue", "cost", "profit"}
        
        if not all(field in row for field in required_fields):
            return False

        try:
            datetime.strptime(row["date"], "%Y-%m-%d")
            float(row["revenue"])
            float(row["cost"])
            float(row["profit"])
            return True
        except (ValueError, KeyError):
            return False

    @staticmethod
    def load_csv(file_path: str) -> List[Tuple]:
        """
        Load and validate CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of tuples (date, revenue, cost, profit)
        """
        data = []
        
        if not Path(file_path).exists():
            print(f"File not found: {file_path}")
            return data

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    if CSVLoader.validate_row(row):
                        data.append((
                            row["date"],
                            float(row["revenue"]),
                            float(row["cost"]),
                            float(row["profit"]),
                        ))
                    else:
                        print(f"Invalid row skipped: {row}")
            
            print(f"Successfully loaded {len(data)} records from {file_path}")
        except Exception as e:
            print(f"Error loading CSV: {e}")

        return data
