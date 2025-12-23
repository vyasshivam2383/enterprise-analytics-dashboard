"""
Enterprise Analytics Dashboard - Streamlit Application
Features: File Upload, Dynamic Analytics, SQL Storage, AI Q&A
"""
import streamlit as st
import pandas as pd
import os
from pathlib import Path
from database.db import Database
from services.analytics_service import AnalyticsService
from utils.ai_insights import DataInsightAI


# Page configuration
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_table' not in st.session_state:
    st.session_state.current_table = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Custom CSS
st.markdown("""
<style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #1a1f3a 0%, #0a0e27 100%);
        border: 1px solid #00D9FF;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #00D9FF;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        color: #888;
        text-transform: uppercase;
    }
    .chat-message {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .chat-user {
        background-color: #1a1f3a;
        border-left: 3px solid #00D9FF;
    }
    .chat-ai {
        background-color: #0a0e27;
        border-left: 3px solid #00FF88;
    }
</style>
""", unsafe_allow_html=True)


def load_sample_data():
    """Load sample financial data."""
    try:
        db = Database()
        service = AnalyticsService(db)
        service.load_data()
        st.session_state.data_loaded = True
        st.session_state.current_table = 'financial_data'
        return db
    except Exception as e:
        st.error(f"❌ Error loading sample data: {str(e)}")
        return None


def process_uploaded_file(uploaded_file):
    """Process and load uploaded CSV file."""
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        if df.empty:
            st.error("❌ Uploaded file is empty!")
            return None
        
        # Create table name from filename
        table_name = uploaded_file.name.replace('.csv', '').replace(' ', '_').lower()
        table_name = ''.join(c if c.isalnum() or c == '_' else '' for c in table_name)
        if not table_name or table_name[0].isdigit():
            table_name = 'table_' + table_name
        table_name = table_name[:50]  # SQLite identifier limit
        
        # Create database and insert data
        db = Database()
        
        # Create table with dynamic columns
        columns = {}
        for col in df.columns:
            col_clean = col.replace(' ', '_').lower()
            # Infer data type
            if df[col].dtype in ['int64', 'float64']:
                columns[col_clean] = 'REAL'
            else:
                columns[col_clean] = 'TEXT'
        
        # Create table
        db.create_table_from_columns(table_name, columns)
        
        # Prepare data with cleaned column names
        data_clean = df.copy()
        data_clean.columns = [c.replace(' ', '_').lower() for c in data_clean.columns]
        
        # Insert data
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns.keys())}) VALUES ({', '.join(['?' for _ in columns])})"
        db.insert_many(insert_query, [tuple(row) for _, row in data_clean.iterrows()])
        
        st.session_state.current_table = table_name
        st.session_state.data_loaded = True
        st.session_state.chat_history = []
        
        return db
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        return None


# Sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Controls")
    
    # Tab selection
    sidebar_tab = st.radio("Choose Mode", ["📊 Sample Data", "📁 Upload Data", "💬 AI Q&A"], label_visibility="collapsed")
    
    st.divider()
    
    if sidebar_tab == "📊 Sample Data":
        if st.button("📥 Load Sample Data", use_container_width=True):
            with st.spinner("Loading sample data..."):
                db = load_sample_data()
                if db:
                    st.success("✅ Sample data loaded!")
                    st.rerun()
    
    elif sidebar_tab == "📁 Upload Data":
        st.markdown("### Upload CSV File")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            st.info(f"📄 File: {uploaded_file.name}")
            
            if st.button("📤 Process & Analyze", use_container_width=True):
                with st.spinner("Processing file..."):
                    db = process_uploaded_file(uploaded_file)
                    if db:
                        st.success("✅ File loaded and analyzed!")
                        st.rerun()
    
    elif sidebar_tab == "💬 AI Q&A":
        if st.session_state.data_loaded:
            st.markdown("### Ask Questions About Your Data")
            st.info("💡 Ask anything about your data and get instant insights!")
        else:
            st.warning("⚠️ Please load data first (Sample or Upload)")
    
    st.divider()
    
    # Statistics
    if st.session_state.data_loaded and st.session_state.current_table:
        try:
            db = Database()
            result = db.execute(f"SELECT COUNT(*) FROM {st.session_state.current_table}")
            records = result[0][0] if result else 0
            st.metric("📊 Total Records", records)
            st.metric("📍 Table", st.session_state.current_table.replace('_', ' ').title())
        except:
            pass


# Main content
st.title("📊 Enterprise Analytics Dashboard")
st.markdown("Real-time analytics, SQL storage, and AI-powered insights")

if st.session_state.data_loaded and st.session_state.current_table:
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Analytics", "📊 Data", "💬 AI Assistant"])
    
    with tab1:
        try:
            st.markdown("### 💰 Key Performance Indicators")
            
            db = Database()
            service = AnalyticsService(db)
            
            # Get analytics based on table
            if st.session_state.current_table == 'financial_data':
                service.load_data()
                analytics = service.get_all_analytics()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Revenue</div>
                        <div class="metric-value">${analytics.get('total_revenue', 0):,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Cost</div>
                        <div class="metric-value">${analytics.get('total_cost', 0):,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Total Profit</div>
                        <div class="metric-value">${analytics.get('total_profit', 0):,.0f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                st.markdown("### 📈 Trends & Visualizations")
                
                daily_data = service.get_daily_data()
                if daily_data:
                    df_display = pd.DataFrame(daily_data, columns=['Date', 'Revenue', 'Cost', 'Profit'])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.line_chart(
                            data=df_display.set_index('Date')[['Revenue', 'Profit']],
                            height=300
                        )
                        st.caption("Revenue & Profit Trends")
                    
                    with col2:
                        st.bar_chart(
                            data=df_display.set_index('Date')[['Cost']],
                            height=300
                        )
                        st.caption("Cost Distribution")
                
                st.divider()
                
                st.markdown("### 📊 Summary Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Avg Revenue", f"${analytics.get('avg_revenue', 0):,.0f}")
                with col2:
                    st.metric("Avg Cost", f"${analytics.get('avg_cost', 0):,.0f}")
                with col3:
                    st.metric("Avg Profit", f"${analytics.get('avg_profit', 0):,.0f}")
                with col4:
                    st.metric("Profit Margin", f"{analytics.get('profit_margin', 0):.1f}%")
            
            else:
                # For custom uploaded files
                st.info("📊 Select data table to view analytics")
                
                # Get basic stats for uploaded file
                query = f"SELECT * FROM {st.session_state.current_table} LIMIT 100"
                result = db.execute(query)
                
                if result:
                    # Get column names
                    cursor_info = db._connection.execute(f"PRAGMA table_info({st.session_state.current_table})")
                    columns = [row[1] for row in cursor_info.fetchall()]
                    
                    df_display = pd.DataFrame(result, columns=columns)
                    
                    st.markdown("### 📊 Data Summary")
                    st.metric("Records", len(result))
                    st.metric("Columns", len(columns))
                    
                    st.markdown("### 📈 Sample Data")
                    st.dataframe(df_display.head(20), use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab2:
        st.markdown("### 📋 Data Table")
        
        try:
            db = Database()
            query = f"SELECT * FROM {st.session_state.current_table}"
            result = db.execute(query)
            
            if result:
                # Get column names
                cursor_info = db._connection.execute(f"PRAGMA table_info({st.session_state.current_table})")
                columns = [row[1] for row in cursor_info.fetchall()]
                
                df_display = pd.DataFrame(result, columns=columns)
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                # Download button
                csv = df_display.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"{st.session_state.current_table}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.markdown("### 💬 AI Assistant - Ask Questions About Your Data")
        
        try:
            db = Database()
            ai_engine = DataInsightAI(db, st.session_state.current_table)
            
            # Chat history display
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(f"""<div class="chat-message chat-user">
                    <strong>You:</strong> {message['content']}
                    </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""<div class="chat-message chat-ai">
                    <strong>AI:</strong> {message['content']}
                    </div>""", unsafe_allow_html=True)
            
            # Input
            col1, col2, col3 = st.columns([0.75, 0.15, 0.1])
            
            with col1:
                user_question = st.text_input("Ask a question about your data...", placeholder="e.g., What is the total revenue?", key="question_input")
            
            with col2:
                ask_button = st.button("Send", use_container_width=True)
            
            with col3:
                if st.button("Clear", use_container_width=True):
                    st.session_state.question_input = ""
                    st.rerun()
            
            if ask_button and user_question:
                # Add user message
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_question
                })
                
                # Get AI response
                ai_response = ai_engine.answer_question(user_question)
                
                # Add AI response
                st.session_state.chat_history.append({
                    'role': 'ai',
                    'content': ai_response
                })
                
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

else:
    st.info("👈 Choose 'Sample Data' or 'Upload Data' in the sidebar to get started!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📥 Sample Data")
        st.write("Load our demo financial dataset to see the dashboard in action with 25 sample records.")
    
    with col2:
        st.markdown("### 📁 Upload Your Data")
        st.write("Upload your own CSV file to analyze your data with AI insights. Works with any CSV format!")

st.divider()
st.caption("Enterprise Analytics Dashboard | File Upload | SQL Storage | AI Q&A | Production Ready")
