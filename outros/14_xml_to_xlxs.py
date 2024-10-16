import pandas as pd
import xml.etree.ElementTree as ET

# Carregar o arquivo XML
tree = ET.parse('base_real.xml')
root = tree.getroot()

# Criar um dicionário para armazenar os DataFrames
tables_data = {}

# Iterar por cada tabela no XML e carregar os registros em DataFrames
for table_element in root.findall('Tabela'):
    table_name = table_element.get('nome')
    records = []
    columns = []

    # Iterar pelos registros e coletar os dados
    for record_element in table_element.findall('Registro'):
        record = {}
        for field in record_element:
            record[field.tag] = field.text
            if field.tag not in columns:
                columns.append(field.tag)
        records.append(record)

    # Criar um DataFrame com os dados coletados
    df = pd.DataFrame(records, columns=columns)
    tables_data[table_name] = df

# Criar um arquivo Excel contendo todas as tabelas, cada uma em uma aba separada
with pd.ExcelWriter('base_real_from_xml.xlsx') as writer:
    for table_name, df in tables_data.items():
        # Converter colunas numéricas para o tipo adequado
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except ValueError:
                pass
        df.to_excel(writer, sheet_name=table_name, index=False)

print("Arquivo Excel gerado com sucesso: base_real_from_xml.xlsx")