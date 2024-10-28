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

def format_styler(df):
    """Format dataframe with styling specific to Quadro 03"""
    # Define the patterns that need indentation
    first_indent_patterns = [
        'CLASSIFICAÇÃO GERAL',
        'USO COMERCIAL',
        'Dependências de uso privativo da unidade autônoma',
        '3.1.', '3.2.', 
        '4.1.', '4.2.', '4.3.', '4.4.', '4.5.', '4.6.',
        '5.1.', 
        '6.1.', '6.2.', '6.3.', '6.4.', '6.5.', '6.6.',
        '9.1.', '9.2.', '9.3.', '9.4.'
    ]
    
    second_indent_patterns = [
        'Designação',
        'Padrão de acabamento',
        'Número de pavimentos',
        'Área equivalente total do projeto-padrão adotado (m²)',
        'QUARTOS',
        'SALAS',
        'Banheiros ou WC',
        'Quartos de empregados',
        '6.3.1.', '6.3.2.', '6.3.3.', '6.3.4.', '6.3.5.', '6.3.6.', 
        '6.3.7.', '6.3.8.', '6.3.9.', '6.3.10.', '6.3.11.',
        '6.5.1.', '6.5.2.', '6.5.3.', '6.5.4.', '6.5.5.'
    ]

    def indent_item(x):
        if pd.notnull(x):
            if any(str(x).startswith(p) for p in second_indent_patterns):
                return '\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0' + str(x)  # Double indentation
            elif any(str(x).startswith(p) for p in first_indent_patterns):
                return '\u00A0\u00A0\u00A0\u00A0' + str(x)  # Single indentation
        return x

    # Apply indentation directly to the DataFrame
    df = df.copy()
    df['item'] = df['item'].apply(indent_item)

    return df.style.hide(axis='index').set_table_styles([
        # Overall table styling
        {'selector': 'table', 'props': [
            ('width', '100%'),
            ('border-collapse', 'collapse'),
            ('margin', '0'),
            ('table-layout', 'fixed')
        ]},
        # Header styling
        {'selector': 'thead th', 'props': [
            ('background-color', '#E8E8E8'),
            ('text-align', 'center'),
            ('font-weight', 'normal'),
            ('border', '1px solid black'),
            ('padding', '2px 4px')
        ]},
        # Specific column styling
        {'selector': 'td:nth-child(1)', 'props': [  # First column (item)
            ('text-align', 'left'),
            ('border', '1px solid black'),
            ('padding', '2px 4px')
        ]},
        {'selector': 'td:nth-child(2), td:nth-child(3)', 'props': [  # Other columns
            ('text-align', 'right'),
            ('border', '1px solid black'),
            ('padding', '2px 4px')
        ]}
    ]).format(
        na_rep='-',
        precision=2,
        decimal=',',
        thousands='.',
        formatter=lambda x: f'{x:,.2f}' if isinstance(x, (int, float)) else x
    )

def generate_header_html(info_data):
    """Generate HTML header with proper escaping"""
    return f"""
    <table style="width: 100%; border-collapse: collapse; margin: 0; padding: 0;">
        <tr>
            <td colspan="4" style="text-align: center; font-weight: bold; border: 1px solid black; padding: 2px 4px;">
                INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS<br>
                (Lei 4.591 - 16/12/64 - Art. 32 e ABNT NBR 12721)
            </td>
        </tr>
        <tr>
            <td colspan="4" style="text-align: center; border: 1px solid black; padding: 2px 4px;">
                QUADRO III - Avaliação do Custo Global e Unitário da Construção
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 2px 4px;">Local do Imóvel: {info_data['local_construcao']}</td>
            <td style="border: 1px solid black; padding: 2px 4px;">Folha 4</td>
            <td colspan="2" style="border: 1px solid black; padding: 2px 4px;">Total de Folhas 10</td>
        </tr>
        <tr>
            <td colspan="2" style="border: 1px solid black; padding: 2px 4px;">INCORPORADOR</td>
            <td colspan="2" style="border: 1px solid black; padding: 2px 4px;">PROFISSIONAL RESPONSÁVEL</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 2px 4px;">{info_data['nome_incorporador']}</td>
            <td style="border: 1px solid black;">Data: 28/10/2024</td>
            <td colspan="2" style="border: 1px solid black; padding: 2px 4px;">{info_data['nome_responsavel_tecnico']} ({info_data['registro_crea']})</td>
        </tr>
    </table>
    """

def main():
    # Configuration
    db_path = './pre_cri/base_real.db'
    output_path = "./pre_cri/output/nbr_03_quadro_area_03.html"
    
    try:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")

        conn = connect_database(db_path)
        
        try:
            # Load main data
            df_quadro_area_03 = execute_query(conn, "SELECT * FROM quadro_area_03")
            
            # Clean ROWID if present
            if 'ROWID' in df_quadro_area_03.columns:
                df_quadro_area_03 = df_quadro_area_03.drop(columns=['ROWID'])
            
            # Load header information
            header_query = """
                SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao 
                FROM informacoes_preliminares 
                LIMIT 1
            """
            header_info = execute_query(conn, header_query)
            
            if header_info.empty:
                raise ValueError("No preliminary information found in database")
            
            info_data = header_info.iloc[0].to_dict()
            
            # Apply formatting
            styled_table = format_styler(df_quadro_area_03)
            
            # Generate complete HTML
            complete_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; font-size: 11px; }}
                    table {{ border-spacing: 0; }}
                </style>
            </head>
            <body>
                <div style="width: 100%; margin: 0; padding: 0;">
                    {generate_header_html(info_data)}
                    {styled_table._repr_html_()}
                </div>
            </body>
            </html>
            """
            
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