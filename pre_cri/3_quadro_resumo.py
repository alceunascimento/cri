import pandas as pd
import sqlite3
import re

# Caminho para o arquivo Excel
workbook_path = './pre_cri/base_real_ajustada.xlsx'
sheet_name = 'quadro_resumo'

# Função para desagregar as unidades em uma lista de números ou strings
def desagregar_unidades(texto):
    unidades = []
    # Encontrar todas as sequências de números ou intervalos
    grupos = re.findall(r'\d+(?:/\d+)?(?: a \d+)?', texto)
    for grupo in grupos:
        # Verificar se há barra e manter o número completo como string
        if '/' in grupo:
            unidades.append(grupo)
        elif ' a ' in grupo:
            inicio, fim = map(int, grupo.split(' a '))
            unidades.extend(range(inicio, fim + 1))
        else:
            unidades.append(int(grupo))
    return unidades

# Ler a aba "quadro_resumo" do arquivo Excel
df = pd.read_excel(workbook_path, sheet_name=sheet_name, header=5)

# Renomear as colunas conforme especificado
column_names = [
    'subcondominio',
    'unidade_tipo',
    'unidade_quantidade',
    'area_alvara_privativa',
    'area_alvara_deposito_vinculado',
    'area_alvara_comum',
    'area_alvara_total',
    'fracao_ideal_solo_subcondominio',
    'area_comum_descoberta',
    'area_total',
    'fracao_ideal_solo_condominio',
    'quota_terreno',
    'numeros_unidades'
]
df.columns = column_names

# Para cada linha do DataFrame, desagregar as unidades
linhas_expandidas = []
for idx, row in df.iterrows():
    unidades = desagregar_unidades(row['numeros_unidades'])
    for unidade in unidades:
        nova_linha = row.copy()
        nova_linha['numeros_unidades'] = unidade
        linhas_expandidas.append(nova_linha)

# Criar um novo DataFrame com as linhas expandidas
df_expanded = pd.DataFrame(linhas_expandidas)

# Converter os nomes das colunas para snake_case
df_expanded.columns = [
    'subcondominio',
    'unidade_tipo',
    'unidade_quantidade',
    'area_alvara_privativa',
    'area_alvara_deposito_vinculado',
    'area_alvara_comum',
    'area_alvara_total',
    'fracao_ideal_solo_subcondominio',
    'area_comum_descoberta',
    'area_total',
    'fracao_ideal_solo_condominio',
    'quota_terreno',
    'unidade_numero'
]

# Reorganizar colunas para que 'unidade_numero' seja a segunda coluna
unidade_numero_col = df_expanded.pop('unidade_numero')
df_expanded.insert(1, 'unidade_numero', unidade_numero_col)

# Validação dos dados: verificar se as quantidades de 'unidade_tipo' correspondem ao número de linhas
for unidade_tipo, grupo in df_expanded.groupby('unidade_tipo'):
    quantidade_esperada = df.loc[df['unidade_tipo'] == unidade_tipo, 'unidade_quantidade'].iloc[0]
    quantidade_real = len(grupo)
    if quantidade_esperada != quantidade_real:
        raise ValueError(f"Erro de validação: {unidade_tipo} deveria ter {quantidade_esperada} unidades, mas tem {quantidade_real} unidades.")

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Criar a tabela `quadro_resumo` no banco de dados
df_expanded.to_sql('quadro_resumo', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `quadro_resumo` criada e populada com sucesso.")