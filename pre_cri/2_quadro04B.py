import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_04B` da pasta de trabalho
workbook_path = './pre_cri/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_04B'

# Ler as variáveis a partir da linha 3 e as colunas a partir da 5 (índice começa em 0, então a coluna 5 é a 4)
df_quadro_area_04B = pd.read_excel(workbook_path, sheet_name=sheet_name, header=2, usecols=lambda x: 'Unnamed' not in x)

# Renomear as colunas conforme especificado
column_names = [
    'subcondominio',
    'unidade_tipo',
    'area_privativa_principal',
    'area_privativa_acessoria',
    'area_privativa_total',
    'area_comum',
    'area_unidade_total',
    'coeficiente_proporcionalidade',
    'unidade_quantidades',
    'obs'
]
df_quadro_area_04B.columns = column_names

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Criar a tabela `quadro_area_04B` no banco de dados
df_quadro_area_04B.to_sql('quadro_area_04B', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_04B` criada e populada com sucesso.")
