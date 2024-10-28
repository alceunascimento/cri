import pandas as pd
import sqlite3

# Carregar a tabela do arquivo Excel
workbook_path = './pre_cri/data/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_03'

# Ler as três colunas (item, valor, outros) começando da linha 15
df_quadro_area_03 = pd.read_excel(
    workbook_path, 
    sheet_name=sheet_name, 
    usecols=[0, 1, 2],  # Colunas A, B, C
    names=['item', 'valor', 'outros'],
    header=None,
    skiprows=15  # Pula as primeiras 14 linhas
)

# Converter colunas numéricas para float (REAL no SQLite)
def convert_to_float(x):
    try:
        return float(str(x).replace(',', '.'))
    except (ValueError, TypeError):
        return x

df_quadro_area_03['valor'] = df_quadro_area_03['valor'].apply(convert_to_float)
df_quadro_area_03['outros'] = df_quadro_area_03['outros'].apply(convert_to_float)

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Definir os tipos das colunas para o SQLite
dtype = {
    'item': 'TEXT',
    'valor': 'REAL',
    'outros': 'REAL'
}

# Criar a tabela no banco de dados com os tipos específicos
df_quadro_area_03.to_sql('quadro_area_03', conn, if_exists='replace', index=False, dtype=dtype)

# Exibir todos os dados
print("\nDados carregados:")
print(df_quadro_area_03)

# Fechar conexão
conn.close()

print("\nTabela `quadro_area_03` criada e populada com sucesso.")