import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_05` da pasta de trabalho
workbook_path = './data/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_05'

# Ler as variáveis a partir da linha 2 (índice começa em 0, então a linha 2 é a de índice 1)
df_quadro_area_05 = pd.read_excel(workbook_path, sheet_name=sheet_name, header=1)

# Renomear as colunas conforme especificado
column_names = [
    'edificacao_tipo',
    'edificacao_pavimento',
    'edificacao_quantidade_unidades_por_pavimentos',
    'edificacao_indicacao_unidades_por_pavimento',
    'edificacao_descricao_pavimentos',
    'alvara_construcao_data_emissao',
    'edificacao_blocos',
    'edificacao_quantidade_unidades_por_subcondominio'
]
df_quadro_area_05.columns = column_names

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')

# Criar a tabela `quadro_area_05` no banco de dados
df_quadro_area_05.to_sql('quadro_area_05', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_05` criada e populada com sucesso.")
