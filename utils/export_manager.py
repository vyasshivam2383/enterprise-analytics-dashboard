"""
Export System
Handles exporting data in multiple formats: CSV, Excel, JSON
"""
import pandas as pd
import json
from typing import Tuple, Optional
from datetime import datetime


class ExportManager:
    """Manage data exports in multiple formats"""
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, filename: Optional[str] = None) -> Tuple[bytes, str]:
        """
        Export DataFrame to CSV
        
        Args:
            df: Input DataFrame
            filename: Optional filename
            
        Returns:
            Tuple of (csv_bytes, filename)
        """
        try:
            if filename is None:
                filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            
            return csv_bytes, filename
        
        except Exception as e:
            raise Exception(f"Error exporting to CSV: {str(e)}")
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, filename: Optional[str] = None) -> Tuple[bytes, str]:
        """
        Export DataFrame to Excel
        
        Args:
            df: Input DataFrame
            filename: Optional filename
            
        Returns:
            Tuple of (excel_bytes, filename)
        """
        try:
            if filename is None:
                filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Use BytesIO for in-memory Excel
            import io
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
                
                # Add some formatting
                worksheet = writer.sheets['Data']
                for idx, col in enumerate(df.columns, 1):
                    worksheet.column_dimensions[chr(64 + idx)].width = 15
            
            excel_bytes = output.getvalue()
            
            return excel_bytes, filename
        
        except ImportError:
            raise Exception("openpyxl not installed. Install with: pip install openpyxl")
        except Exception as e:
            raise Exception(f"Error exporting to Excel: {str(e)}")
    
    @staticmethod
    def export_to_json(df: pd.DataFrame, filename: Optional[str] = None, orient: str = 'records') -> Tuple[bytes, str]:
        """
        Export DataFrame to JSON
        
        Args:
            df: Input DataFrame
            filename: Optional filename
            orient: JSON orientation ('records', 'table', 'split', 'index')
            
        Returns:
            Tuple of (json_bytes, filename)
        """
        try:
            if filename is None:
                filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            json_str = df.to_json(orient=orient, indent=2, date_format='iso')
            json_bytes = json_str.encode('utf-8')
            
            return json_bytes, filename
        
        except Exception as e:
            raise Exception(f"Error exporting to JSON: {str(e)}")
    
    @staticmethod
    def export_summary_to_json(summary_dict: dict, filename: Optional[str] = None) -> Tuple[bytes, str]:
        """
        Export summary statistics to JSON
        
        Args:
            summary_dict: Summary statistics dictionary
            filename: Optional filename
            
        Returns:
            Tuple of (json_bytes, filename)
        """
        try:
            if filename is None:
                filename = f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            json_str = json.dumps(summary_dict, indent=2, default=str)
            json_bytes = json_str.encode('utf-8')
            
            return json_bytes, filename
        
        except Exception as e:
            raise Exception(f"Error exporting summary: {str(e)}")
    
    @staticmethod
    def export_multiple_sheets(
        dataframes: dict,
        filename: Optional[str] = None
    ) -> Tuple[bytes, str]:
        """
        Export multiple DataFrames to Excel with multiple sheets
        
        Args:
            dataframes: Dict of {sheet_name: DataFrame}
            filename: Optional filename
            
        Returns:
            Tuple of (excel_bytes, filename)
        """
        try:
            if filename is None:
                filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            import io
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for sheet_name, df in dataframes.items():
                    df.to_excel(writer, index=False, sheet_name=sheet_name[:31])  # Excel limit is 31 chars
            
            excel_bytes = output.getvalue()
            
            return excel_bytes, filename
        
        except ImportError:
            raise Exception("openpyxl not installed. Install with: pip install openpyxl")
        except Exception as e:
            raise Exception(f"Error exporting multiple sheets: {str(e)}")
    
    @staticmethod
    def get_export_filename(base_name: str, format_type: str) -> str:
        """
        Generate export filename with timestamp
        
        Args:
            base_name: Base filename
            format_type: 'csv', 'xlsx', 'json'
            
        Returns:
            Full filename with timestamp and extension
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        extensions = {
            'csv': '.csv',
            'xlsx': '.xlsx',
            'json': '.json'
        }
        
        ext = extensions.get(format_type, '.csv')
        return f"{base_name}_{timestamp}{ext}"
