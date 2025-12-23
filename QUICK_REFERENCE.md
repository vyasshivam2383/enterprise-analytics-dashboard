"""
QUICK REFERENCE GUIDE - Enterprise Analytics Dashboard
All new modules and how to use them
"""

# ===========================================================================
# PHASE A: ERROR HANDLING
# ===========================================================================

from utils.error_handler import ErrorHandler, ValidationError

# Validate CSV upload
is_valid, error_msg = ErrorHandler.validate_csv_upload(df)
if not is_valid:
    st.error(error_msg)  # "❌ CSV file is empty..."

# Validate column exists
is_valid, error_msg = ErrorHandler.validate_column_exists(
    "financial_data", "revenue", available_columns
)

# Validate numeric column
is_valid, error_msg = ErrorHandler.validate_numeric_column(df, "revenue")
if error_msg and "warning" in error_msg.lower():
    st.warning(error_msg)
elif error_msg:
    st.error(error_msg)

# Safe numeric operation
result, error = ErrorHandler.safe_numeric_operation(
    data=[100, 200, 300],
    operation='mean'  # sum, mean, min, max, std
)
# result = 200.0, error = ""


# ===========================================================================
# PHASE B: DATA PROFILING
# ===========================================================================

from analytics.profiling import DataProfiler

profiler = DataProfiler()

# Profile entire DataFrame
profiles = profiler.profile_dataframe(df)
# Returns: {'revenue': {...}, 'cost': {...}, 'date': {...}}

# Profile single column
profile = profiler.profile_column(df['revenue'])
# Returns: {'type': 'numeric', 'count': 25, 'mean': 463.00, ...}

# Get summary
summary = profiler.get_summary_stats(df)
# Returns: {'total_rows': 25, 'numeric_columns': 3, 'missing_values': 0, ...}

# Format for UI display
stats_str = profiler.get_column_stats_for_display(df, 'revenue')
# Returns formatted markdown string for st.markdown()
st.markdown(stats_str)


# ===========================================================================
# PHASE C: ADVANCED FILTERING
# ===========================================================================

from utils.filter_engine import FilterParser, FilterEngine

# Parse filter string
is_valid, filter_dict, error = FilterParser.parse_filter("revenue > 500")
# filter_dict = {
#     'column': 'revenue',
#     'operator': 'gt',
#     'operator_symbol': '>',
#     'value': 500.0,
#     'value_type': 'numeric'
# }

# Parse between filter
is_valid, filter_dict, error = FilterParser.parse_between_filter(
    "revenue between 100 and 500"
)

# Apply filter to DataFrame
filtered_df, error = FilterEngine.apply_filter(df, filter_dict)

# Apply multiple filters (AND logic)
filters = [
    {'column': 'revenue', 'operator': 'gt', 'value': 500},
    {'column': 'cost', 'operator': 'lt', 'value': 300}
]
result_df, error = FilterEngine.apply_multiple_filters(df, filters)

# Get SQL WHERE clause
sql = FilterEngine.get_filter_sql(filter_dict)
# Returns: "WHERE revenue > 500"


# ===========================================================================
# PHASE D: GROUPING & AGGREGATION
# ===========================================================================

from utils.aggregation_engine import AggregationEngine

# Group and aggregate
result_df, error = AggregationEngine.group_and_aggregate(
    df=df,
    group_column='date',
    agg_column='revenue',
    agg_function='sum'  # sum, mean, min, max, count, std, median
)

# Multi-column aggregation
result_df, error = AggregationEngine.multi_aggregation(
    df=df,
    group_column='date',
    agg_columns={
        'revenue': ['sum', 'mean'],
        'cost': ['min', 'max']
    }
)

# Get unique values for grouping
unique_dates = AggregationEngine.get_unique_values(df, 'date', limit=100)

# Get available aggregations per column
available = AggregationEngine.validate_aggregations_available(df)
# Returns: {'revenue': ['sum', 'mean', 'min', ...], 'date': ['count']}

# Get SQL query
sql = AggregationEngine.get_groupby_sql('date', 'revenue', 'sum', 'financial_data')
# Returns: "SELECT date, SUM(revenue) as sum_revenue FROM financial_data GROUP BY date"


# ===========================================================================
# PHASE E: VISUALIZATIONS
# ===========================================================================

from utils.chart_generator import ChartGenerator

# Line chart
fig = ChartGenerator.create_line_chart(
    df=df,
    x_column='date',
    y_columns=['revenue', 'profit'],
    title="Revenue & Profit Trends"
)
st.plotly_chart(fig)

# Bar chart
fig = ChartGenerator.create_bar_chart(
    df=df,
    x_column='date',
    y_column='cost',
    title="Cost Distribution"
)

# Pie chart
fig = ChartGenerator.create_pie_chart(
    df=df,
    values_column='revenue',
    names_column='date',
    title="Revenue Distribution"
)

# Scatter plot
fig = ChartGenerator.create_scatter_plot(
    df=df,
    x_column='revenue',
    y_column='cost',
    size_column='profit',  # Optional
    color_column='date',   # Optional
    title="Revenue vs Cost Relationship"
)

# Histogram
fig = ChartGenerator.create_histogram(
    df=df,
    column='revenue',
    nbins=30,
    title="Revenue Distribution"
)

# Box plot
fig = ChartGenerator.create_box_plot(
    df=df,
    y_columns=['revenue', 'cost', 'profit'],
    title="Distribution Summary"
)

# Heatmap (correlation)
fig = ChartGenerator.create_heatmap(
    df=df,
    title="Correlation Matrix"
)


# ===========================================================================
# PHASE F: EXPORT
# ===========================================================================

from utils.export_manager import ExportManager

# Export to CSV
csv_bytes, filename = ExportManager.export_to_csv(df, filename="mydata.csv")
st.download_button("📥 Download CSV", csv_bytes, filename)

# Export to Excel
excel_bytes, filename = ExportManager.export_to_excel(df)
st.download_button("📥 Download Excel", excel_bytes, filename)

# Export to JSON
json_bytes, filename = ExportManager.export_to_json(
    df,
    orient='records'  # records, table, split, index
)

# Export multiple sheets
dataframes = {
    'Data': df,
    'Summary': summary_df,
    'Analysis': analysis_df
}
excel_bytes, filename = ExportManager.export_multiple_sheets(dataframes)

# Export summary
summary_dict = {'rows': 25, 'columns': 3, 'numeric_cols': 2}
json_bytes, filename = ExportManager.export_summary_to_json(summary_dict)


# ===========================================================================
# PHASE G: AI Q&A
# ===========================================================================

from utils.ai_insights import DataInsightAI

ai = DataInsightAI(db, 'financial_data')

# Ask question
answer = ai.answer_question("What's the highest revenue?")
st.markdown(answer)

# Get confidence
confidence = ai.get_confidence_score()
st.caption(f"Confidence: {confidence*100:.0f}%")

# Supported question types:
# - "What's the maximum/highest/largest revenue?"
# - "Show me the minimum/lowest cost"
# - "What's the total/sum profit?"
# - "Average revenue?"
# - "How many records?"
# - "Is revenue increasing? (trend)"
# - "Compare revenue vs cost"
# - "Profit margin?"
# - "Revenue to cost ratio?"


# ===========================================================================
# PHASE H: PERFORMANCE OPTIMIZATION
# ===========================================================================

from utils.performance import ComputationCache, QueryOptimizer

# Cache expensive computation
@ComputationCache.cached_computation(ttl_minutes=60)
def expensive_analytics_computation(data):
    # Long-running operation
    return result

# Use in code
result = expensive_analytics_computation(df)  # Cached after first call

# Clear cache
ComputationCache.clear_cache()

# Clean expired entries
ComputationCache.cleanup_expired()

# Query optimization helpers
query = QueryOptimizer.optimize_select_query('financial_data', ['revenue', 'cost'])
agg_query = QueryOptimizer.optimize_aggregation_query('financial_data', 'revenue', 'sum')
filter_query = QueryOptimizer.optimize_filter_query(
    'financial_data', 'revenue', '>', 500
)


# ===========================================================================
# PHASE I: DATASET MANAGEMENT
# ===========================================================================

from utils.dataset_manager import DatasetManager

dm = DatasetManager()

# List datasets
tables, error = dm.list_all_datasets()
# Returns: ['financial_data', 'sales_data', 'customers']

# Get dataset info
info, error = dm.get_dataset_info('financial_data')
# Returns: {'name': 'financial_data', 'row_count': 25, 'columns': [...]}

# Delete dataset
success, msg = dm.delete_dataset('old_data')

# Rename dataset
success, msg = dm.rename_dataset('old_name', 'new_name')

# Check if exists
exists = dm.table_exists('financial_data')

# Get summary
summary = dm.get_dataset_summary('financial_data')
# Returns: {'rows': 25, 'columns': 4, 'numeric_cols': 3, ...}


# ===========================================================================
# COMPLETE WORKFLOW EXAMPLE
# ===========================================================================

import streamlit as st
from database.db import Database
from utils.error_handler import ErrorHandler
from analytics.profiling import DataProfiler
from utils.filter_engine import FilterParser, FilterEngine
from utils.aggregation_engine import AggregationEngine
from utils.chart_generator import ChartGenerator
from utils.export_manager import ExportManager
from utils.ai_insights import DataInsightAI
from utils.dataset_manager import DatasetManager

# Setup
db = Database()
profiler = DataProfiler()
dm = DatasetManager()

# User uploads CSV
uploaded_file = st.file_uploader("Choose CSV")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Validate
    is_valid, error = ErrorHandler.validate_csv_upload(df)
    if not is_valid:
        st.error(error)
    else:
        # Profile
        summary = profiler.get_summary_stats(df)
        st.write(f"Loaded {summary['total_rows']} rows, {summary['total_columns']} columns")
        
        # Filter
        filter_input = st.text_input("Filter (e.g., revenue > 500)")
        if filter_input:
            is_valid, filter_dict, error = FilterParser.parse_filter(filter_input)
            if is_valid:
                df_filtered, error = FilterEngine.apply_filter(df, filter_dict)
            else:
                st.error(error)
        
        # Aggregate
        col1, col2 = st.columns(2)
        with col1:
            group_col = st.selectbox("Group by", df.columns)
        with col2:
            agg_col = st.selectbox("Aggregate", df.select_dtypes(include=['number']).columns)
        
        agg_func = st.radio("Function", ['sum', 'mean', 'min', 'max', 'count'])
        
        result_df, error = AggregationEngine.group_and_aggregate(
            df, group_col, agg_col, agg_func
        )
        
        # Visualize
        fig = ChartGenerator.create_bar_chart(
            result_df, group_col, f'{agg_func}_{agg_col}'
        )
        st.plotly_chart(fig)
        
        # Export
        csv_bytes, fname = ExportManager.export_to_csv(result_df)
        st.download_button("Download CSV", csv_bytes, fname)
        
        # AI
        ai = DataInsightAI(db, 'table_name')
        question = st.text_input("Ask AI:")
        if question:
            answer = ai.answer_question(question)
            st.markdown(answer)
            confidence = ai.get_confidence_score()
            st.caption(f"Confidence: {confidence*100:.0f}%")


# ===========================================================================
# END OF QUICK REFERENCE
# ===========================================================================
