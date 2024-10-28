import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_01
query = "SELECT * FROM quadro_area_05"
df_quadro_area_05 = pd.read_sql_query(query, conn)

# Buscar as informações da tabela informacoes_preliminares
query = """
SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao,
       data_aprovacao_projeto
FROM informacoes_preliminares 
LIMIT 1
"""
result = pd.read_sql_query(query, conn).iloc[0]

# Extrair os valores das colunas
incorporador = result['nome_incorporador']
responsavel_tecnico = result['nome_responsavel_tecnico']
registro_crea = result['registro_crea']
local_construcao = result['local_construcao']
data_aprovacao = result['data_aprovacao_projeto']


# Fechar a conexão com o banco de dados
conn.close()

# Function to format multiline content
def format_multiline_content(df, column_name):
    values = df[column_name].dropna().tolist()
    return '<br>'.join(values) if values else ''

# Preparar os dados do formulário com múltiplas linhas
form_data = {
    'a) Tipo de edificação:': format_multiline_content(df_quadro_area_05, 'edificacao_tipo'),
    'b) Número de Pavimentos:': format_multiline_content(df_quadro_area_05, 'edificacao_pavimento'),
    'c) Número de unidades autônomas por pavimento:': format_multiline_content(df_quadro_area_05, 'edificacao_quantidade_unidades_por_pavimentos'),
    'd) Explicitação da numeração das unidades autônomas:': format_multiline_content(df_quadro_area_05, 'edificacao_indicacao_unidades_por_pavimento'),
    'e) Pavimentos especiais (situação e descrição):': format_multiline_content(df_quadro_area_05, 'edificacao_descricao_pavimentos'),
    'f) Data de aprovação do projeto e repartição competente:':  format_multiline_content(df_quadro_area_05, 'alvara_construcao_data_emissao'),
    'g) Outras indicações (numero de blocos):': format_multiline_content(df_quadro_area_05, 'edificacao_blocos'),
    'g) Outras indicações (total de unidades autônomas):': format_multiline_content(df_quadro_area_05, 'edificacao_quantidade_unidades_por_subcondominio')
}

# HTML para o cabeçalho e conteúdo principal
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
        td, th {{ border: 1px solid black; padding: 8px; }}
        .header {{ text-align: center; font-weight: bold; }}
        .section-title {{ background-color: #f0f0f0; }}
        .label {{ font-weight: bold; width: 30%; vertical-align: top; }}
        .content {{ text-align: left; }}
        .content-cell {{ text-align: left; vertical-align: top; }}
        .multiline {{
            white-space: pre-line;
            font-style: regular;
        }}
    </style>
</head>
<body>
    <table>
        <tr>
            <td colspan="4" class="header">
                INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS<br>
                (LEI 4591 - 16/12/64 - ART. 32 E ABNT NBR 12.721/2006)
            </td>
        </tr>
        <tr>
            <td colspan="3">
                INFORMAÇÕES GERAIS<br>
            </td>
            <td style="text-align: right;">
                FOLHA NÚMERO 12<br>
                TOTAL FOLHAS 18
            </td>
        </tr>
        <tr>
            <td colspan="4">LOCAL DO IMÓVEL: {local_construcao}</td>
        </tr>
        <tr>
            <td colspan="2" class="section-title">INCORPORADOR</td>
            <td colspan="2" class="section-title">PROFISSIONAL RESPONSÁVEL PELO CÁLCULO</td>
        </tr>
        <tr>
            <td colspan="2">
                Nome: {incorporador}<br>
                Data: out/2024
            </td>
            <td colspan="2">
                Nome: {responsavel_tecnico}<br>
                Data: out/2024 &nbsp;&nbsp;&nbsp;&nbsp; Registro no CREA: {registro_crea}
            </td>
        </tr>
    </table>

    <table>
        <tr>
            <td class="label">a) Tipo de edificação:</td>
            <td class="content-cell">{form_data['a) Tipo de edificação:']}</td>
        </tr>
        <tr>
            <td class="label">b) Número de Pavimentos:</td>
            <td class="content-cell">{form_data['b) Número de Pavimentos:']}</td>
        </tr>
        <tr>
            <td class="label">c) Número de unidades autônomas por pavimento:</td>
            <td class="content-cell multiline">{form_data['c) Número de unidades autônomas por pavimento:']}</td>
        </tr>
        <tr>
            <td class="label">d) Explicitação da numeração das unidades autônomas:</td>
            <td class="content-cell multiline">{form_data['d) Explicitação da numeração das unidades autônomas:']}</td>
        </tr>
        <tr>
            <td class="label">e) Pavimentos especiais (situação e descrição):</td>
            <td class="content-cell multiline">{form_data['e) Pavimentos especiais (situação e descrição):']}</td>
        </tr>
        <tr>
            <td class="label">f) Data de aprovação do projeto e repartição competente:</td>
            <td class="content-cell">{form_data['f) Data de aprovação do projeto e repartição competente:']}</td>
        </tr>
        <tr>
            <td class="label">g) Outras indicações (numero de blocos):</td>
            <td class="content-cell">{form_data['g) Outras indicações (numero de blocos):']}</td>
        </tr>
        <tr>
            <td class="label">g) Outras indicações (total de unidades autônomas):</td>
            <td class="content-cell">{form_data['g) Outras indicações (total de unidades autônomas):']}</td>
        </tr>
    </table>
</body>
</html>
"""

# Salvar o conteúdo completo em um arquivo HTML
with open("./pre_cri/output/nbr_05_quadro_area_05.html", "w", encoding='utf-8') as file:
    file.write(html_template)