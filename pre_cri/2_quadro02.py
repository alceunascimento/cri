import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_02` da pasta de trabalho
workbook_path = './pre_cri/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_02'

# Ler as variáveis a partir da linha 5 e as colunas a partir da 7 (índice começa em 0, então a coluna 7 é a 6)
df_quadro_area_02 = pd.read_excel(workbook_path, sheet_name=sheet_name, header=4, usecols=lambda x: 'Unnamed' not in x)

# Renomear as colunas conforme especificado
column_names = [
    'subcondominio',
    'unidade_tipo',
    'area_divisao_nao_prorcional_privativa_coberta_padrao',
    'area_divisao_nao_prorcional_privativa_descoberta_real',
    'area_divisao_nao_prorcional_privativa_descoberta_equivalente',
    'area_divisao_nao_prorcional_privativa_totais_real',
    'area_divisao_nao_prorcional_privativa_totais_equivalente_custo_padrao',
    'area_divisao_nao_proporcional_comum_coberta_padrao',
    'area_divisao_nao_proporcional_comum_descoberta_real',
    'area_divisao_nao_proporcional_comum_descoberta_equivalente',
    'area_divisao_nao_proporcional_comum_totais_real',
    'area_divisao_nao_proporcional_comum_totais_equivalente_custo_padrao',
    'area_total_equivalente_area_custo_padrao',
    'fracao_ideal_solo_condominio',
    'area_divisao_proporcional_comum_coberta_padrao',
    'area_divisao_proporcional_comum_descoberta_real',
    'area_divisao_proporcional_comum_descoberta_equivalente',
    'area_divisao_proporcional_comum_totais_real',
    'area_divisao_proporcional_comum_totais_equivalente_custo_padrao',
    'area_unidade_real',
    'area_unidade_equivalente_custo_padrao',
    'unidade_quantidades'
]
df_quadro_area_02.columns = column_names

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Criar a tabela `quadro_area_02` no banco de dados
df_quadro_area_02.to_sql('quadro_area_02', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_02` criada e populada com sucesso.")