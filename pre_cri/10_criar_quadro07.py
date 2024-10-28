import sqlite3
import pandas as pd
import os
from datetime import datetime

def connect_database(db_path):
    """Establish database connection with error handling"""
    try:
        return sqlite3.connect(db_path)
    except sqlite3.Error as e:
        raise Exception(f"Failed to connect to database: {e}")

def execute_query(conn, query):
    """Execute SQL query with error handling"""
    try:
        return pd.read_sql_query(query, conn)
    except (sqlite3.Error, pd.io.sql.DatabaseError) as e:
        raise Exception(f"Query execution failed: {e}")

def ensure_output_directory(path):
    """Ensure output directory exists"""
    os.makedirs(os.path.dirname(path), exist_ok=True)

def validate_dataframe(df, required_columns):
    """Validate dataframe has required columns"""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

def create_multi_index_columns():
    """Create proper multi-index columns"""
    return [
        "DEPENDÊNCIAS",
        "PISOS",
        "PAREDES",
        "TETOS",
        "OUTROS"
    ]
    
def format_styler(df):
    """Format dataframe with styling"""
    return df.style.hide(axis='index').set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background-color', 'lightgrey'),
            ('text-align', 'center'),
            ('font-weight', 'bold'),
            ('display', 'table-cell'),
            ('border', '1px solid black')
        ]},
        {'selector': 'tbody td', 'props': [
            ('border', '1px solid black'),
            ('text-align', 'right')
        ]},
    ]).format(na_rep='-')

def generate_header_html(info_data):
    """Generate HTML header with proper escaping"""
    return f"""
    <table style="width: 100%; border: 1px solid black; border-collapse: collapse;">
        <tr>
            <td colspan="6" style="text-align: center; font-weight: bold; border: 1px solid black;">
                INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS<br>
                (Lei 4.591 - 16/12/64 - Art. 32 e ABNT NBR 12721)
            </td>
        </tr>
        <tr>
            <td colspan="6" style="text-align: center; border: 1px solid black;">
                QUADRO VII - MEMORIAL DESCRITIVO DOS ACABAMENTOS  (Dependências de uso privativo)
            </td>
        </tr>
        <tr>
            <td colspan="3" style="border: 1px solid black;">Local do Imóvel: {info_data['local_construcao']}, Curitiba, Paraná</td>
            <td style="border: 1px solid black;">Folha 2</td>
            <td colspan="2" style="border: 1px solid black;">Total de Folhas 10</td>
        </tr>
        <tr>
        <td style="border: 1px solid black;">Nome do edifício: {info_data['nome_edificio']}</td>
        </tr>
        <tr>
            <td colspan="3" style="border: 1px solid black;">INCORPORADOR</td>
            <td colspan="3" style="border: 1px solid black;">PROFISSIONAL RESPONSÁVEL</td>
        </tr>
        <tr>
            <td colspan="2" style="border: 1px solid black;">{info_data['nome_incorporador']}</td>
            <td style="border: 1px solid black;">Data: 28/10/2024</td>
            <td colspan="3" style="border: 1px solid black;">{info_data['nome_responsavel_tecnico']} ({info_data['registro_crea']})</td>
        </tr>
    </table>
    """

def main():
    # Configuration
    db_path = './pre_cri/base_real.db'
    output_path = "./pre_cri/output/nbr_07_quadro_area_07.html"
    
    try:
        # Ensure database exists
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")

        # Connect to database
        conn = connect_database(db_path)
        
        try:
            # Load main data
            df_quadro_area_07 = execute_query(conn, "SELECT * FROM quadro_area_07")
            
            # Clean ROWID and subcondominio if present
            if 'ROWID' in df_quadro_area_07.columns:
                df_quadro_area_07 = df_quadro_area_07.drop(columns=['ROWID'])
            if 'subcondominio' in df_quadro_area_07.columns:
                df_quadro_area_07 = df_quadro_area_07.drop(columns=['subcondominio'])
            
            # Load header information
            header_query = """
                SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao, nome_edificio
                FROM informacoes_preliminares 
                LIMIT 1
            """
            header_info = execute_query(conn, header_query)
            
            if header_info.empty:
                raise ValueError("No preliminary information found in database")
            
            info_data = header_info.iloc[0].to_dict()
            
            # Set up multi-index columns
            columns = create_multi_index_columns()
            df_quadro_area_07.columns = columns[:len(df_quadro_area_07.columns)]
            
            # Format table
            styled_table = format_styler(df_quadro_area_07)
            
            # Generate complete HTML
            header_html = generate_header_html(info_data)
            complete_html = header_html + styled_table._repr_html_()
            
            # Ensure output directory exists
            ensure_output_directory(output_path)
            
            # Save file
            with open(output_path, "w", encoding='utf-8') as file:
                file.write(complete_html)
            
            print(f"HTML file successfully generated at: {output_path}")
            
        finally:
            conn.close()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()