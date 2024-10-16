import pandas as pd
import sqlite3
import re
import time 

tick = time.time()

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('./data/base_cris_desagregado.db')

# Ler a tabela 'unidades' em um DataFrame do pandas
df = pd.read_sql_query("SELECT * FROM unidades", conn)

# Fechar a conexão com o banco de dados
conn.close()

# Converter colunas numéricas para o tipo float (caso não estejam)
colunas_numericas = [
    'fracao_ideal_condominio',
    'cota_terreno',
    'area_total_global_coberta_e_descoberta',
    'area_privativa',
    'area_comum',
    'area_comum_descoberta_recreacao',
    'area_privativa_vinculada_deposito'
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

# 1. Soma de 'fracao_ideal_condominio' e verificação se é igual a 1
soma_fracao = df['fracao_ideal_condominio'].sum()
print(f"\n1. Soma de 'fracao_ideal_condominio': {soma_fracao}")

if abs(soma_fracao - 1) < 1e-6:
    print("-> A soma de 'fracao_ideal_condominio' é igual a 1.")
else:
    print("-> A soma de 'fracao_ideal_condominio' NÃO é igual a 1.")

# 2. Soma de 'cota_terreno_condominio'
soma_cota_terreno = df['cota_terreno'].sum()
print(f"\n2. Soma de 'cota_terreno': {soma_cota_terreno}")

# 3. Verificar se existem 'unidade' duplicadas
duplicated_units = df[df.duplicated(subset='unidades', keep=False)]
if not duplicated_units.empty:
    print("\n3. Existem unidades duplicadas:")
    print(duplicated_units[['unidades']].drop_duplicates().to_string(index=False))
else:
    print("\n3. Não existem unidades duplicadas.")


# 4. Verificar se, para cada unidade, a soma das áreas é igual
def verificar_areas(row):
    total_area_calculada = (
        row['area_privativa'] +
        row['area_comum'] +
        row['area_comum_descoberta_recreacao'] +
        row['area_privativa_vinculada_deposito']
    )
    return abs(row['area_total_global_coberta_e_descoberta'] - total_area_calculada) < 1e-6

df['areas_correspondem'] = df.apply(verificar_areas, axis=1)

areas_incorretas = df[df['areas_correspondem'] == False]

if not areas_incorretas.empty:
    print("\n4. As seguintes unidades têm discrepâncias nas áreas:")
    print(areas_incorretas[['unidades', 'area_total_global_coberta_e_descoberta', 'area_privativa', 'area_comum', 'area_comum_descoberta_recreacao', 'area_privativa_vinculada_deposito']].to_string(index=False))
else:
    print("\n4. Para todas as unidades, a soma das áreas privativas e comuns corresponde à área global construída (conbertas e descobertas).")


# Abra um arquivo para escrever o relatório
with open('./producao_minima/relatorio.txt', 'w') as f:
    # Redirecione as saídas para o arquivo
    f.write(f"\n1. Soma de 'fracao_ideal_condominio': {soma_fracao}\n")
    if abs(soma_fracao - 1) < 1e-6:
        f.write("-> A soma de 'fracao_ideal_condominio' é igual a 1.\n")
    else:
        f.write("-> A soma de 'fracao_ideal_condominio' NÃO é igual a 1.\n")

    f.write(f"\n2. Soma de 'cota_terreno': {soma_cota_terreno}\n")

    if not duplicated_units.empty:
        f.write("\n3. Existem unidades duplicadas:\n")
        f.write(duplicated_units[['unidades']].drop_duplicates().to_string(index=False))
        f.write("\n")
    else:
        f.write("\n3. Não existem unidades duplicadas.\n")

    if not areas_incorretas.empty:
        f.write("\n4. As seguintes unidades têm discrepâncias nas áreas:\n")
        f.write(areas_incorretas[['unidades', 'area_total_global_coberta_e_descoberta', 'area_privativa', 'area_comum', 'area_privativa_vinculada_deposito']].to_string(index=False))
        f.write("\n")
    else:
        f.write("\n4. Para todas as unidades, a soma das áreas corresponde à área total construída.\n")

print("Relatório salvo em 'relatorio.txt'.")

tack = time.time()
execution_time = tack - tick
print(f"Tempo total de execução: {execution_time:.2f} segundos.")
