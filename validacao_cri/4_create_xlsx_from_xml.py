import xml.etree.ElementTree as ET
import pandas as pd

# Função para verificar e converter os valores para números, se possível
def converter_valor(valor):
    try:
        # Tenta converter para float
        return float(valor)
    except ValueError:
        # Se a conversão falhar, retorna o valor original (texto)
        return valor

# Carregar o arquivo XML
tree = ET.parse('./producao_minima/tabela_cri.xml')
root = tree.getroot()

# Listar os dados extraídos do XML
data = []
columns = []

# Iterar sobre cada registro no XML
for tabela in root.findall('.//tabela'):
    for registro in tabela.findall('registro'):
        row_data = {}
        for child in registro:
            # Adicionar o nome do campo e o valor correspondente
            if child.tag not in columns:
                columns.append(child.tag)
            # Converter o valor para número, se aplicável
            row_data[child.tag] = converter_valor(child.text)
        data.append(row_data)

# Criar DataFrame com os dados extraídos
df = pd.DataFrame(data, columns=columns)

# Salvar em uma planilha Excel
df.to_excel('./producao_minima/saida_tabela_cri.xlsx', index=False)

print("XML convertido para Excel com sucesso.")
