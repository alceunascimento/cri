import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_02
query = "SELECT * FROM quadro_area_04A"
df_quadro_area_04 = pd.read_sql_query(query, conn)

# Remover a coluna 'ROWID' se ela estiver presente
if 'ROWID' in df_quadro_area_04.columns:
    df_quadro_area_04 = df_quadro_area_04.drop(columns=['ROWID'])

# Buscar as informações da tabela informacoes_preliminares
query = """
SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao, nome_edificio
FROM informacoes_preliminares 
LIMIT 1
"""
result = pd.read_sql_query(query, conn).iloc[0]

# Extrair os valores das colunas
incorporador = result['nome_incorporador']
responsavel_tecnico = result['nome_responsavel_tecnico']
registro_crea = result['registro_crea']
local_construcao = result['local_construcao']
nome_edificio = result['nome_edificio']

# Fechar a conexão com o banco de dados
conn.close()

# Criar as colunas hierárquicas de acordo com a estrutura fornecida, incluindo 'subcondominio'
columns = pd.MultiIndex.from_tuples([
    ("", "DESIGNAÇÃO DA UNIDADE", "(QII-19)", "39"),
    
    ("CUSTO DA CONSTRUÇÃO DA UNIDADE AUTÔNOMA", "ÁREA EQUIVALENTE EM ÁREA DE CUSTO PADRÃO DAS UNIDADES", "(QII-38)", "40"),
    ("CUSTO DA CONSTRUÇÃO DA UNIDADE AUTÔNOMA", "CUSTO", "(31 x ITEM 13.QIII)", "41"),
    ("CUSTO DA CONSTRUÇÃO DA UNIDADE AUTÔNOMA", "COEFICIENTE DE PROPORCIONALIDADE (PARA RATEIO DO CUSTO DA CONSTRUÇÃO)", "(QII-31)", "42"),
      
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "COEFICIENTE DE PROPORCIONALIDADE (DAS UNIDADES QUE SUPORTAM O CUSTO DA CONSTRUÇÃO)", "(42)", "43"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "COEFICIENTE DE RATEIO DE CONSTRUÇÃO TOTAL", "(43/SOMA 43)", "44"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "ÁREA EQUIVALENTE EM ÁREA DE CUSTO PADRÃO TOTAL", "(44 X SOMA 40)", "45"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "CUSTO DE CONSTRUÇÃO TOTAL", "(44 X ITEM 13.QIII)", "46"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "CUSTO DA SUB-ROGAÇÃO SUPORTADA POR CADA UNIDADE", "(46 - 41)", "47"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "ÁREA REAL DAS UNIDADES SUB-ROGADAS", "(QII-37)", "48"),
    ("RERRATEIO DO CUSTO (QUANDO HOUVER UNIDADE(S) DADA(S) EM PAGAMENTO DO TERRENO)", "QUOTA DA ÁREA REAL DADA EM PAGAMENTO DO TERRENO", "(44 X SOMA 48)", "49"),
    
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "TOTAL (TOTAL DE UNIDADES IDÊNTICAS)", "", "50"),
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "SUB-ROGADAS", "", "51"),
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "DIFERENCA (UNIDADES QUE SUPORTAM O CUSTO DA EDIFICAÇÃO)", "(50-51)", "52")
])


# Right after loading the DataFrame from SQL
df_quadro_area_04 = df_quadro_area_04.drop('subcondominio', axis=1)

# Atribuir o novo cabeçalho ao dataframe
df_quadro_area_04.columns = columns[:len(df_quadro_area_04.columns)]  # Ajuste dinâmico para garantir compatibilidade

# Extraindo a coluna 'Quantidade' sem o MultiIndex para garantir o alinhamento
quantidade_col = df_quadro_area_04[("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "DIFERENCA (UNIDADES QUE SUPORTAM O CUSTO DA EDIFICAÇÃO)", "(50-51)", "52")].values
print(quantidade_col)

soma_quantidade1 = df_quadro_area_04[("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "TOTAL (TOTAL DE UNIDADES IDÊNTICAS)", "", "50")].sum().item()
print(soma_quantidade1) 
print(type(soma_quantidade1))


soma_quantidade2 = df_quadro_area_04[("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "DIFERENCA (UNIDADES QUE SUPORTAM O CUSTO DA EDIFICAÇÃO)", "(50-51)", "52")].sum().item()
print(soma_quantidade2) 
print(type(soma_quantidade2))




# Selecionar as colunas numéricas para multiplicação, exceto a coluna 'Quantidade'
numeric_cols = df_quadro_area_04.drop(columns=[
    ("", "DESIGNAÇÃO DA UNIDADE", "(QII-19)", "39"), 
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "TOTAL (TOTAL DE UNIDADES IDÊNTICAS)", "", "50"),
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "DIFERENCA (UNIDADES QUE SUPORTAM O CUSTO DA EDIFICAÇÃO)", "(50-51)", "52")
])
print(numeric_cols)

# Aplicar a multiplicação para cada valor das colunas numéricas pelo valor da coluna `Quantidade`
df_multiplicado = numeric_cols.mul(quantidade_col, axis=0)
# Calcular a soma das colunas multiplicadas
sum_row = df_multiplicado.sum()

# Identificar a coluna de custo
coluna_custo = ("CUSTO DA CONSTRUÇÃO DA UNIDADE AUTÔNOMA", "CUSTO", "(31 x ITEM 13.QIII)", "41")

# Arredondar apenas o valor desta coluna para duas casas decimais
sum_row[coluna_custo] = round(sum_row[coluna_custo], 2)




print(sum_row)


# Primeiro arredonda os valores numéricos para 2 casas decimais
#sum_row = sum_row.apply(lambda x: round(x, 6) if isinstance(x, (int, float)) else x)
# Adicionar a coluna de Pavimento com valor "Total" na linha de somatório
sum_row[("", "DESIGNAÇÃO DA UNIDADE", "(QII-19)", "39")] = "Total"
# Adicionar a linha de somatório ao dataframe original
df_quadro_area_04.loc['Total'] = sum_row

# Substituir o valor da coluna 'Quantidade' na linha de somatório
df_quadro_area_04.at['Total', ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "TOTAL (TOTAL DE UNIDADES IDÊNTICAS)", "", "50")] = soma_quantidade1
df_quadro_area_04.at['Total', ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "DIFERENCA (UNIDADES QUE SUPORTAM O CUSTO DA EDIFICAÇÃO)", "(50-51)", "52")] = soma_quantidade2
print(df_quadro_area_04)




# Formatar os dados usando pandas Styler
def format_styler(df):
    styler = df.style.set_caption("").set_table_styles(
        [
            {'selector': 'thead th:first-child', 'props': 'display:none'},  # Hide the first column header
            {'selector': 'thead th', 'props': [('background-color', 'lightgrey'), ('text-align', 'center'), ('font-weight', 'bold'), ('display', 'table-cell'), ('border', '1px solid black')]},
            {'selector': 'tbody td', 'props': [('border', '1px solid black'), ('text-align', 'right')]},
            {'selector': '.index_name', 'props': 'display:none'},
            {'selector': '.row_heading', 'props': 'display:none'}
        ]
    ).format(na_rep='-', precision=8, decimal=',', thousands='.')\
    .format({("CUSTO DA CONSTRUÇÃO DA UNIDADE AUTÔNOMA", "CUSTO", "(31 x ITEM 13.QIII)", "41"): '{:,.2f}'.format}, decimal=',', thousands='.')
    
    return styler

# Aplicar a formatação
styled_table = format_styler(df_quadro_area_04)

# HTML para o cabeçalho antes da tabela, usando os dados obtidos
html_cabecalho = f"""
<table style="width: 100%; border: 1px solid black; border-collapse: collapse;">
    <tr>
        <td colspan="4" style="text-align: center; font-weight: bold; border: 1px solid black;">
            INFORMAÇÕES PARA ARQUIVO NO REGISTRO DE IMÓVEIS<br>
            (Lei 4.591 - 16/12/64 - Art. 32 e ABNT NBR 12721)
        </td>
    </tr>
    <tr>
        <td colspan="4" style="text-align: center; border: 1px solid black;">
            QUADRO IV A - AVALIAÇÃO DO CUSTO DE CONSTRUÇÃO DE CADA UNIDADE AUTÔNOMA E CÁCULO DO RE-RATEIO DE SUBROGAÇÃO - COLUNAS 39 A 52
        </td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Local do Imóvel: {local_construcao}, Curitiba, Paraná</td>
        <td style="border: 1px solid black;">Folha 5</td>
        <td style="border: 1px solid black;">Total de Folhas 10</td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Nome do edifício: {nome_edificio}</td>
    </tr>
    <tr>
        <td colspan="2" style="border: 1px solid black;">INCORPORADOR</td>
        <td colspan="2" style="border: 1px solid black;">PROFISSIONAL RESPONSÁVEL</td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">{incorporador}</td>
        <td style="border: 1px solid black;">Data: 28/10/2024</td>
        <td style="border: 1px solid black;">{responsavel_tecnico} ({registro_crea})</td>
        <td style="border: 1px solid black;"></td>
    </tr>
</table>
"""

# Gerar o conteúdo completo em HTML, unindo o cabeçalho e a tabela formatada
html_output = html_cabecalho + styled_table._repr_html_()

# Salvar o conteúdo completo em um arquivo HTML
with open("./pre_cri/output/nbr_04A_quadro_area_04A.html", "w") as file:
    file.write(html_output)

print("Arquivo HTML gerado com sucesso.")
