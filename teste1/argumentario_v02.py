import pandas as pd

# Assumindo que os DataFrames foram criados a partir de um arquivo XML
# Dataframes disponíveis: cri, alvara, imovel, informacoes_preliminares, quadro_areas_01, quadro_areas_02, quadro_areas_03, quadro_areas_04A, quadro_areas_04B, quadro_areas_05, quadro_areas_06, quadro_areas_07, quadro_areas_08

dataframes = {
    'cri': pd.DataFrame(),
    'alvara': pd.DataFrame(),
    'imovel': pd.DataFrame({'descricao_imovel': ['Descrição exemplo'], 'area_imovel_tabular': [500]}),
    'informacoes_preliminares': pd.DataFrame({'3.9 Área do Lote/Terreno (m2)': [500]}),
    'quadro_areas_01': pd.DataFrame(),
    'quadro_areas_02': pd.DataFrame(),
    'quadro_areas_03': pd.DataFrame(),
    'quadro_areas_04A': pd.DataFrame(),
    'quadro_areas_04B': pd.DataFrame(),
    'quadro_areas_05': pd.DataFrame(),
    'quadro_areas_06': pd.DataFrame(),
    'quadro_areas_07': pd.DataFrame(),
    'quadro_areas_08': pd.DataFrame()
}

# Função para responder a pergunta A.1
def verificar_area_terreno(dataframes):
    respostas = []
    
    if 'informacoes_preliminares' in dataframes and 'imovel' in dataframes:
        informacoes_preliminares = dataframes['informacoes_preliminares']
        imovel = dataframes['imovel']
        
        try:
            area_terreno = informacoes_preliminares['3.9 Área do Lote/Terreno (m2)'].iloc[0]
            area_imovel = imovel['area_imovel_tabular'].iloc[0]
            
            if area_terreno == area_imovel:
                resposta = f"A.1. A 'área do terreno' é igual à 'área do imóvel' contida na descrição tabular da matrícula?\n- Sim. Nos dois documentos consta a área de {area_terreno}m²."
            else:
                diferenca = abs(area_terreno - area_imovel)
                resposta = f"A.1. A 'área do terreno' é igual à 'área do imóvel' contida na descrição tabular da matrícula?\n- Não. Há uma diferença de {diferenca}m² entre as áreas dos dois documentos."
            
            respostas.append(resposta)
        except IndexError:
            respostas.append("Erro: As tabelas 'informacoes_preliminares' ou 'imovel' não possuem dados suficientes para a verificação.")
    else:
        respostas.append("Erro: Os DataFrames 'informacoes_preliminares' e/ou 'imovel' não estão disponíveis.")
    
    return respostas

# Chamando a função e exibindo as respostas
with open('relatorio_verificacao.txt', 'w') as relatorio:
    relatorio.write("AUTOMATIZAÇÃO INCORPORAÇÃO IMOBILIÁRIA\n")
    relatorio.write("EDIFÍCIOS\n\n")
    relatorio.write("# A. Questões definidas pela legislação (Código de Normas da CGJ TJPR Extrajudicial)\n\n")
    
    respostas = verificar_area_terreno(dataframes)
    for resposta in respostas:
        relatorio.write(resposta + "\n")

print("Relatório gerado com sucesso em 'relatorio_verificacao.txt'")