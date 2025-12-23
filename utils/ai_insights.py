"""
AI-powered intelligent question answering for data insights.
Handles natural English questions with flexible pattern matching.
Features: Multi-step queries, ratio analysis, confidence scoring
"""
import pandas as pd
import re
from typing import Dict, Any, List, Optional, Tuple
from database.db import Database


class DataInsightAI:
    """
    Advanced AI question-answering engine for data analysis.
    Understands natural English questions and provides accurate insights.
    Supports: Max/Min/Sum/Avg/Count/Trend/Comparison/Ratios/Multi-step queries
    """

    def __init__(self, db: Database, table_name: str):
        """
        Initialize AI with database connection.
        
        Args:
            db: Database instance
            table_name: Table name to analyze
        """
        self.db = db
        self.table_name = table_name
        self.data = None
        self.columns = []
        self.numeric_cols = []
        self.confidence = 1.0  # Confidence score (0-1)
        self._load_data()

    def _load_data(self):
        """Load and analyze data from table."""
        try:
            query = f"SELECT * FROM {self.table_name}"
            results = self.db.execute(query)
            
            if not results:
                self.data = pd.DataFrame()
                return
            
            # Get column names
            cursor_info = self.db._connection.execute(f"PRAGMA table_info({self.table_name})")
            self.columns = [row[1] for row in cursor_info.fetchall()]
            
            # Create DataFrame
            self.data = pd.DataFrame(results, columns=self.columns)
            
            # Identify numeric columns
            self.numeric_cols = self.data.select_dtypes(include=['number']).columns.tolist()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame()

    def answer_question(self, question: str) -> str:
        """
        Answer user question with intelligent natural language processing.
        Supports: max/min/sum/avg/count/trend/comparison/ratios
        
        Args:
            question: User question in natural English
            
        Returns:
            Formatted answer with insights
        """
        if self.data is None or self.data.empty:
            return "❌ No data available. Please upload a CSV file first."
        
        # Check for ratio questions first
        if self._is_ratio_question(question):
            self._set_confidence(0.9)
            return self._answer_ratio_question(question)
        
        # Check for multi-column comparisons
        if self._is_multi_column_question(question):
            self._set_confidence(0.85)
            return self._answer_multi_column_question(question)

        question_lower = question.lower().strip()
        
        # Extract what metric they're asking about
        metric_col = self._find_relevant_column(question_lower)
        
        if not metric_col:
            return self._generate_generic_response(question_lower)
        
        # Determine question type
        if self._is_max_question(question_lower):
            return self._answer_max(metric_col, question)
        
        elif self._is_min_question(question_lower):
            return self._answer_min(metric_col, question)
        
        elif self._is_sum_question(question_lower):
            return self._answer_sum(metric_col, question)
        
        elif self._is_avg_question(question_lower):
            return self._answer_avg(metric_col, question)
        
        elif self._is_count_question(question_lower):
            return self._answer_count(metric_col, question)
        
        elif self._is_trend_question(question_lower):
            return self._answer_trend(metric_col, question)
        
        elif self._is_comparison_question(question_lower):
            return self._answer_comparison(metric_col, question_lower)
        
        else:
            return self._answer_general(metric_col, question)

    def _find_relevant_column(self, question: str) -> Optional[str]:
        """Find which column the question is about with smart matching."""
        # Build synonyms map for common column names
        synonyms = {
            'revenue': ['revenue', 'revenues', 'sales', 'rev', 'income', 'earnings'],
            'cost': ['cost', 'costs', 'expense', 'expenses', 'spending'],
            'profit': ['profit', 'profits', 'earnings', 'net', 'gain'],
            'price': ['price', 'prices', 'amount', 'value', 'cost'],
            'quantity': ['quantity', 'qty', 'count', 'number', 'volume'],
            'date': ['date', 'time', 'when', 'day'],
        }
        
        # Remove common filler words
        question_words = question.lower().replace('?', '').replace(',', '').split()
        question_words = [w for w in question_words if len(w) > 2]
        
        best_match = None
        best_score = 0
        
        # Check each numeric column for keyword matches
        for col in self.numeric_cols:
            col_lower = col.lower()
            score = 0
            
            # Direct match with column name
            if col_lower in question:
                score += 100
            
            # Check synonyms
            for key, syns in synonyms.items():
                if col_lower == key or col_lower in syns:
                    for word in question_words:
                        if word in syns or word == key:
                            score += 50
            
            # Match any word in question
            for word in question_words:
                if word in col_lower or col_lower in word:
                    if len(word) > 3:  # Avoid single letter matches
                        score += 10
            
            if score > best_score:
                best_score = score
                best_match = col
        
        # Fallback: check all columns including text
        if best_score == 0:
            for col in self.columns:
                col_lower = col.lower()
                for word in question_words:
                    if word in col_lower or col_lower in word:
                        if len(word) > 3:
                            return col
        
        # Return best match or first numeric column
        if best_match:
            return best_match
        elif self.numeric_cols:
            return self.numeric_cols[0]
        
        return None

    def _is_max_question(self, q: str) -> bool:
        """Check if question asks for maximum."""
        return any(word in q for word in ["max", "highest", "largest", "biggest", "most", "greatest", "peak"])

    def _is_min_question(self, q: str) -> bool:
        """Check if question asks for minimum."""
        return any(word in q for word in ["min", "lowest", "smallest", "least", "bottom"])

    def _is_sum_question(self, q: str) -> bool:
        """Check if question asks for total."""
        return any(word in q for word in ["total", "sum", "altogether", "combined", "all together"])

    def _is_avg_question(self, q: str) -> bool:
        """Check if question asks for average."""
        return any(word in q for word in ["average", "avg", "mean", "typical", "on average"])

    def _is_count_question(self, q: str) -> bool:
        """Check if question asks for count."""
        return any(word in q for word in ["how many", "count", "number of", "total records", "total rows"])

    def _is_trend_question(self, q: str) -> bool:
        """Check if question asks about trends."""
        return any(word in q for word in ["trend", "increasing", "decreasing", "growing", "rising", "falling", "change", "pattern"])

    def _is_comparison_question(self, q: str) -> bool:
        """Check if question asks to compare."""
        return " vs " in q or " compared to " in q or " versus " in q

    def _answer_max(self, col: str, question: str) -> str:
        """Answer maximum value question."""
        try:
            if col not in self.numeric_cols:
                return f"❌ Cannot find maximum of non-numeric column '{col}'"
            
            max_val = self.data[col].max()
            avg_val = self.data[col].mean()
            
            return f"""
📈 **Highest {col.replace('_', ' ').title()}**

• **Maximum**: {max_val:,.2f}
• **Average**: {avg_val:,.2f}
• **Distance from average**: {(max_val - avg_val):,.2f} ({((max_val/avg_val - 1) * 100):+.1f}%)
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_min(self, col: str, question: str) -> str:
        """Answer minimum value question."""
        try:
            if col not in self.numeric_cols:
                return f"❌ Cannot find minimum of non-numeric column '{col}'"
            
            min_val = self.data[col].min()
            avg_val = self.data[col].mean()
            
            return f"""
📉 **Lowest {col.replace('_', ' ').title()}**

• **Minimum**: {min_val:,.2f}
• **Average**: {avg_val:,.2f}
• **Distance from average**: {(avg_val - min_val):,.2f} ({((1 - min_val/avg_val) * 100):+.1f}%)
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_sum(self, col: str, question: str) -> str:
        """Answer total/sum question."""
        try:
            if col not in self.numeric_cols:
                return f"❌ Cannot sum non-numeric column '{col}'"
            
            total = self.data[col].sum()
            count = len(self.data)
            avg = self.data[col].mean()
            
            return f"""
📊 **Total {col.replace('_', ' ').title()}**

• **Sum**: {total:,.2f}
• **Records**: {count}
• **Average per record**: {avg:,.2f}
• **Percentage breakdown**: Each record averages {(avg/total*100 if total != 0 else 0):.2f}% of total
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_avg(self, col: str, question: str) -> str:
        """Answer average question."""
        try:
            if col not in self.numeric_cols:
                return f"❌ Cannot calculate average of non-numeric column '{col}'"
            
            avg = self.data[col].mean()
            median = self.data[col].median()
            std = self.data[col].std()
            
            return f"""
📊 **Average {col.replace('_', ' ').title()}**

• **Mean**: {avg:,.2f}
• **Median**: {median:,.2f}
• **Std Dev**: {std:,.2f}
• **Variation**: ±{(std/avg*100):.1f}% from mean
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_count(self, col: str, question: str) -> str:
        """Answer count question."""
        try:
            count = len(self.data)
            non_null = self.data[col].count() if col in self.columns else count
            
            return f"""
📊 **Data Count**

• **Total records**: {count}
• **Non-null values in {col}**: {non_null}
• **Missing values**: {count - non_null}
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_trend(self, col: str, question: str) -> str:
        """Answer trend question."""
        try:
            if col not in self.numeric_cols or len(self.data) < 2:
                return f"❌ Cannot analyze trend for column '{col}'"
            
            first_val = self.data[col].iloc[0]
            last_val = self.data[col].iloc[-1]
            change = last_val - first_val
            pct_change = (change / first_val * 100) if first_val != 0 else 0
            
            trend = "📈 **INCREASING**" if change > 0 else "📉 **DECREASING**" if change < 0 else "➡️ **STABLE**"
            
            return f"""
{trend}

• **Start**: {first_val:,.2f}
• **End**: {last_val:,.2f}
• **Change**: {change:,.2f} ({pct_change:+.1f}%)
• **Avg daily change**: {(change / len(self.data)):,.2f}
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_comparison(self, col: str, question: str) -> str:
        """Answer comparison question."""
        try:
            if len(self.numeric_cols) < 2:
                return "❌ Need at least 2 numeric columns to compare"
            
            # Find which columns to compare
            cols_to_compare = [c for c in self.numeric_cols if c in question.lower()]
            if len(cols_to_compare) < 2:
                cols_to_compare = self.numeric_cols[:2]
            
            results = f"📊 **Comparison: {cols_to_compare[0]} vs {cols_to_compare[1]}**\n\n"
            
            for col in cols_to_compare:
                results += f"**{col.replace('_', ' ').title()}**:\n"
                results += f"  • Total: {self.data[col].sum():,.2f}\n"
                results += f"  • Average: {self.data[col].mean():,.2f}\n"
                results += f"  • Max: {self.data[col].max():,.2f}\n\n"
            
            return results
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _answer_general(self, col: str, question: str) -> str:
        """Answer general question about a column."""
        try:
            if col not in self.numeric_cols:
                return f"📊 Showing data for column: **{col.replace('_', ' ').title()}**"
            
            return f"""
📊 **Overview: {col.replace('_', ' ').title()}**

• **Sum**: {self.data[col].sum():,.2f}
• **Average**: {self.data[col].mean():,.2f}
• **Maximum**: {self.data[col].max():,.2f}
• **Minimum**: {self.data[col].min():,.2f}
• **Records**: {len(self.data)}
"""
        except Exception as e:
            return f"❌ Error: {str(e)}"

    def _is_ratio_question(self, q: str) -> bool:
        """Detect ratio/percentage questions"""
        ratio_words = ['ratio', 'percentage', 'percent', 'margin', 'divided', 'per', 'vs', 'versus']
        return any(word in q.lower() for word in ratio_words)
    
    def _answer_ratio_question(self, question: str) -> str:
        """Answer ratio-based questions like profit margin, revenue to cost ratio"""
        try:
            q_lower = question.lower()
            
            # Profit margin: profit / revenue
            if 'profit margin' in q_lower or ('margin' in q_lower and 'profit' in q_lower):
                if 'profit' in self.numeric_cols and 'revenue' in self.numeric_cols:
                    profit = self.data['profit'].sum()
                    revenue = self.data['revenue'].sum()
                    if revenue != 0:
                        margin = (profit / revenue) * 100
                        return f"""
💰 **Profit Margin Analysis**

• **Margin**: {margin:.2f}%
• **Total Profit**: ${profit:,.2f}
• **Total Revenue**: ${revenue:,.2f}
• **Interpretation**: For every $100 in revenue, ${margin:.2f} is profit
                        """
            
            # Revenue to Cost ratio
            if 'revenue' in q_lower and 'cost' in q_lower and ('ratio' in q_lower or 'vs' in q_lower):
                if 'revenue' in self.numeric_cols and 'cost' in self.numeric_cols:
                    revenue = self.data['revenue'].sum()
                    cost = self.data['cost'].sum()
                    if cost != 0:
                        ratio = revenue / cost
                        return f"""
📊 **Revenue to Cost Ratio**

• **Ratio**: {ratio:.2f}:1
• **Total Revenue**: ${revenue:,.2f}
• **Total Cost**: ${cost:,.2f}
• **Meaning**: Revenue is {ratio:.2f}x the cost
                        """
            
            return "❌ Data not available for requested ratio"
        
        except Exception as e:
            return f"❌ Error calculating ratio: {str(e)}"
    
    def _is_multi_column_question(self, q: str) -> bool:
        """Detect multi-column comparison questions"""
        return ' and ' in q.lower() or ' vs ' in q.lower() or 'compare' in q.lower()
    
    def _answer_multi_column_question(self, question: str) -> str:
        """Answer questions comparing multiple columns"""
        try:
            q_lower = question.lower()
            
            # Extract columns mentioned
            mentioned_cols = []
            for col in self.numeric_cols:
                if col.lower() in q_lower or col.lower().replace('_', ' ') in q_lower:
                    mentioned_cols.append(col)
            
            if len(mentioned_cols) < 2:
                return "❌ Please mention at least two columns to compare"
            
            response = f"📊 **Comparison Analysis**\n\n"
            
            for col in mentioned_cols[:3]:  # Limit to 3 columns
                values = self.data[col].dropna()
                response += f"""**{col.replace('_', ' ').title()}**
• Sum: ${values.sum():,.2f}
• Average: ${values.mean():,.2f}
• Min: ${values.min():,.2f}
• Max: ${values.max():,.2f}

"""
            
            return response
        
        except Exception as e:
            return f"❌ Error in comparison: {str(e)}"
    
    def get_confidence_score(self) -> float:
        """
        Get confidence score for last answer (0-1)
        
        Returns:
            Confidence value
        """
        return self.confidence
    
    def _set_confidence(self, score: float):
        """Set confidence score"""
        self.confidence = max(0.0, min(1.0, score))

    def _generate_generic_response(self, question: str) -> str:
        """Generate response when column not identified."""
        if self.numeric_cols:
            return f"""
📊 **Available numeric columns to ask about:**

{chr(10).join([f'• {col.replace("_", " ").title()}' for col in self.numeric_cols])}

Ask something like: "What's the highest {self.numeric_cols[0]}?" or "Show me the average {self.numeric_cols[0]}"
"""
        else:
            return "❌ No numeric data found in this dataset"
