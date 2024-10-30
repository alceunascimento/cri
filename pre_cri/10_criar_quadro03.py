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
                return '\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0' + str(x)
            elif any(str(x).startswith(p) for p in first_indent_patterns):
                return '\u00A0\u00A0\u00A0\u00A0' + str(x)
        return x

    def format_number(value, decimals=8):
        """Format number with thousand separator and specified decimals"""
        if pd.isna(value):
            return '-'
        
        # Format with thousand separator and specified decimals
        formatted = f'{value:,.{decimals}f}'
        # Replace dots and commas correctly for Brazilian format
        formatted = formatted.replace(',', '@').replace('.', ',').replace('@', '.')
        return formatted

    def format_percentage(value):
        """Format number as percentage with 2 decimal places"""
        if pd.isna(value):
            return '-'
        
        # Convert to percentage and format with 2 decimal places
        percentage = value * 100
        formatted = f'{percentage:.2f}'.replace('.', ',')
        return f'{formatted}%'

    def format_date(value):
        """Format number as date MM/YYYY"""
        if pd.isna(value):
            return '-'
        try:
            # Assuming value is in YYYYMM format as integer
            year = int(value) // 100
            month = int(value) % 100
            return f'{month:02d}/{year}'
        except:
            return str(value)

    # Define format for each cell based on its content and position
    def custom_format(val, item=None, column=None):
        # Handle NaN/None values consistently
        if pd.isna(val):
            return '-'
            
        # Special case for date
        if str(item).strip() == '3.1. Data' and column == 'valor':
            return format_date(val)
            
        # For the 'outros' column, format as percentage
        if column == 'outros' and isinstance(val, (int, float)):
            if str(item).strip() in ['4.', '5.', '5.1.']:  # Header rows
                return '-'
            return format_percentage(val)
            
        if isinstance(val, (int, float)):
            # For all values in 'valor' column
            if column == 'valor':
                if str(item).strip() in ['4.', '5.', '5.1.']:  # Header rows
                    return '-'
                return format_number(val, 2)
            
            # For percentage values (column 3)
            elif val <= 1:
                return format_number(val, 8)
            
            # For other numeric values
            else:
                return format_number(val, 8)
                
        # Convert string 'nan' to '-'
        if str(val).lower() == 'nan':
            return '-'
                
        return str(val)

    # Apply indentation
    df = df.copy()
    df['item'] = df['item'].apply(indent_item)

    # Format all columns consistently
    for col in df.columns:
        df[col] = df.apply(lambda row: custom_format(row[col], row['item'], col), axis=1)

    return df.style.hide(axis='index').hide(axis='columns').set_table_styles([
        # Overall table styling
        {'selector': 'table', 'props': [
            ('width', '100%'),
            ('border-collapse', 'collapse'),
            ('margin', '0'),
            ('table-layout', 'fixed'),
            ('font-family', 'Arial'),
            ('font-size', '11px')
        ]},
        # Column styling for first column (left-aligned)
        {'selector': 'td:nth-child(1)', 'props': [
            ('text-align', 'left'),
            ('border', '1px solid black'),
            ('padding', '2px 4px'),
            ('width', '60%')
        ]},
        # Column styling for other columns (right-aligned)
        {'selector': 'td:nth-child(2), td:nth-child(3)', 'props': [
            ('text-align', 'right'),
            ('border', '1px solid black'),
            ('padding', '2px 4px'),
            ('width', '20%')
        ]}
    ])

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
            <td style="border: 1px solid black; padding: 2px 4px;">Local do Imóvel: {info_data['local_construcao']}, {info_data['cidade_uf']}</td>
            <td style="border: 1px solid black; padding: 2px 4px;">Folha 4</td>
            <td colspan="2" style="border: 1px solid black; padding: 2px 4px;">Total de Folhas 10</td>
        </tr>
        <tr>
        <td style="border: 1px solid black;">Nome do edifício: {info_data['nome_edificio']}</td>
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
                SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao, cidade_uf, nome_edificio 
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