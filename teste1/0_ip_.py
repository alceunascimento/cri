import pandas as pd
import sqlite3

# Carregar a aba `informacoes_preliminares` da pasta de trabalho
workbook_path = './data/base_real_ajustada.xlsx'
sheet_name = 'informacoes_preliminares'

# Ler as variáveis a partir da coluna B e os valores da coluna C (índice começa em 0, então B é 1 e C é 2)
df_informacoes_preliminares = pd.read_excel(workbook_path, sheet_name=sheet_name, usecols=[1, 2], header=None, names=['chave', 'valor'], skiprows=1)

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')

# Criar a tabela `informacoes_preliminares` no banco de dados
df_informacoes_preliminares.to_sql('informacoes_preliminares', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `informacoes_preliminares` criada e populada com sucesso.")