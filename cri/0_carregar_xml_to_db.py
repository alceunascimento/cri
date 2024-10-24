import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import sys

# Redirecionar a saída para um arquivo de log
log_file = './cri/log_leitura_xml.txt'
sys.stdout = open(log_file, 'w')

# Carregar o XML
file_path = './cri/base_real.xml'
tree = ET.parse(file_path)
root = tree.getroot()

# Dicionário para armazenar os DataFrames
dataframes = {}

# Lista para armazenar os nomes das tabelas encontradas
table_names = []

# Iterar sobre os elementos do XML e identificar as tabelas
for table in root.findall('.//Tabela'):
    table_name = table.get('nome') if table.get('nome') else table.tag  # Usar o atributo 'nome' ou a tag como nome da tabela
    table_names.append(table_name)
    rows = []
    columns = []
    
    # Iterar sobre as linhas da tabela
    for row in table.findall('.//Registro'):
        row_data = {}
        # Iterar sobre as colunas da linha
        for col in row:
            if col.tag not in columns:
                columns.append(col.tag)
            row_data[col.tag] = col.text
        rows.append(row_data)
    
    # Criar um DataFrame a partir das linhas e colunas extraídas
    df = pd.DataFrame(rows, columns=columns)

    # Tentar converter as colunas para tipos numéricos quando possível
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            print(f"Coluna '{col}' não foi convertida para numérico devido a valores incompatíveis.")
    
    dataframes[table_name] = df

# Criar um banco de dados SQLite e conectar a ele
db_path = './cri/base_cri.db'
conn = sqlite3.connect(db_path)

# Verificar quantas tabelas foram encontradas no XML
print(f"Número de tabelas encontradas no XML: {len(table_names)}")
print("Nomes das tabelas encontradas:")
for name in table_names:
    print(f"- {name}")

# Verificar quantos DataFrames foram criados
print(f"Número de DataFrames criados: {len(dataframes)}")
print("Nomes dos DataFrames criados e número de linhas em cada um:")
for table_name, dataframe in dataframes.items():
    print(f"- Tabela: {table_name}, Número de linhas: {len(dataframe)}")

# Inserir os DataFrames no banco de dados SQLite
for table_name, dataframe in dataframes.items():
    dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"Tabela '{table_name}' inserida no banco de dados SQLite com sucesso.")


# Fechar a conexão com o banco de dados
conn.close()


# Fechar o arquivo de log
sys.stdout.close()