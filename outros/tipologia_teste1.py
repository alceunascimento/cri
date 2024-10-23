import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')
cursor = conn.cursor()

# Query para selecionar todas as unidades, agrupadas por especie_unidade e tipo_unidade
query = """
SELECT especie_unidade, tipo_unidade, unidade_numero, area_privativa, area_comum, area_total_construida, 
       fracao_ideal_solo_condominio, quota_terreno_condominio, 
       fracao_ideal_unidade_subcondominio, vaga_vinculada_descoberta
FROM cri
ORDER BY especie_unidade, tipo_unidade;
"""

# Executa a consulta
cursor.execute(query)
unidades = cursor.fetchall()

# Organiza os dados em um dicionário agrupado por especie_unidade e tipo_unidade
unidades_dict = {}
for unidade in unidades:
    especie = unidade[0]
    tipo = unidade[1]
    if (especie, tipo) not in unidades_dict:
        unidades_dict[(especie, tipo)] = []
    unidades_dict[(especie, tipo)].append(unidade)

# Abre o arquivo para escrita
with open('./outros/tipologia_unidade.txt', 'w', encoding='utf-8') as f:
    # Itera sobre cada combinação de especie_unidade e tipo_unidade
    for (especie_unidade, tipo_unidade), lista_unidades in unidades_dict.items():
        numero_unidades = len(lista_unidades)
        numeros_unidades = ', '.join([str(unidade[2]) for unidade in lista_unidades])
        area_privativa = lista_unidades[0][3]
        area_comum = lista_unidades[0][4]
        area_total_construida = lista_unidades[0][5]
        fracao_ideal_solo = lista_unidades[0][6]
        quota_terreno = lista_unidades[0][7]
        fracao_ideal_unidade = lista_unidades[0][8]
        vaga_vinculada_descoberta = lista_unidades[0][9]

        # Monta o texto final para essa combinação de especie_unidade e tipo_unidade
        texto = f"""
        {especie_unidade} TIPO {tipo_unidade}: {numero_unidades} unidades, correspondentes às unidades nº {numeros_unidades}, 
        possuindo cada unidade as seguintes áreas construídas: área privativa de {area_privativa} metros quadrados, 
        área comum de {area_comum} metros quadrados, perfazendo a área construída de {area_total_construida} metros quadrados; 
        cabendo-lhe as seguintes frações: fração ideal de solo no subcondomínio de {fracao_ideal_unidade}, fração ideal de solo no condomínio de {fracao_ideal_solo} 
        e quota de terreno de {quota_terreno} metros quadrados.
        """

        # Escreve o texto no arquivo
        f.write(texto)
        f.write('\n')

# Fecha a conexão com o banco de dados
conn.close()
