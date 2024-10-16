import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_08` da pasta de trabalho
workbook_path = './data/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_08'

# Ler as variáveis a partir da linha 2 (índice começa em 0, então a linha 2 é a de índice 1)
df_quadro_area_08 = pd.read_excel(workbook_path, sheet_name=sheet_name, header=1)

# Renomear as colunas conforme especificado
column_names = [
    'dependencias',
    'pisos',
    'paredes',
    'tetos',
    'outros',
    'subcondominio'
]
df_quadro_area_08.columns = column_names

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')

# Criar a tabela `quadro_area_08` no banco de dados
df_quadro_area_08.to_sql('quadro_area_08', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_08` criada e populada com sucesso.")
