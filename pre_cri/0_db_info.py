import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DatabaseDocumentGenerator:
    def __init__(self, db_path: str = './pre_cri/base_real.db'):
        self.db_path = Path(db_path)
        self.output_path = self.db_path.parent / f"database_structure_{datetime.now().strftime('%Y%m%d')}.txt"
        self.conn = None

    def connect_to_database(self) -> None:
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            logging.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            raise

    def get_table_names(self) -> List[str]:
        """Get all table names from the database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            logging.error(f"Error retrieving table names: {e}")
            raise

    def get_table_info(self, table_name: str) -> List[Tuple]:
        """Get column information for a specific table"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error retrieving table info for {table_name}: {e}")
            raise

    def get_table_sample(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        """Get a sample of records from the table"""
        try:
            return pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", self.conn)
        except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
            logging.error(f"Error retrieving sample data for {table_name}: {e}")
            raise

    def generate_documentation(self) -> None:
        """Generate documentation file with database structure"""
        try:
            with open(self.output_path, 'w', encoding='utf-8') as file:
                # Write header
                file.write("DATABASE STRUCTURE DOCUMENTATION\n")
                file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Database: {self.db_path.name}\n")
                file.write("="*80 + "\n\n")

                # Get and process each table
                tables = self.get_table_names()
                for table_name in tables:
                    # Table header
                    file.write(f"TABLE: {table_name}\n")
                    file.write("-"*80 + "\n\n")

                    # Column information
                    file.write("COLUMNS:\n")
                    columns = self.get_table_info(table_name)
                    for col in columns:
                        col_id, name, dtype, notnull, default, pk = col
                        file.write(f"- {name}\n")
                        file.write(f"  Type: {dtype}\n")
                        file.write(f"  Nullable: {'No' if notnull else 'Yes'}\n")
                        file.write(f"  Primary Key: {'Yes' if pk else 'No'}\n")
                        file.write(f"  Default: {default if default else 'None'}\n")
                        file.write("\n")

                    # Sample data
                    file.write("SAMPLE DATA:\n")
                    sample_df = self.get_table_sample(table_name)
                    file.write(sample_df.to_string())
                    file.write("\n\n")
                    file.write("="*80 + "\n\n")

            logging.info(f"Documentation generated successfully: {self.output_path}")

        except Exception as e:
            logging.error(f"Error generating documentation: {e}")
            raise

    def close_connection(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed")

def main():
    doc_generator = DatabaseDocumentGenerator()
    try:
        doc_generator.connect_to_database()
        doc_generator.generate_documentation()
    except Exception as e:
        logging.error(f"Documentation generation failed: {e}")
        raise
    finally:
        doc_generator.close_connection()

if __name__ == "__main__":
    main()