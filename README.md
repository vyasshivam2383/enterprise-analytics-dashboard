# 📊 Enterprise Analytics Dashboard

**Production-grade analytics platform with OOPS architecture, SQL storage, AI-powered insights, and advanced data management.**

## Overview

This is a professional-quality analytics dashboard built with Streamlit, SQLite, and Python. It's designed for enterprise-level data analysis with zero external API dependencies and deployment-ready architecture.

### Key Features

✅ **Complete OOPS Architecture** (Abstraction, Inheritance, Polymorphism, Encapsulation, Composition)
✅ **SQL-Based Storage** (SQLite with dynamic schema)
✅ **File Upload** (Any CSV format, auto-processing)
✅ **Real-Time Analytics** (Revenue, Cost, Profit, Trends)
✅ **AI-Powered Q&A** (Natural language questions with confidence scoring)
✅ **Advanced Filtering** (Dynamic WHERE clauses)
✅ **Grouping & Aggregation** (GROUP BY on any column)
✅ **Data Profiling** (Statistical analysis per column)
✅ **Multiple Visualizations** (Line, Bar, Pie, Scatter, Heatmap)
✅ **Multi-Format Export** (CSV, Excel, JSON)
✅ **Dataset Management** (Switch, rename, delete datasets)
✅ **Performance Optimization** (Computation caching, query optimization)
✅ **Enterprise UI** (Dark theme, professional styling)
✅ **Error Handling** (Robust validation and user-friendly messages)

---

## Architecture

### Project Structure

```
enterprise_analytics_dashboard/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── analytics.db                    # SQLite database
├── analytics/
│   ├── __init__.py
│   ├── base.py                     # Abstract base class (OOPS)
│   ├── revenue.py                  # Revenue analytics (inheritance)
│   ├── trends.py                   # Trend analytics (inheritance)
│   └── profiling.py                # Data profiling module
├── database/
│   ├── __init__.py
│   └── db.py                       # Database layer (encapsulation)
├── services/
│   ├── __init__.py
│   └── analytics_service.py        # Service layer (composition)
└── utils/
    ├── __init__.py
    ├── csv_loader.py               # CSV loading utilities
    ├── ai_insights.py              # AI Q&A engine
    ├── error_handler.py            # Error handling & validation
    ├── filter_engine.py            # Advanced filtering
    ├── aggregation_engine.py       # GROUP BY & aggregation
    ├── chart_generator.py          # Visualization generation
    ├── export_manager.py           # Multi-format export
    ├── dataset_manager.py          # Dataset management
    └── performance.py              # Caching & optimization
```

### OOPS Principles

1. **Abstraction** - `BaseAnalytics` with abstract `compute()`
2. **Inheritance** - `RevenueAnalytics`, `TrendAnalytics` extend base
3. **Polymorphism** - Service calls `compute()` on any analytics class
4. **Encapsulation** - Private `_connection` in Database class
5. **Composition** - Service uses Database and Analytics objects

---

## Features in Detail

### A. Core Stability
- Robust error handling for empty files, non-numeric data, missing columns
- User-friendly error messages
- Input validation for all operations
- Graceful error recovery

### B. Data Profiling
- Column-wise statistical analysis
- Numeric: mean, median, min, max, std, quartiles
- Text: unique count, most frequent value
- Missing value detection

### C. Advanced Filtering
- Syntax: `column > value`, `column between X and Y`
- Supports: >, <, >=, <=, ==, !=
- Works with numeric and text columns

### D. Grouping & Aggregation
- GROUP BY on any column
- Aggregations: sum, mean, min, max, count, median, std
- Multi-column aggregation

### E. Visualizations
- Line charts, bar charts, pie charts
- Scatter plots, histograms, box plots
- Correlation heatmaps
- Professional dark theme styling

### F. Export System
- CSV export (respects filters & grouping)
- Excel export (.xlsx with multiple sheets)
- JSON export (records or table format)
- Timestamped filenames

### G. AI Q&A Engine
- Natural language question parsing
- Question types: max, min, sum, average, count, trend, ratio, comparison
- Context-aware answers with statistics
- Confidence scoring
- Safe responses: "Data not available" when unsure

### H. Performance Optimization
- Computation caching with TTL
- Query optimization helpers
- Avoids unnecessary data reloading

### I. Dataset Management
- List, switch, delete, rename datasets
- Get dataset info (rows, columns, memory)
- Dataset isolation

### J. Code Quality
- Comprehensive docstrings
- Type hints on all methods
- Clean separation of concerns
- Consistent naming conventions

### K. UI/UX Polish
- Dark professional theme (#0a0e27 + cyan #00D9FF)
- Responsive layout
- Clear KPI cards
- Intuitive navigation

### L. Documentation
- Comprehensive README
- Inline docstrings in all modules
- Architecture explanation
- Feature descriptions

---

## Installation & Setup

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Open: `http://localhost:8501`

---

## Usage Guide

### Loading Data
- **Sample:** Click "Load Sample Data"
- **Custom:** Upload any CSV file

### Analytics Tab
- View KPI cards
- See trend charts
- Summary statistics

### Data Tab
- Browse dataset
- Download as CSV

### AI Assistant Tab
- Ask natural English questions
- Examples: "What's the highest revenue?" | "Is profit increasing?"

---

## Database

Default table: `financial_data` with columns:
- id (INTEGER PRIMARY KEY)
- date (TEXT)
- revenue (REAL)
- cost (REAL)
- profit (REAL)

Custom uploads auto-detect and create appropriate schemas.

---

## Limitations & Future

### Current
- Single SQLite database
- No user authentication
- Pattern-matching AI (not LLM)

### Future
- Real-time streaming
- ML forecasting
- User authentication
- Multi-database support
- Scheduled reports
- API endpoints

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Updated:** December 23, 2025
│   ├── __init__.py
│   └── db.py                   # SQLite wrapper (ENCAPSULATION)
│
├── services/                   # Business logic layer
│   ├── __init__.py
│   └── analytics_service.py    # Service layer (COMPOSITION)
│
├── utils/                      # Helper utilities
│   ├── __init__.py
│   └── csv_loader.py           # CSV validation & loading
│
├── data/
│   └── financial_data.csv      # Sample financial dataset
│
└── .streamlit/
    └── config.toml             # Dark theme configuration
```

## 🎓 OOPS Concepts Demonstrated

### 1. **Abstraction** - `analytics/base.py`
```python
class BaseAnalytics(ABC):
    @abstractmethod
    def compute(self) -> Dict[str, Any]:
        pass
```
- Abstract base class enforces contract for all analytics modules
- Hides implementation details, exposes only interface

### 2. **Inheritance** - `analytics/revenue.py` and `analytics/trends.py`
```python
class RevenueAnalytics(BaseAnalytics):
    def compute(self) -> Dict[str, Any]:
        # Concrete implementation
```
- Both revenue and trend analytics inherit from BaseAnalytics
- Override abstract `compute()` method with specific logic

### 3. **Encapsulation** - `database/db.py`
```python
class Database:
    def __init__(self, db_path: str):
        self._connection = None  # Private attribute
    
    def _initialize(self):        # Private method
        # Implementation
```
- Database connection is private (`_connection`)
- Controlled access through public methods (`execute`, `insert_data`)
- Implementation details hidden from users

### 4. **Polymorphism** - `services/analytics_service.py`
```python
def _compute_analytics(self, analytics: BaseAnalytics) -> Dict[str, Any]:
    return analytics.compute()  # Works with any subclass
```
- Service calls `compute()` without knowing concrete type
- Works identically with `RevenueAnalytics` or `TrendAnalytics`

### 5. **Composition** - `services/analytics_service.py`
```python
class AnalyticsService:
    def __init__(self, db_path: str):
        self._db = Database(db_path)
        self._revenue_analytics = RevenueAnalytics(self._db)
        self._trend_analytics = TrendAnalytics(self._db)
```
- Service **composes** Database and Analytics instances
- Uses "has-a" relationship instead of inheritance
- Flexible and maintainable design

## 📊 SQL Features

The project demonstrates SQL analytics with:
- **Table Creation** - Auto-create `financial_data` table
- **INSERT** - Bulk insert from CSV
- **SELECT with Aggregation** - SUM(), AVG()
- **GROUP BY** - Daily aggregations
- **ORDER BY** - Sorted results

Example queries in analytics modules:
```sql
-- Revenue aggregation
SELECT SUM(revenue), AVG(revenue) FROM financial_data

-- Daily trends
SELECT date, SUM(revenue), SUM(cost), SUM(profit)
FROM financial_data
GROUP BY date
ORDER BY date
```

## 🎨 Streamlit Features

The UI showcases:
- **Dark Professional Theme** - Custom `.streamlit/config.toml`
- **KPI Cards** - Total Revenue, Cost, Profit
- **Line Charts** - Revenue & Profit trends
- **Bar Charts** - Cost distribution
- **Metrics** - Profit margin calculation
- **Data Tables** - Daily financial data
- **Sidebar Controls** - Refresh data button
- **Responsive Layout** - Wide layout with columns

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Local Installation

1. **Clone or navigate to project:**
```bash
cd enterprise_analytics_dashboard
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. **Access the dashboard:**
   - Opens automatically at `http://localhost:8501`

### Dataset

The project includes `data/financial_data.csv` with:
- Date (YYYY-MM-DD format)
- Revenue
- Cost
- Profit

Data is automatically loaded into SQLite on first run.

## 📦 Dependencies

- **streamlit** - Web UI framework
- **pandas** - Data manipulation
- **Python stdlib** - sqlite3, abc, csv

No external database or API required.

## 🌐 Deployment on Streamlit Community Cloud

### Steps to Deploy:

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Connect to Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Features:**
   - Free hosting
   - Auto-redeploy on git push
   - SQLite works natively
   - No environment variables needed

## 📈 Code Quality

- **Type Hints** - All functions annotated
- **Docstrings** - Module and function level
- **Error Handling** - Try-catch with logging
- **Separation of Concerns** - Clear layer boundaries
- **DRY Principle** - No code duplication
- **SOLID Principles** - Single responsibility, Open/closed

## 🔧 Project Structure Benefits

| Layer | Purpose | Example |
|-------|---------|---------|
| **Presentation** | UI & user interaction | `app.py` |
| **Services** | Business logic | `analytics_service.py` |
| **Analytics** | Domain computation | `revenue.py`, `trends.py` |
| **Database** | Data persistence | `db.py` |
| **Utils** | Helper functions | `csv_loader.py` |

## 🎯 Key Features

✅ **No Over-Engineering** - Clean, simple, focused  
✅ **No Authentication** - Immediate usability  
✅ **No External Dependencies** - SQLite only  
✅ **Linear Flow** - Clear data pipeline  
✅ **Production-Ready** - Proper error handling  
✅ **OOPS Showcase** - All principles demonstrated  
✅ **Free Deployment** - Streamlit Community Cloud compatible  

## 📝 License

This project is provided as an enterprise showcase template.

## 🤝 Contributing

This is a showcase project. Feel free to use as a template for your own analytics dashboards.

---

**Built with ❤️ | Enterprise-Grade Python | Clean Architecture**
