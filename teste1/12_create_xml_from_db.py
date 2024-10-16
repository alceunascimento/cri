import sqlite3
import xml.etree.ElementTree as ET

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('base_real.db')
cursor = conn.cursor()

# Criar o elemento raiz do XML
root = ET.Element('RegistroImoveis')

# Adicionar o cabeçalho ao XML
header = ET.SubElement(root, 'Header')
ET.SubElement(header, 'Titulo').text = 'INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS'
ET.SubElement(header, 'Matricula').text = '00.000'
ET.SubElement(header, 'ServicoRegistroImoveis').text = '1'

# Listar todas as tabelas no banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

# Iterar por cada tabela e adicioná-las ao XML
for table_name in tables:
    table_name = table_name[0]
    table_element = ET.SubElement(root, 'Tabela', nome=table_name)

    # Obter todos os registros da tabela atual
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    # Iterar por cada linha e adicionar ao XML
    for row in rows:
        row_element = ET.SubElement(table_element, 'Registro')
        for col_name, col_value in zip(columns, row):
            col_element = ET.SubElement(row_element, col_name)
            col_element.text = str(col_value) if col_value is not None else ''

# Fechar a conexão com o banco de dados
conn.close()

# Converter o ElementTree em uma string e salvar em um arquivo XML
tree = ET.ElementTree(root)
tree.write('base_real.xml', encoding='utf-8', xml_declaration=True)

print("Arquivo XML gerado com sucesso: base_real.xml")