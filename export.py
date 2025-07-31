import sqlite3
import pandas as pd
import os

class SimpleDataExporter:
    def __init__(self, db_path='placement.db'):
        self.db_path = db_path
        self.tables = ['students', 'programming', 'soft_skills', 'placements']
    
    def export_to_csv(self, output_folder='placement_data'):
        """Export all tables to CSV files"""
        os.makedirs(output_folder, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            for table in self.tables:
                df = pd.read_sql(f"SELECT * FROM {table}", conn)
                df.to_csv(f"{output_folder}/{table}.csv", index=False)
                print(f"Exported {table}.csv")
        
        print("\nValidation:")
        for table in self.tables:
            file_path = f"{output_folder}/{table}.csv"
            if os.path.exists(file_path):
                print(f"✓ {file_path} exists")
            else:
                print(f"✗ {file_path} missing")

if __name__ == "__main__":
    exporter = SimpleDataExporter()
    exporter.export_to_csv()
