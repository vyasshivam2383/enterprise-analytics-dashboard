"""
Advanced Visualization Module
Provides enhanced charting capabilities with multiple visualization types
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Dict, Any


class ChartGenerator:
    """Generate various professional charts for data visualization"""
    
    # Professional color palette (matches dark theme)
    COLORS = {
        'primary': '#00D9FF',      # Cyan
        'secondary': '#00FF88',     # Green
        'accent': '#FF6B6B',        # Red
        'neutral': '#888888',       # Gray
        'bg': '#0a0e27'            # Dark background
    }
    
    @staticmethod
    def create_line_chart(
        df: pd.DataFrame,
        x_column: str,
        y_columns: list,
        title: str = "Trend Analysis"
    ) -> Optional[go.Figure]:
        """
        Create interactive line chart
        
        Args:
            df: Input DataFrame
            x_column: X-axis column
            y_columns: List of Y-axis columns
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = px.line(
                df,
                x=x_column,
                y=y_columns,
                title=title,
                markers=True,
                line_shape='linear'
            )
            
            # Apply theme
            fig.update_layout(
                plot_bgcolor=ChartGenerator.COLORS['bg'],
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16,
                hovermode='x unified'
            )
            
            fig.update_traces(
                line=dict(width=2),
                marker=dict(size=6)
            )
            
            return fig
        
        except Exception as e:
            print(f"Error creating line chart: {str(e)}")
            return None
    
    @staticmethod
    def create_bar_chart(
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: str = "Distribution"
    ) -> Optional[go.Figure]:
        """
        Create interactive bar chart
        
        Args:
            df: Input DataFrame
            x_column: X-axis column
            y_column: Y-axis column
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = px.bar(
                df,
                x=x_column,
                y=y_column,
                title=title
            )
            
            # Apply theme
            fig.update_layout(
                plot_bgcolor=ChartGenerator.COLORS['bg'],
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16
            )
            
            fig.update_traces(marker_color=ChartGenerator.COLORS['primary'])
            
            return fig
        
        except Exception as e:
            print(f"Error creating bar chart: {str(e)}")
            return None
    
    @staticmethod
    def create_pie_chart(
        df: pd.DataFrame,
        values_column: str,
        names_column: str,
        title: str = "Distribution"
    ) -> Optional[go.Figure]:
        """
        Create interactive pie chart
        
        Args:
            df: Input DataFrame
            values_column: Column with values
            names_column: Column with labels
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = px.pie(
                df,
                values=values_column,
                names=names_column,
                title=title
            )
            
            # Apply theme
            fig.update_layout(
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16
            )
            
            return fig
        
        except Exception as e:
            print(f"Error creating pie chart: {str(e)}")
            return None
    
    @staticmethod
    def create_scatter_plot(
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        size_column: Optional[str] = None,
        color_column: Optional[str] = None,
        title: str = "Relationship Analysis"
    ) -> Optional[go.Figure]:
        """
        Create interactive scatter plot
        
        Args:
            df: Input DataFrame
            x_column: X-axis column
            y_column: Y-axis column
            size_column: Optional column for point size
            color_column: Optional column for point color
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                size=size_column,
                color=color_column,
                title=title,
                hover_data=df.columns.tolist()
            )
            
            # Apply theme
            fig.update_layout(
                plot_bgcolor=ChartGenerator.COLORS['bg'],
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16,
                hovermode='closest'
            )
            
            return fig
        
        except Exception as e:
            print(f"Error creating scatter plot: {str(e)}")
            return None
    
    @staticmethod
    def create_histogram(
        df: pd.DataFrame,
        column: str,
        nbins: int = 30,
        title: str = "Distribution"
    ) -> Optional[go.Figure]:
        """
        Create interactive histogram
        
        Args:
            df: Input DataFrame
            column: Column to visualize
            nbins: Number of bins
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = px.histogram(
                df,
                x=column,
                nbins=nbins,
                title=title
            )
            
            # Apply theme
            fig.update_layout(
                plot_bgcolor=ChartGenerator.COLORS['bg'],
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16
            )
            
            fig.update_traces(marker_color=ChartGenerator.COLORS['secondary'])
            
            return fig
        
        except Exception as e:
            print(f"Error creating histogram: {str(e)}")
            return None
    
    @staticmethod
    def create_box_plot(
        df: pd.DataFrame,
        y_columns: list,
        title: str = "Distribution Summary"
    ) -> Optional[go.Figure]:
        """
        Create interactive box plot
        
        Args:
            df: Input DataFrame
            y_columns: Columns to visualize
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            fig = go.Figure()
            
            for col in y_columns:
                fig.add_trace(go.Box(
                    y=df[col],
                    name=col,
                    boxmean='sd'
                ))
            
            fig.update_layout(
                title=title,
                plot_bgcolor=ChartGenerator.COLORS['bg'],
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16,
                showlegend=True
            )
            
            return fig
        
        except Exception as e:
            print(f"Error creating box plot: {str(e)}")
            return None
    
    @staticmethod
    def create_heatmap(
        df: pd.DataFrame,
        title: str = "Correlation Matrix"
    ) -> Optional[go.Figure]:
        """
        Create correlation heatmap
        
        Args:
            df: Input DataFrame (should be numeric columns)
            title: Chart title
            
        Returns:
            Plotly Figure object or None on error
        """
        try:
            # Select only numeric columns
            numeric_df = df.select_dtypes(include=['number'])
            
            if numeric_df.empty:
                return None
            
            corr_matrix = numeric_df.corr()
            
            fig = px.imshow(
                corr_matrix,
                labels=dict(color="Correlation"),
                title=title,
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1
            )
            
            fig.update_layout(
                paper_bgcolor=ChartGenerator.COLORS['bg'],
                font=dict(color='white'),
                title_font_size=16
            )
            
            return fig
        
        except Exception as e:
            print(f"Error creating heatmap: {str(e)}")
            return None
