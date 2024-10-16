import pandas as pd
import re
import sqlite3

# Conectar ao banco de dados SQLite
db_path = './cri/base_cri.db'
conn = sqlite3.connect(db_path)

try:
    # Obter o cursor para executar comandos SQL
    cursor = conn.cursor()

    # Obter os nomes de todas as tabelas no banco de dados
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [row[0] for row in cursor.fetchall()]

    # Dicionário para armazenar os nomes das tabelas e suas respectivas variáveis (colunas)
    tables_info = {}

    # Iterar sobre as tabelas para obter os nomes das variáveis (colunas)
    for table_name in table_names:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in cursor.fetchall()]
        tables_info[table_name] = columns

finally:
    # Fechar a conexão com o banco de dados
    conn.close()

# Criar um DataFrame a partir das informações das tabelas
tables_info_list = []
for table_name, columns in tables_info.items():
    for column in columns:
        tables_info_list.append({'Tabela': table_name, 'Variável': column})

df_tables_info = pd.DataFrame(tables_info_list)

# Salvar as informações em um arquivo Excel
output_file = './cri/informacoes_tabelas.xlsx'
df_tables_info.to_excel(output_file, index=False)

print(f"Informações das tabelas salvas no arquivo '{output_file}' com sucesso.")


# Carregar o arquivo Excel com as informações das tabelas
df = pd.read_excel('./cri/informacoes_tabelas.xlsx')

# Verificar se a coluna 'nome_variavel' existe
if 'Variável' not in df.columns:
    raise KeyError("A coluna 'Variável' não foi encontrada no arquivo Excel.")

# Função para ajustar o nome das variáveis
def ajustar_nome_variavel(nome):
    # Substituir underscores por espaços e converter o texto para minúsculo
    nome_ajustado = nome.replace('_', ' ').lower()
    # Colocar a primeira letra de cada palavra em maiúsculo
    nome_ajustado = re.sub(r'\b(\w)', lambda m: m.group(1).upper(), nome_ajustado)
    return nome_ajustado

# Aplicar a função para ajustar os nomes das variáveis e criar uma nova coluna 'para'
df['para'] = df['Variável'].apply(ajustar_nome_variavel)

# Salvar o arquivo Excel com a nova coluna 'para'
df.to_excel('./cri/informacoes_tabelas_ajustadas.xlsx', index=False)