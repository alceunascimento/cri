import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_01
query = "SELECT * FROM quadro_area_01"
df_quadro_area_01 = pd.read_sql_query(query, conn)

# Fechar a conexão com o banco de dados
conn.close()

# Criar as colunas hierárquicas de acordo com a estrutura fornecida
columns = pd.MultiIndex.from_tuples([
    # pavimento
    ("", "", "", "Pavimento", "1"),
    
    # ÁREA DE DIVISÃO NÃO PROPORCIONAL: ÁREA PRIVATIVA
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO", "REAL", "2"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "3"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "4"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "REAL", "5"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "6"),
    
    # ÁREA DE DIVISÃO NÃO PROPORCIONAL: ÁREA DE USO COMUM
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "REAL", "7"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "8"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "9"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL", "10"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "11"),
    
    # ÁREA DE DIVISÃO PROPORCIONAL: ÁREA DE USO COMUM
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "REAL", "12"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "13"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "14"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL", "15"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "16"),
    
    # ÁREA DO PAVIMENTO
    ("ÁREA DO PAVIMENTO", "", "", "REAL", "17"),
    ("ÁREA DO PAVIMENTO", "", "", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "18"),
    
    # QUANTIDADE (Número de unidades de pavimentos idênticos)
    ("QUANTIDADE", "", "", "Número de unidades de pavimentos")
])

# Atribuir o novo cabeçalho ao dataframe
df_quadro_area_01.columns = columns[:len(df_quadro_area_01.columns)]  # Ajuste dinâmico para garantir compatibilidade

# Extraindo a coluna 'Quantidade' sem o MultiIndex para garantir o alinhamento
quantidade_col = df_quadro_area_01[('QUANTIDADE', '', '', 'Número de unidades de pavimentos')].values

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

# Agora calcular a soma da coluna 'Quantidade' separadamente
soma_quantidade = df_quadro_area_01[('QUANTIDADE', '', '', 'Número de unidades de pavimentos')].sum()

print(soma_quantidade)

# Substituir o valor da coluna 'Quantidade' na linha de somatório
df_quadro_area_01.at['Total', ('QUANTIDADE', '', '', 'Número de unidades de pavimentos')] = soma_quantidade

print(df_quadro_area_01)

# Formatar os dados usando pandas Styler
def format_styler(df):
    styler = df.style.set_caption("QUADRO 02 - ÁREA DE DIVISÃO").set_table_styles(
        [
            {'selector': 'thead th', 'props': [('background-color', 'lightgrey'), ('text-align', 'center'), ('font-weight', 'bold')]},
            {'selector': 'tbody td', 'props': [('border', '1px solid black')]}
        ]
    ).format(na_rep='-', precision=2)
    
    return styler

# Aplicar a formatação
styled_table = format_styler(df_quadro_area_01)

# Para salvar a tabela em HTML
html_output = styled_table._repr_html_()

with open("./pre_cri/tabela_quadro_area_02.html", "w") as file:
    file.write(html_output)
