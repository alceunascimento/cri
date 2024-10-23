import sqlite3
import xml.etree.ElementTree as ET

# Ler o arquivo XML e criar um novo banco de dados SQLite
# Etapa 1: Carregar o XML, identificar a tabela 'cri' e gerar o banco de dados 'base_real_cri.db'

tree = ET.parse('./pre_cri/base_real.xml')
root = tree.getroot()

# Identificar os campos da tabela 'cri' no XML
for tabela in root.findall("Tabela"):
    if tabela.attrib.get("nome") == "cri":  # Verificar se a tabela é a desejada
        registro = tabela.find('Registro')
        if registro is not None:
            # Obter todos os nomes dos campos presentes no primeiro registro encontrado
            colunas = [campo.tag for campo in registro]
            break

# Conectar ao novo banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real_cri.db')
cursor = conn.cursor()

# Criar a tabela 'cri' dinamicamente com base nos campos identificados
colunas_sql = [f"{coluna} TEXT" for coluna in colunas]
colunas_sql_str = ', '.join(colunas_sql)

cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS cri (
        {colunas_sql_str}
    )
''')

# Inserir os dados do XML no banco de dados
for tabela in root.findall("Tabela"):
    if tabela.attrib.get("nome") == "cri":  # Verificar se a tabela é a desejada
        for registro in tabela.findall('Registro'):
            valores = [campo.text for campo in registro]
            placeholders = ', '.join(['?'] * len(valores))
            cursor.execute(f'''
                INSERT INTO cri ({', '.join(colunas)})
                VALUES ({placeholders})
            ''', valores)
            print(f"Inserido: Unidade {registro.find('unidade_numero').text}")

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados 'base_real_cri.db' criado e populado com sucesso.")



import sqlite3

# Conectar ao banco de dados SQLite existente
conn = sqlite3.connect('./pre_cri/base_real_cri.db')
cursor = conn.cursor()

# Selecionar os dados relevantes da tabela 'cri'
cursor.execute("SELECT * FROM cri")
rows = cursor.fetchall()
colunas = [col[0] for col in cursor.description]
dados = [dict(zip(colunas, row)) for row in rows]

# Função para gerar o texto do memorial descritivo com base nos dados do banco de dados
def gerar_memorial_descritivo(row):
    memorial = ""
    subcondominio = row.get('subcondominio', '').upper()
    especie_unidade = row.get('especie_unidade', '').upper()
    unidade_numero = row.get('unidade_numero', '')
    try:
        area_total_construida = float(row.get('area_total_construida', 0))
        area_privativa = float(row.get('area_privativa', 0))
        area_comum = float(row.get('area_comum', 0))
        fracao_ideal_solo_condominio = float(row.get('fracao_ideal_solo_condominio', 0))
        quota_terreno = float(row.get('quota_terreno_condominio', 0))
    except ValueError:
        area_total_construida = 0.0
        area_privativa = 0.0
        area_comum = 0.0
        fracao_ideal_solo_condominio = 0.0
        quota_terreno = 0.0
    
    pavimento = row.get('pavimento', '')
    confrontacao_frente = row.get('confrontacao_frente', '')
    confrontacao_direita = row.get('confrontacao_direita', '')
    confrontacao_esquerda = row.get('confrontacao_esquerda', '')
    confrontacao_fundo = row.get('confrontacao_fundos', '')
    tipo_vaga = row.get('tipo_vaga', '')
    tipo_vaga = tipo_vaga.lower() if tipo_vaga else ''
    deposito_vinculado = row.get('tipo_garagem_vinculada', None)
    deposito_numero = row.get('localizacao_garagem_vinculada', '')

    if subcondominio == 'RESIDENCIAL':
        memorial = (
            f"{especie_unidade} {unidade_numero}: "
            f"Subcondomínio: {subcondominio}. "
            f"Áreas construídas: "
            f"área construída de {area_total_construida:.2f} metros quadrados, "
            f"sendo a área privativa de {area_privativa:.2f} metros quadrados "
            f"e a área comum de {area_comum:.2f} metros quadrados. "
            f"Fração ideal de solo e partes comuns: {fracao_ideal_solo_condominio:.8f}; "
            f"Quota de terreno: {quota_terreno:.8f} metros quadrados. "
            f"Localização: {pavimento}, sendo que para quem entra na unidade, "
            f"confronta pela frente com {confrontacao_frente}, "
            f"pelo lado direito com {confrontacao_direita}, "
            f"pelo lado esquerdo com {confrontacao_esquerda} "
            f"e pelo fundo com {confrontacao_fundo}."
        )
    elif subcondominio == 'GALERIA':
        memorial = (
            f"{especie_unidade} {unidade_numero}: "
            f"Subcondomínio: {subcondominio}. "
            f"Áreas construídas: "
            f"área construída de {area_total_construida:.2f} metros quadrados, "
            f"sendo a área privativa de {area_privativa:.2f} metros quadrados "
            f"e a área comum de {area_comum:.2f} metros quadrados. "
            f"Fração ideal de solo e partes comuns: {fracao_ideal_solo_condominio:.8f}; "
            f"Quota de terreno: {quota_terreno:.8f} metros quadrados. "
            f"Localização: {pavimento}, sendo que para quem entra na unidade, "
            f"confronta pela frente com {confrontacao_frente}, "
            f"pelo lado direito com {confrontacao_direita}, "
            f"pelo lado esquerdo com {confrontacao_esquerda} "
            f"e pelo fundo com {confrontacao_fundo}."
        )
    elif subcondominio == 'ESTACIONAMENTO':
        tipo_vaga_str = "01 (simples)" if tipo_vaga == 'simples' else "02 (dupla)"
        memorial = (
            f"{especie_unidade} {unidade_numero}: "
            f"Subcondomínio: {subcondominio}. "
            f"Capacidade e uso: {tipo_vaga_str} veículo(s) de passeio, de pequeno e médio porte e uso residencial. "
            f"Áreas construídas: "
            f"área construída de {area_total_construida:.2f} metros quadrados, "
            f"sendo a área privativa de {area_privativa:.2f} metros quadrados "
            f"e a área comum de {area_comum:.2f} metros quadrados. "
            f"Fração ideal de solo e partes comuns: {fracao_ideal_solo_condominio:.8f}; "
            f"Quota de terreno: {quota_terreno:.8f} metros quadrados. "
            f"Localização: {pavimento}, sendo que para quem entra na unidade, "
            f"confronta pela frente com {confrontacao_frente}, "
            f"pelo lado direito com {confrontacao_direita}, "
            f"pelo lado esquerdo com {confrontacao_esquerda} "
            f"e pelo fundo com {confrontacao_fundo}."
        )
        if deposito_vinculado:
            memorial += f" Depósito vinculado: {deposito_numero} com {area_privativa:.2f} metros quadrados."
    
    return memorial

# Gerar o memorial descritivo para cada unidade
memoriais = [gerar_memorial_descritivo(row) for row in dados]

# Salvar o memorial descritivo em um arquivo de texto
with open('./pre_cri/memorial.md', 'w', encoding='utf-8') as f:
    for memorial in memoriais:
        f.write(memorial + "\n")

print("Memorial descritivo gerado com sucesso e salvo em 'memorial.md'.")

# Fechar a conexão com o banco de dados
conn.close()
