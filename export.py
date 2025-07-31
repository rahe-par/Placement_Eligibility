import sqlite3
import pandas as pd
from typing import List

class PlacementDataExporter:
    def __init__(self, db_path: str = 'placement.db'):
        self.db_path = db_path
        self.tables = [
            'students', 
            'programming', 
            'soft_skills', 
            'placements'
        ]
    
    def export_to_csv(self, output_folder: str = 'placement_data') -> None:
        """Export all tables to CSV files in the specified folder"""
        import os
        os.makedirs(output_folder, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        
        for table in self.tables:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
            file_path = f"{output_folder}/{table}.csv"
            df.to_csv(file_path, index=False)
            print(f"Exported {table} to {file_path}")
        
        conn.close()
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a specific table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        conn.close()
        return columns
    
    def validate_data_export(self, output_folder: str = 'placement_data') -> bool:
        """Validate that all CSV files were created correctly"""
        import os
        all_valid = True
        
        for table in self.tables:
            file_path = f"{output_folder}/{table}.csv"
            if not os.path.exists(file_path):
                print(f"Error: {file_path} not found")
                all_valid = False
                continue
                
            try:
                df = pd.read_csv(file_path)
                expected_columns = self.get_table_columns(table)
                if not all(col in df.columns for col in expected_columns):
                    print(f"Error: {file_path} has missing columns")
                    all_valid = False
            except Exception as e:
                print(f"Error reading {file_path}: {str(e)}")
                all_valid = False
        
        return all_valid


if __name__ == "__main__":
    # Example usage
    exporter = PlacementDataExporter()
    
    print("Exporting data to CSV files...")
    exporter.export_to_csv()
    
    print("\nValidating exported data...")
    if exporter.validate_data_export():
        print("All CSV files exported successfully and validated!")
    else:
        print("There were issues with some exported files")