"""
Enterprise Analytics Dashboard - Streamlit Application
Features: File Upload, Dynamic Analytics, SQL Storage, AI Q&A
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime
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
if 'service' not in st.session_state:
    st.session_state.service = AnalyticsService()

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = None

if 'current_table' not in st.session_state:
    st.session_state.current_table = 'financial_data'


@st.cache_resource
def get_service():
    """Get cached analytics service."""
    return AnalyticsService()


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
        table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
        
        # Get database
        service = get_service()
        db = service.db
        
        # Create table with dynamic columns
        columns = {}
        for col in df.columns:
            # Infer data type
            if df[col].dtype in ['int64', 'float64']:
                columns[col] = 'REAL'
            else:
                columns[col] = 'TEXT'
        
        # Create table
        db.create_table_from_columns(table_name, columns)
        
        # Insert data
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns.keys())}) VALUES ({', '.join(['?' for _ in columns])})"
        db.insert_many(insert_query, [tuple(row) for _, row in df.iterrows()])
        
        st.session_state.current_table = table_name
        st.session_state.ai_engine = DataInsightAI(db, table_name)
        st.session_state.uploaded_file = uploaded_file.name
        st.session_state.data_loaded = True
        
        return df
    
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
            service = get_service()
            service.load_data()
            st.session_state.data_loaded = True
            st.session_state.current_table = 'financial_data'
            st.session_state.ai_engine = DataInsightAI(service.db, 'financial_data')
            st.success("✅ Sample data loaded!")
            st.rerun()
    
    elif sidebar_tab == "📁 Upload Data":
        st.markdown("### Upload CSV File")
        uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
        
        if uploaded_file is not None:
            st.info(f"📄 File: {uploaded_file.name}")
            
            if st.button("📤 Process & Analyze", use_container_width=True):
                with st.spinner("Processing file..."):
                    df = process_uploaded_file(uploaded_file)
                    if df is not None:
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
    if st.session_state.data_loaded:
        service = get_service()
        db = service.db
        
        try:
            result = db.execute(f"SELECT COUNT(*) FROM {st.session_state.current_table}")
            records = result[0][0] if result else 0
            st.metric("📊 Total Records", records)
            st.metric("📍 Table", st.session_state.current_table.replace('_', ' ').title())
        except:
            pass


# Main content
st.title("📊 Enterprise Analytics Dashboard")
st.markdown("Real-time analytics, SQL storage, and AI-powered insights")

if st.session_state.data_loaded:
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Analytics", "📊 Data", "💬 AI Assistant"])
    
    with tab1:
        st.markdown("### 💰 Key Performance Indicators")
        
        service = get_service()
        service.load_data()
        analytics = service.get_all_analytics()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Revenue</div>
                <div class="metric-value">${analytics['total_revenue']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Cost</div>
                <div class="metric-value">${analytics['total_cost']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Profit</div>
                <div class="metric-value">${analytics['total_profit']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 📈 Trends & Visualizations")
        
        daily_data = service.get_daily_data()
        df_display = pd.DataFrame(daily_data, columns=['Date', 'Revenue', 'Cost', 'Profit'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.line_chart(
                data=df_display.set_index('Date')[['Revenue', 'Profit']],
                width='stretch',
                height=300
            )
            st.caption("Revenue & Profit Trends")
        
        with col2:
            st.bar_chart(
                data=df_display.set_index('Date')[['Cost']],
                width='stretch',
                height=300
            )
            st.caption("Cost Distribution")
        
        st.divider()
        
        st.markdown("### 📊 Summary Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Avg Revenue", f"${analytics['avg_revenue']:,.0f}")
        with col2:
            st.metric("Avg Cost", f"${analytics['avg_cost']:,.0f}")
        with col3:
            st.metric("Avg Profit", f"${analytics['avg_profit']:,.0f}")
        with col4:
            st.metric("Profit Margin", f"{analytics['profit_margin']:.1f}%")
    
    with tab2:
        st.markdown("### 📋 Data Table")
        
        service = get_service()
        daily_data = service.get_daily_data()
        df_display = pd.DataFrame(daily_data, columns=['Date', 'Revenue', 'Cost', 'Profit'])
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_display.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="analytics_data.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with tab3:
        st.markdown("### 💬 AI Assistant - Ask Questions About Your Data")
        
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
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            user_question = st.text_input("Ask a question about your data...", placeholder="e.g., What is the total revenue?")
        
        with col2:
            ask_button = st.button("Send", use_container_width=True)
        
        if ask_button and user_question:
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_question
            })
            
            # Get AI response
            if st.session_state.ai_engine:
                ai_response = st.session_state.ai_engine.answer_question(user_question)
            else:
                ai_response = "❌ AI engine not initialized. Please load data first."
            
            # Add AI response
            st.session_state.chat_history.append({
                'role': 'ai',
                'content': ai_response
            })
            
            st.rerun()

else:
    st.info("👈 Choose 'Sample Data' or 'Upload Data' in the sidebar to get started!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📥 Sample Data")
        st.write("Load our demo financial dataset to see the dashboard in action.")
    
    with col2:
        st.markdown("### 📁 Upload Your Data")
        st.write("Upload your own CSV file to analyze your data with AI insights.")

st.divider()
st.caption("Enterprise Analytics Dashboard | File Upload | SQL Storage | AI Q&A | Production Ready")
