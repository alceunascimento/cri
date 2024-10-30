import pandas as pd
import sqlite3

# Carregar a aba `quadro_area_04A` da pasta de trabalho
workbook_path = './pre_cri/data/base_real_ajustada.xlsx'
sheet_name = 'quadro_area_04A'

# Ler as variáveis a partir da linha 3 e as colunas a partir da 5 (índice começa em 0, então a coluna 5 é a 4)
df_quadro_area_04A = pd.read_excel(workbook_path, sheet_name=sheet_name, header=13, usecols=lambda x: 'Unnamed' not in x)

# Renomear as colunas conforme especificado
column_names = [
    'subcondominio',
    'unidade_tipo',
    'area_unidade_equivalente_custo_padrao',
    'custo',
    'fracao_ideal_solo_condominio',
    'coeficiente_proporcionalidade_unidades_suportam_custo_construcao',
    'coeficiente_raterio_construcao_total_rerrateio_incorpora_unidades_pagamento_terreno',
    'area_equivalente_area_custo_padrao_total_rerrateio_areas_equivalentes_custo_propria_subrogada',
    'custo_construcao_total_rerrateio_custo',
    'custo_subrogacao_unidade',
    'area_unidade_real',
    'quota_area_real_dada_pagamento_terreno',
    'unidade_quantidade_total',
    'unidade_quantidade_subrogadas',
    'unidade_quantidade_diferenca'
]
df_quadro_area_04A.columns = column_names

# Lista de colunas que contêm custos e precisam ter 2 casas decimais
colunas_custo = ['custo', 'custo_construcao_total_rerrateio_custo', 'custo_subrogacao_unidade']

# Formatar colunas de custo para terem 2 casas decimais usando round()
for coluna in colunas_custo:
    df_quadro_area_04A[coluna] = df_quadro_area_04A[coluna].round(2)

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Definir tipos de colunas para o SQLite
dtype_mapping = {}
for coluna in df_quadro_area_04A.columns:
    if coluna in colunas_custo:
        dtype_mapping[coluna] = 'REAL'  # Usando REAL para números decimais no SQLite

# Criar a tabela `quadro_area_04A` no banco de dados
df_quadro_area_04A.to_sql(
    'quadro_area_04A',
    conn,
    if_exists='replace',
    index=False,
    dtype=dtype_mapping
)

# Fechar conexão
conn.close()

print("Tabela `quadro_area_04A` criada e populada com sucesso.")