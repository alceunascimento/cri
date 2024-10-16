import xml.etree.ElementTree as ET
import pandas as pd
import sys

# Redirecionar a saída para um arquivo de log
log_file = 'log_leitura_xml.txt'
sys.stdout = open(log_file, 'w')

# Carregar o XML
file_path = 'base_real_assinado.xml'
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
    dataframes[table_name] = df

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

# Exibir os nomes das tabelas carregadas
for table_name, dataframe in dataframes.items():
    print(f"Tabela: {table_name}")
    print(dataframe.head())
    print("\n")

# Fechar o arquivo de log
sys.stdout.close()