import sqlite3
import re

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')
cursor = conn.cursor()

# APURAÇÃO PARA VAGAS


# Apura a quantidade total de unidades autônomas da espécie "VAGA"
query_total_vagas = """
SELECT COUNT(*)
FROM cri
WHERE especie_unidade = 'VAGA';
"""
cursor.execute(query_total_vagas)
total_vagas = cursor.fetchone()[0]

# Apura a quantidade total de vagas simples e duplas
query_tipo_vagas = """
SELECT tipo_vaga, COUNT(*)
FROM cri
WHERE especie_unidade = 'VAGA'
GROUP BY tipo_vaga;
"""
cursor.execute(query_tipo_vagas)
tipo_vagas = cursor.fetchall()

# Apura a quantidade de vagas por pavimento
query_vagas_por_pavimento = """
SELECT pavimento, COUNT(*)
FROM cri
WHERE especie_unidade = 'VAGA'
GROUP BY pavimento
ORDER BY pavimento;
"""
cursor.execute(query_vagas_por_pavimento)
vagas_por_pavimento = cursor.fetchall()

# Apura os números de vagas simples e duplas por pavimento
query_detalhe_vagas_por_pavimento = """
SELECT pavimento, unidade_numero, tipo_vaga
FROM cri
WHERE especie_unidade = 'VAGA'
ORDER BY pavimento, unidade_numero;
"""
cursor.execute(query_detalhe_vagas_por_pavimento)
vagas = cursor.fetchall()

# Organiza os dados em um dicionário agrupado por pavimento
vagas_dict = {}
pavimentos_com_vagas = set()  # Conjunto para armazenar os pavimentos com vagas
for vaga in vagas:
    pavimento = vaga[0]
    unidade_numero = vaga[1]
    tipo_vaga = vaga[2]  # 'simples' ou 'dupla'
    
    if pavimento not in vagas_dict:
        vagas_dict[pavimento] = {
            'simples': [],
            'duplas': []
        }
    
    if tipo_vaga == 'simples':
        vagas_dict[pavimento]['simples'].append(unidade_numero)
    else:
        vagas_dict[pavimento]['duplas'].append(unidade_numero)
    
    pavimentos_com_vagas.add(pavimento)

# Função auxiliar para formatar a lista de vagas
def formatar_vagas(vagas):
    return ', '.join(map(str, vagas))

# Função para formatar a lista de pavimentos
def formatar_pavimentos(pavimentos):
    return ', '.join(sorted(pavimentos))

# Monta o texto inicial com os pavimentos identificados dinamicamente
pavimentos_formatados = formatar_pavimentos(pavimentos_com_vagas)
texto_vagas = f"As vagas localizam-se nos {pavimentos_formatados}, num total de {total_vagas} unidades autônomas, "

# Variáveis para armazenar a contagem de vagas simples e duplas
vagas_simples_total = vagas_duplas_total = 0

# Monta o texto com a quantidade total de vagas simples e duplas
for tipo_vaga, count in tipo_vagas:
    if tipo_vaga == 'simples':
        vagas_simples_total = count
    elif tipo_vaga == 'dupla':
        vagas_duplas_total = count

# Concatena a contagem de vagas simples e duplas na ordem correta
texto_vagas += f"sendo {vagas_simples_total} vagas simples e {vagas_duplas_total} vagas duplas.\n"

# Itera pelos pavimentos e concatena as informações de vagas
for pavimento, total_vagas_subsolo in vagas_por_pavimento:
    vagas_simples = formatar_vagas(vagas_dict[pavimento]['simples'])
    vagas_duplas = formatar_vagas(vagas_dict[pavimento]['duplas'])
    
    texto_subsolo = f"No {pavimento} serão {total_vagas_subsolo} vagas autônomas de nº {vagas_simples} (vagas simples) e "
    
    if vagas_duplas:
        texto_subsolo += f"{vagas_duplas} (vagas duplas)"
    
    texto_subsolo += ".\n"
    
    # Adiciona o texto do subsolo ao texto final
    texto_vagas += texto_subsolo

# APURAÇÃO PARA APARTAMENTOS


# Função auxiliar para extrair o número do pavimento
def extrair_numero_pavimento(pavimento_str):
    match = re.match(r"(\d+)", pavimento_str)
    return int(match.group(1)) if match else float('inf')  # Retorna o número ou um valor infinito para evitar erro

# Função auxiliar para formatar a lista de unidades
def formatar_unidades(unidades):
    return ', '.join(map(str, unidades))


# Apura a quantidade total de unidades autônomas da espécie "APARTAMENTO"
query_total_apartamentos = """
SELECT COUNT(*)
FROM cri
WHERE especie_unidade = 'APARTAMENTO';
"""
cursor.execute(query_total_apartamentos)
total_apartamentos = cursor.fetchone()[0]

# Apura a localização dos apartamentos por pavimento
query_apartamentos_por_pavimento = """
SELECT pavimento, unidade_numero
FROM cri
WHERE especie_unidade = 'APARTAMENTO'
ORDER BY pavimento, unidade_numero;
"""
cursor.execute(query_apartamentos_por_pavimento)
apartamentos = cursor.fetchall()

# Organiza os dados em um dicionário agrupado por pavimento para os apartamentos
apartamentos_dict = {}
pavimentos_com_apartamentos = set()  # Conjunto para armazenar os pavimentos com apartamentos
for apartamento in apartamentos:
    pavimento = apartamento[0]
    unidade_numero = apartamento[1]
    
    if pavimento not in apartamentos_dict:
        apartamentos_dict[pavimento] = []
    
    apartamentos_dict[pavimento].append(unidade_numero)
    pavimentos_com_apartamentos.add(pavimento)

# Monta o texto inicial para os apartamentos
primeiro_pavimento = min(pavimentos_com_apartamentos, key=extrair_numero_pavimento)
ultimo_pavimento = max(pavimentos_com_apartamentos, key=extrair_numero_pavimento)

texto_apartamentos = f"Os Apartamentos estão localizados do {primeiro_pavimento} ao {ultimo_pavimento}, num total de {total_apartamentos} unidades autônomas, sendo:\n"

# Itera pelos pavimentos e concatena as informações de apartamentos, ordenando pelo número
for pavimento in sorted(apartamentos_dict.keys(), key=extrair_numero_pavimento):
    unidades_formatadas = formatar_unidades(apartamentos_dict[pavimento])
    texto_pavimento = f"{pavimento}: apartamentos nº {unidades_formatadas};\n"
    texto_apartamentos += texto_pavimento


# Função auxiliar para formatar a lista de unidades
def formatar_unidades(unidades):
    unidades_formatadas = ', '.join(map(str, unidades[:-1])) + f' e {unidades[-1]}'
    return unidades_formatadas

# Apura a quantidade total de unidades autônomas da espécie "LOJA"
query_total_lojas = """
SELECT COUNT(*)
FROM cri
WHERE especie_unidade = 'LOJA';
"""
cursor.execute(query_total_lojas)
total_lojas = cursor.fetchone()[0]

# Apura a localização das lojas por pavimento
query_lojas_por_pavimento = """
SELECT pavimento, unidade_numero
FROM cri
WHERE especie_unidade = 'LOJA'
ORDER BY pavimento, unidade_numero;
"""
cursor.execute(query_lojas_por_pavimento)
lojas = cursor.fetchall()

# Dicionário para armazenar as unidades por pavimento
lojas_dict = {}
for pavimento, unidade in lojas:
    if pavimento not in lojas_dict:
        lojas_dict[pavimento] = []
    lojas_dict[pavimento].append(unidade)

# Construção do texto
texto_lojas = f"As Lojas estão localizadas no térreo, num total de {total_lojas} unidades autônomas, sendo as Lojas nº "

# Itera pelos pavimentos e concatena as informações das lojas, ordenando pelo número
for pavimento in sorted(lojas_dict.keys(), key=lambda x: int(x) if x.isdigit() else x):
    unidades_formatadas = formatar_unidades(sorted(lojas_dict[pavimento]))
    texto_pavimento = f"{unidades_formatadas}.\n"
    texto_lojas += texto_pavimento



# FINALIZACAO DE TODOS DATAFRAMES

# Salva os textos gerados em arquivos
with open('./outros/localizacao_vagas.txt', 'w', encoding='utf-8') as f:
    f.write(texto_vagas)

with open('./outros/localizacao_apartamentos.txt', 'w', encoding='utf-8') as f:
    f.write(texto_apartamentos)
    
with open('./outros/localizacao_lojas.txt', 'w', encoding='utf-8') as f:
    f.write(texto_lojas)
    

# Exibe o texto final para apartamentos
print(texto_vagas)
print(texto_apartamentos)
print(texto_lojas)

# Fecha a conexão com o banco de dados
conn.close()
