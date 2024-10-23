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

# Ordenar os dados pelo campo 'unidade_numero'
dados_ordenados = sorted(dados, key=lambda x: int(''.join(filter(str.isdigit, x.get('unidade_numero', '0')))))

# Gerar o memorial descritivo para cada unidade
memoriais = [gerar_memorial_descritivo(row) for row in dados_ordenados]

# Contar quantas unidades foram geradas por subcondomínio
count_residencial = sum(1 for memorial in memoriais if 'RESIDENCIAL' in memorial)
count_galeria = sum(1 for memorial in memoriais if 'GALERIA' in memorial)
count_estacionamento = sum(1 for memorial in memoriais if 'ESTACIONAMENTO' in memorial)

print(f"Total de unidades RESIDENCIAL incluídas: {count_residencial}")
print(f"Total de unidades GALERIA incluídas: {count_galeria}")
print(f"Total de unidades ESTACIONAMENTO incluídas: {count_estacionamento}")



# Estruturar o markdown conforme solicitado
markdown_content = f"""
---
title: "Memorial Descritivo"
subtitle: "em atendimento ao art. 32, alínea i, da Lei nº 4.591/64"
---

# DADOS GERAIS
## Incorporador
{dados[0].get('incorporador', 'N/A')}

## Responsável técnico pela construção
{dados[0].get('responsavel_tecnico_construcao', 'N/A')}

## Responsável técnico pelo cálculo áreas NBR 12.721
{dados[0].get('responsavel_tecnico_nbr', 'N/A')}

## Matrícula
{dados[0].get('matricula', 'N/A')}

## Edificio
{dados[0].get('edificio', 'N/A')}

## Acesso ao edificio
{dados[0].get('acesso_edificio', 'N/A')}


# PARTES DE PROPRIEDADE EXCLUSIVA
## SUBCONDOMINIO RESIDENCIAL
"""

# Adicionar memoriais do subcondomínio residencial
markdown_content += "\n\n".join([memorial for memorial in memoriais if "RESIDENCIAL" in memorial]) + "\n"


markdown_content += """
## SUBCONDOMINIO GALERIA
"""

# Adicionar memoriais do subcondomínio galeria
markdown_content += "\n\n".join([memorial for memorial in memoriais if "GALERIA" in memorial]) + "\n"

markdown_content += """
## SUBCONDOMINIO ESTACIONAMENTO
"""

# Adicionar memoriais do subcondomínio estacionamento
markdown_content += "\n\n".join([memorial for memorial in memoriais if "ESTACIONAMENTO" in memorial]) + "\n"






# Inserir variáveis da tabela 'cri'
partes_comuns_base = dados[0].get('partes_comuns_base', 'N/A')
partes_comuns_geral = dados[0].get('partes_comuns_geral', 'N/A')
partes_comuns_residencial = dados[0].get('partes_comuns_residencial', 'N/A')
partes_comuns_estacionamento = dados[0].get('partes_comuns_estacionamento', 'N/A')
partes_comuns_residencial_estacionamento = dados[0].get('partes_comuns_residencial_estacionamento', 'N/A')
partes_comuns_galeria = dados[0].get('partes_comuns_galeria', 'N/A')
localizacao_residencial = dados[0].get('localizacao_residencial', 'N/A')
localizacao_galeria = dados[0].get('localizacao_galeria', 'N/A')
localizacao_estacionamento = dados[0].get('localizacao_estacionamento', 'N/A')
tipos_residencial = dados[0].get('tipos_residencial', 'N/A')
tipos_galeria = dados[0].get('tipos_galeria', 'N/A')
tipos_estacionamento = dados[0].get('tipos_estacionamento', 'N/A')


markdown_content += f"""
# PARTES COMUNS
{partes_comuns_base}

## CONDOMINIO GERAL
{partes_comuns_geral}

## SUBCONDOMINIO RESIDENCIAL
{partes_comuns_residencial}

## SUBCONDOMINIO ESTACIONAMENTO
{partes_comuns_estacionamento}

## SUBCONDOMINIO RESIDENCIAL E ESTACIONAMENTO
{partes_comuns_residencial_estacionamento}

## SUBCONDOMINIO GALERIA
{partes_comuns_galeria}
"""

markdown_content += f"""
# LOCALIZAÇÃO DAS UNIDADES AUTÔNMAS
## SUBCONDOMINIO RESIDENCIAL
{localizacao_residencial}

## SUBCONDOMINIO ESTACIONAMENTO
{localizacao_estacionamento}

## SUBCONDOMINIO GALERIA
{localizacao_galeria}
"""

markdown_content += f"""
# TIPOLOGIA DAS UNIDADES AUTÔNMAS
## SUBCONDOMINIO RESIDENCIAL
{tipos_residencial}

## SUBCONDOMINIO ESTACIONAMENTO
{tipos_estacionamento}

## SUBCONDOMINIO GALERIA
{tipos_galeria}
"""




# Salvar o memorial descritivo em um arquivo de texto
with open('./pre_cri/memorial.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)

print("Memorial descritivo estruturado e salvo em 'memorial.md'.")

# Fechar a conexão com o banco de dados
conn.close()
