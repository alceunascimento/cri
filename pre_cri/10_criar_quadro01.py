import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_01
query = "SELECT * FROM quadro_area_01"
df_quadro_area_01 = pd.read_sql_query(query, conn)

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

# Criar as colunas hierárquicas de acordo com a estrutura fornecida
columns = pd.MultiIndex.from_tuples([
    # pavimento
    ("", "", "", "Pavimento", "1"),
    
    # ÁREA DE DIVISÃO NÃO PROPORCIONAL: ÁREA PRIVATIVA
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO", "", "2"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "3"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "4"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "REAL (2+3)", "5"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (2+4)", "6"),
    
    # ÁREA DE DIVISÃO NÃO PROPORCIONAL: ÁREA DE USO COMUM
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "", "7"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "8"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "9"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL (7+8)", "10"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (7+9)", "11"),
    
    # ÁREA DE DIVISÃO PROPORCIONAL: ÁREA DE USO COMUM
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "", "12"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "13"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "14"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL (12+13)", "15"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (12+14)", "16"),
    
    # ÁREA DO PAVIMENTO
    ("ÁREA DO PAVIMENTO", "", "", "REAL 5+10+15)", "17"),
    ("ÁREA DO PAVIMENTO", "", "", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (6+11+16)", "18"),
    
    # QUANTIDADE (Número de unidades de pavimentos idênticos)
    ("QUANTIDADE", "", "", "Número de unidades de pavimentos")
])

# Atribuir o novo cabeçalho ao dataframe
df_quadro_area_01.columns = columns[:len(df_quadro_area_01.columns)]  # Ajuste dinâmico para garantir compatibilidade

# Extraindo a coluna 'Quantidade' sem o MultiIndex para garantir o alinhamento
quantidade_col = df_quadro_area_01[('QUANTIDADE', '', '', 'Número de unidades de pavimentos')].values
print(quantidade_col)
soma_quantidade = df_quadro_area_01[('QUANTIDADE', '', '', 'Número de unidades de pavimentos')].sum().item()
print(soma_quantidade) 
print(type(soma_quantidade))

# Selecionar as colunas numéricas para multiplicação, exceto a coluna 'Quantidade'
numeric_cols = df_quadro_area_01.drop(columns=[('', '', '', 'Pavimento', '1'), ('QUANTIDADE', '', '', 'Número de unidades de pavimentos')])
# Aplicar a multiplicação para cada valor das colunas numéricas pelo valor da coluna `Quantidade`
df_multiplicado = numeric_cols.mul(quantidade_col, axis=0)
# Calcular a soma das colunas multiplicadas
sum_row = df_multiplicado.sum()

# Adicionar a coluna de Pavimento com valor "Total" na linha de somatório
sum_row[('', '', '', 'Pavimento', '1')] = "Total"
# Adicionar a linha de somatório ao dataframe original
df_quadro_area_01.loc['Total'] = sum_row


# Substituir o valor da coluna 'Quantidade' na linha de somatório
df_quadro_area_01.at['Total', ('QUANTIDADE', '', '', 'Número de unidades de pavimentos')] = soma_quantidade
print(df_quadro_area_01)


# SECOND SUMS
real_private_area_col = ('ÁREA DE DIVISÃO NÃO PROPORCIONAL', 'ÁREA PRIVATIVA', 'TOTAIS', 'REAL (2+3)', '5')
real_common_area_col = ('ÁREA DE DIVISÃO NÃO PROPORCIONAL', 'ÁREA DE USO COMUM', 'TOTAIS', 'REAL (7+8)', '10')
real_proportional_common_area_col = ('ÁREA DE DIVISÃO PROPORCIONAL', 'ÁREA DE USO COMUM', 'TOTAIS', 'REAL (12+13)', '15')

equivalent_private_area_col = ('ÁREA DE DIVISÃO NÃO PROPORCIONAL', 'ÁREA PRIVATIVA', 'TOTAIS', 'EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (2+4)', '6')
equivalent_common_area_col = ('ÁREA DE DIVISÃO NÃO PROPORCIONAL', 'ÁREA DE USO COMUM', 'TOTAIS', 'EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (7+9)', '11')
equivalent_proportional_common_area_col = ('ÁREA DE DIVISÃO PROPORCIONAL', 'ÁREA DE USO COMUM', 'TOTAIS', 'EQUIVALENTE EM ÁREA DE CUSTO PADRÃO (12+14)', '16')

# Calculate the sums
real_private_area_sum = df_quadro_area_01.loc['Total', real_private_area_col].sum()
real_common_area_sum = df_quadro_area_01.loc['Total', real_common_area_col].sum()
real_proportional_common_area_sum = df_quadro_area_01.loc['Total', real_proportional_common_area_col].sum()

equivalent_private_area_sum = df_quadro_area_01.loc['Total', equivalent_private_area_col].sum()
equivalent_common_area_sum = df_quadro_area_01.loc['Total', equivalent_common_area_col].sum()
equivalent_proportional_common_area_sum = df_quadro_area_01.loc['Total', equivalent_proportional_common_area_col].sum()

# Create a new "Total 2" row
df_quadro_area_01.loc['Total 2', ('', '', '', 'Pavimento', '1')] = "ÁREA REAL GLOBAL:"
df_quadro_area_01.loc['Total 3', ('', '', '', 'Pavimento', '1')] = "ÁREA EQUIVALENTE GLOBAL:"


# Update the "Total" row with the correct values
#df_quadro_area_01.loc['Total 2', ('', '', '', 'Pavimento', '1')] = "Total 2"
df_quadro_area_01.loc['Total 2', ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO", "", "2")] = real_private_area_sum + real_common_area_sum + real_proportional_common_area_sum
df_quadro_area_01.loc['Total 3', ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO", "", "2")] = equivalent_private_area_sum + equivalent_common_area_sum + equivalent_proportional_common_area_sum















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
    ).format(na_rep='-', precision=8, decimal=',', thousands='.')
    
    return styler

# Aplicar a formatação
styled_table = format_styler(df_quadro_area_01)


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
            QUADRO I - Cálculo das Áreas nos Pavimentos e da Área Global - Colunas 1 a 18
        </td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Local do Imóvel: {local_construcao}, Curitiba, Paraná</td>
        <td style="border: 1px solid black;">Folha 2</td>
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
with open("./pre_cri/output/nbr_01_quadro_area_01.html", "w") as file:
    file.write(html_output)
