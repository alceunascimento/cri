import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_02
query = "SELECT * FROM quadro_area_04B"
df_quadro_area_04 = pd.read_sql_query(query, conn)

# Remover a coluna 'ROWID' se ela estiver presente
if 'ROWID' in df_quadro_area_04.columns:
    df_quadro_area_04 = df_quadro_area_04.drop(columns=['ROWID'])

# Buscar as informações da tabela informacoes_preliminares para o cabeçalho
query = """
SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao 
FROM informacoes_preliminares 
LIMIT 1
"""
result = pd.read_sql_query(query, conn).iloc[0]

# Extrair os valores das colunas para o cabeçalho
incorporador = result['nome_incorporador']
responsavel_tecnico = result['nome_responsavel_tecnico']
registro_crea = result['registro_crea']
local_construcao = result['local_construcao']

# Fechar a conexão com o banco de dados
conn.close()

# Criar as colunas hierárquicas de acordo com a estrutura fornecida, incluindo 'subcondominio'
columns = pd.MultiIndex.from_tuples([
    ("", "", "subcondominio"),
    ("", "DESIGNAÇÃO DA UNIDADE (19)", "A"),
    
    ("ÁREAS REAIS", "ÁREA PRIVATIVA PRINCIPAL", "B"),
    ("ÁREAS REAIS", "OUTRAS ÁREAS PRIVATIVAS (ACESSÓRIAS)", "C"),
    ("ÁREAS REAIS", "ÁREA PRIVATIVA TOTAL (23)=(B+C)", "D"),
    ("ÁREAS REAIS", "ÁREA DE USO COMUM (28+35)", "E"),
    ("ÁREAS REAIS", "ÁREA REAL TOTAL (37)=(D+E)", "F"),
    
    ("", "COEFICIENTE DE PROPORCIONALIDADE (31)", "G"),
    
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "", ""),
    
    ("OBSERVAÇÕES", "", ""),
])

# Atribuir o novo cabeçalho ao dataframe
df_quadro_area_04.columns = columns[:len(df_quadro_area_04.columns)]  # Ajuste dinâmico para garantir compatibilidade

# Extraindo a coluna 'Quantidade' sem o MultiIndex para garantir o alinhamento
quantidade_col = df_quadro_area_04[("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "", "")].values
print(quantidade_col)

soma_quantidade1 = df_quadro_area_04[("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "", "")].sum().item()
print(soma_quantidade1) 
print(type(soma_quantidade1))




# Selecionar as colunas numéricas para multiplicação, exceto a coluna 'Quantidade'
numeric_cols = df_quadro_area_04.drop(columns=[
    ("", "DESIGNAÇÃO DA UNIDADE (19)", "A"), 
    ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "", ""),
    ("", "", "subcondominio")
])
print(numeric_cols)

# Aplicar a multiplicação para cada valor das colunas numéricas pelo valor da coluna `Quantidade`
df_multiplicado = numeric_cols.mul(quantidade_col, axis=0)
# Calcular a soma das colunas multiplicadas
sum_row = df_multiplicado.sum()

# Adicionar a coluna de Pavimento com valor "Total" na linha de somatório
sum_row[("", "DESIGNAÇÃO DA UNIDADE (19)", "A")] = "Total"
# Adicionar a linha de somatório ao dataframe original
df_quadro_area_04.loc['Total'] = sum_row

# Substituir o valor da coluna 'Quantidade' na linha de somatório
df_quadro_area_04.at['Total', ("QUANTIDADES (Nº DE UNIDADES IDÊNTICAS)", "", "")] = soma_quantidade1

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
    ).format(na_rep='-', precision=8)
    
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
            QUADRO IV B - RESUMO DAS ÁREAS REAIS PARA ATOS DE REGISTRO E ESCRITURAÇÃO - COLUNAS A a G
        </td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Local do Imóvel: {local_construcao}</td>
        <td style="border: 1px solid black;">Folha 2</td>
        <td style="border: 1px solid black;">Total de Folhas 10</td>
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
with open("./pre_cri/output/nbr_04B_quadro_area_04B.html", "w") as file:
    file.write(html_output)

print("Arquivo HTML gerado com sucesso.")
