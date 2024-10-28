import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Buscar as informações da tabela informacoes_preliminares com base nas variáveis fornecidas
query = """
SELECT nome_incorporador, cnpj_incorporador, endereco_incorporador, 
       nome_responsavel_tecnico, registro_crea, art, endereco_responsavel_tecnico,
       nome_edificio, local_construcao, cidade_uf, designacao_projeto_padrao,
       quantidade_unidades_autonomas, padrao_acabamento, numero_pavimentos, vagas_total, 
       vagas_unidade_autonoma, vagas_acessorio_unidade_autonoma, vagas_uso_comum, area_lote, 
       data_aprovacao_projeto, numero_alvara_projeto
FROM informacoes_preliminares
LIMIT 1
"""
result = pd.read_sql_query(query, conn).iloc[0]

# Extrair os valores das colunas
incorporador = result['nome_incorporador']
cnpj = result['cnpj_incorporador']
endereco_incorporador = result['endereco_incorporador']
responsavel_tecnico = result['nome_responsavel_tecnico']
registro_crea = result['registro_crea']
art = result['art']
endereco_responsavel_tecnico = result['endereco_responsavel_tecnico']
nome_edificio = result['nome_edificio']
local_construcao = result['local_construcao']
cidade_uf = result['cidade_uf']
designacao_projeto_padrao = result['designacao_projeto_padrao']
quantidade_unidades_autonomas = result['quantidade_unidades_autonomas']
padrao_acabamento = result['padrao_acabamento']
numero_pavimentos = result['numero_pavimentos']
vagas_total = result['vagas_total']
vagas_unidade_autonoma = result['vagas_unidade_autonoma']
vagas_acessorio_unidade_autonoma = result['vagas_acessorio_unidade_autonoma']
vagas_uso_comum = result['vagas_uso_comum']
area_lote = result['area_lote']
data_aprovacao_projeto = result['data_aprovacao_projeto']
numero_alvara_projeto = result['numero_alvara_projeto']

# Fechar a conexão com o banco de dados
conn.close()

# HTML para o novo quadro com a estrutura ajustada de acordo com a imagem de referência
html_quadro = f"""
<html>
<head>
    <title>Informações Preliminares - NBR 12.721</title>
    <style>
        table {{
            width: 100%;
            border-collapse: collapse;
            border: 1px solid black;
        }}
        th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .section-header {{
            font-weight: bold;
            background-color: #e0e0e0;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1 style="text-align: center;">NBR 12.721 - INFORMAÇÕES PRELIMINARES</h1>
    
    <table>
        <tr class="section-header">
            <td colspan="2">1. INCORPORADOR</td>
        </tr>
        <tr>
            <td>1.1 Nome:</td>
            <td>{incorporador}</td>
        </tr>
        <tr>
            <td>1.2 CNPJ / CPF:</td>
            <td>{cnpj}</td>
        </tr>
        <tr>
            <td>1.3 Endereço:</td>
            <td>{endereco_incorporador}</td>
        </tr>

        <tr class="section-header">
            <td colspan="4">2. RESPONSABILIDADE TÉCNICA PELAS INFORMAÇÕES E CÁLCULOS</td>
        </tr>
        <tr>
            <td>2.1 Profissional Responsável Técnico:</td>
            <td>{responsavel_tecnico}</td>
        </tr>
        <tr>
            <td>2.2 Número de registro profissional no CREA:</td>
            <td>{registro_crea}</td>
        </tr>
        <tr>
            <td>2.3 Anotação de Responsabilidade Técnica (ART):</td>
            <td>{art}</td>
        </tr>
        <tr>
            <td>2.4 Endereço:</td>
            <td>{endereco_responsavel_tecnico}</td>
        </tr>

        <tr class="section-header">
            <td colspan="4">3. DADOS DO PROJETO / IMÓVEL</td>
        </tr>
        <tr>
            <td>3.1 Nome do Edifício:</td>
            <td>{nome_edificio}</td>
        </tr>
        <tr>
            <td>3.2 Local da Construção:</td>
            <td>{local_construcao}</td>
        </tr>
        <tr>
            <td>3.3 Cidade / UF:</td>
            <td>{cidade_uf}</td>
        </tr>
        <tr>
            <td>3.4 Designação Projeto-padrão da NBR 12.721:</td>
            <td>{designacao_projeto_padrao}</td>
        </tr>
        <tr>
            <td>3.5 Quantidade de Unidades Autônomas:</td>
            <td>{quantidade_unidades_autonomas}</td>
        </tr>
        <tr>
            <td>3.6 Padrão de Acabamento:</td>
            <td>{padrao_acabamento}</td>
        </tr>
        <tr>
            <td>3.7 Número de Pavimentos:</td>
            <td>{numero_pavimentos}</td>
        </tr>
        <tr>
            <td>3.8 Vagas Total:</td>
            <td>{vagas_total}</td>
        </tr>
        <tr>
            <td>3.8.1 Vagas por Unidade Autônoma:</td>
            <td>{vagas_unidade_autonoma}</td>
        </tr>
        <tr>
            <td>3.8.2 Vagas Acessório de Unidade Autônoma:</td>
            <td>{vagas_acessorio_unidade_autonoma}</td>
        </tr>
        <tr>
            <td>3.8.3 Vagas de Uso Comum:</td>
            <td>{vagas_uso_comum}</td>
        </tr>
        <tr>
            <td>3.9 Área do Lote / Terreno:</td>
            <td>{area_lote} m²</td>
        </tr>
        <tr>
            <td>3.10 Data de aprovação do projeto arquitetônico:</td>
            <td>{data_aprovacao_projeto}</td>
        </tr>
        <tr>
            <td>3.11 Número do Alvará:</td>
            <td>{numero_alvara_projeto}</td>
        </tr>

        <tr class="section-header">
            <td colspan="2">4. INFORMACOES PLANILHAS / QUADROS</td>
        </tr>
            <td colspan="2"> 
            Esta é a primeira folha de um total de 10 folhas, 
            todas numeradas seguidamente e assinadas conjuntamente 
            pelo profissional responsável técnico, incorporador /
            proprietário, para arquivamento e registro junto ao 
            competente Registro de Imóveis, em atendimento ao disposto 
            na Lei 4.591, de 16 de dezembro de 1.964.
            </td>
        </tr>
    </table>
</body>
</html>
"""

# Salvar o conteúdo HTML em um arquivo
with open("./pre_cri/output/nbr_00_informacoes_preliminares.html", "w") as file:
    file.write(html_quadro)

print("Arquivo HTML gerado com sucesso.")
