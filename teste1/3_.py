import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_03` da pasta de trabalho
workbook_path = './data/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_03'

# Ler as variáveis a partir da coluna B e os valores da coluna C (índice começa em 0, então B é 1 e C é 2)
df_quadro_area_03 = pd.read_excel(workbook_path, sheet_name=sheet_name, usecols=[1, 2], header=None, names=['chave', 'valor'], skiprows=1)

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')

# Criar a tabela `quadro_area_03` no banco de dados
df_quadro_area_03.to_sql('quadro_area_03', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_03` criada e populada com sucesso.")