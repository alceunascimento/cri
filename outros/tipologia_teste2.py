import sqlite3

# Conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')
cursor = conn.cursor()

# Query para selecionar todas as unidades, agrupadas por especie_unidade e tipo_unidade
query = """
SELECT especie_unidade, tipo_unidade, unidade_numero, area_privativa, area_comum, area_total_construida, 
       fracao_ideal_solo_condominio, quota_terreno_condominio, 
       fracao_ideal_unidade_subcondominio, vaga_vinculada_descoberta, area_vinculada_outras, area_comum_descoberta
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

# Abre três arquivos separados para apartamentos, vagas e lojas
with open('./outros/tipos_apartamento.txt', 'w', encoding='utf-8') as f_apartamento, \
     open('./outros/tipos_vagas.txt', 'w', encoding='utf-8') as f_vaga, \
     open('./outros/tipos_lojas.txt', 'w', encoding='utf-8') as f_loja:
    
    # Itera sobre cada combinação de especie_unidade e tipo_unidade
    for (especie_unidade, tipo_unidade), lista_unidades in unidades_dict.items():
        numero_unidades = len(lista_unidades)
        numeros_unidades = ', '.join([str(unidade[2]) for unidade in lista_unidades])
        area_privativa = lista_unidades[0][3]
        area_comum = lista_unidades[0][4]
        area_total_construida = lista_unidades[0][5]
        fracao_ideal_solo_condominio = lista_unidades[0][6]
        quota_terreno = lista_unidades[0][7]
        fracao_ideal_unidade_subcondominio = lista_unidades[0][8]
        vaga_vinculada_descoberta = lista_unidades[0][9]
        area_vinculada_outras = lista_unidades[0][10]
        area_comum_descoberta = lista_unidades[0][11]

        # Define o texto final de acordo com a especie_unidade
        if especie_unidade.lower() == 'apartamento':
            texto_apartamento = f"""
            APARTAMENTO {tipo_unidade}: {numero_unidades} unidades, correspondentes aos apartamentos nº {numeros_unidades}, 
            possuindo cada unidade as seguintes áreas construídas: área privativa de {area_privativa} metros quadrados, 
            área comum de {area_comum} metros quadrados, perfazendo a área construída de {area_total_construida} metros quadrados; 
            cabendo-lhe as seguintes frações: fração ideal de solo no subcondomínio de {fracao_ideal_unidade_subcondominio}, fração ideal de solo no condomínio de {fracao_ideal_solo_condominio} 
            e quota de terreno de {quota_terreno} metros quadrados. Possuindo ainda uma área comum descoberta de {area_comum_descoberta} metros quadrados
            """

            # Escreve o texto_apartamento no arquivo de apartamentos
            f_apartamento.write(texto_apartamento)
            f_apartamento.write('\n')

        elif especie_unidade.lower() == 'vaga':
            # Verifica se existe área vinculada (área de depósito) associada
            if area_vinculada_outras == 0:
                texto_vaga = f"""
                VAGA TIPO {tipo_unidade}: {numero_unidades} unidades, correspondentes às vagas nº {numeros_unidades}, 
                possuindo cada unidade as seguintes áreas construídas: área privativa de {area_privativa} metros quadrados, 
                área comum de {area_comum} metros quadrados, perfazendo a área construída de {area_total_construida} metros quadrados; 
                cabendo-lhe as seguintes frações: fração ideal de solo no subcondomínio de {fracao_ideal_unidade_subcondominio}, fração ideal de solo no condomínio de {fracao_ideal_solo_condominio} 
                e quota de terreno de {quota_terreno} metros quadrados.
                """
            else:
                texto_vaga = f"""
                VAGA TIPO {tipo_unidade}: {numero_unidades} unidades, correspondentes às vagas nº {numeros_unidades}, 
                possuindo cada unidade as seguintes áreas construídas: área privativa de {area_privativa} metros quadrados, 
                área comum de {area_comum} metros quadrados, área de depósito vinculado {numeros_unidades}, respectivamente, de {area_vinculada_outras} metros quadrados, 
                perfazendo a área construída de {area_total_construida} metros quadrados; 
                cabendo-lhe as seguintes frações: fração ideal de solo no subcondomínio de {fracao_ideal_unidade_subcondominio}, fração ideal de solo no condomínio de {fracao_ideal_solo_condominio} 
                e quota de terreno de {quota_terreno} metros quadrados.
                """

            # Escreve o texto_vaga no arquivo de vagas
            f_vaga.write(texto_vaga)
            f_vaga.write('\n')

        elif especie_unidade.lower() == 'loja':
            texto_loja = f"""
            LOJA {tipo_unidade}: {numero_unidades} unidades, correspondentes ao Comércio e Serviço Vicinal  nº {numeros_unidades}, 
            possuindo área privativa de {area_privativa} metros quadrados, área comum de {area_comum} metros quadrados, 
            perfazendo uma área total construída de {area_total_construida} metros quadrados; 
            cabendo-lhe as seguintes frações: fração ideal de solo no subcondomínio de {fracao_ideal_unidade_subcondominio}, fração ideal de solo no condomínio de {fracao_ideal_solo_condominio} 
            e quota de terreno de {quota_terreno} metros quadrados.
            """

            # Escreve o texto_loja no arquivo de lojas
            f_loja.write(texto_loja)
            f_loja.write('\n')

# Fecha a conexão com o banco de dados
conn.close()
