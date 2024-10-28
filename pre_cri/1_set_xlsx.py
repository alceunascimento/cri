import pandas as pd
import sqlite3
import os
import sys
from pathlib import Path

def setup_database():
    """
    Set up the database connection with proper error handling and existing database removal.
    Returns a connection object or None if setup fails.
    """
    try:
        db_path = Path('./pre_cri/base_real.db')
        
        # Create pre_cri directory if it doesn't exist
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Remove existing database if it exists
        if db_path.exists():
            try:
                db_path.unlink()  # Delete the file
                print(f"Existing database removed: {db_path}")
            except PermissionError:
                print(f"Error: Cannot delete existing database. File may be in use.")
                return None
            except Exception as e:
                print(f"Error removing existing database: {str(e)}")
                return None
        
        # Create new database connection
        return sqlite3.connect(str(db_path))
    
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return None

def main():
    try:
        # Setup paths
        workbook_path = Path('./pre_cri/data/base_real_ajustada.xlsx')
        
        # Verify Excel file exists
        if not workbook_path.exists():
            print(f"Error: Excel file not found at {workbook_path}")
            sys.exit(1)
            
        # Setup database connection
        conn = setup_database()
        if conn is None:
            print("Failed to setup database connection")
            sys.exit(1)
            
        try:
            # Define sheet names
            sheet_names = [
                'informacoes_preliminares', 'quadro_area_01', 'quadro_area_02', 
                'quadro_area_03', 'quadro_area_04A', 'quadro_area_04B', 
                'quadro_area_05', 'quadro_area_06', 'quadro_area_07', 
                'quadro_area_08', 'quadro_resumo'
            ]

            # Load each sheet into a dictionary of dataframes
            dataframes = {}
            for sheet in sheet_names:
                try:
                    dataframes[sheet] = pd.read_excel(workbook_path, sheet_name=sheet)
                    print(f"Successfully loaded sheet: {sheet}")
                except Exception as e:
                    print(f"Error loading sheet {sheet}: {str(e)}")
                    continue

            print("Estrutura base configurada. Vamos começar a trabalhar aba por aba.")
            
            return dataframes, conn
            
        except Exception as e:
            print(f"Error processing Excel file: {str(e)}")
            return None, None
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None, None
        
    finally:
        # Ensure connection is closed even if an error occurs
        if 'conn' in locals() and conn is not None:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    dataframes, conn = main()
    if dataframes is None:
        sys.exit(1)