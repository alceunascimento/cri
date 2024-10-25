import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_02
query = "SELECT * FROM quadro_area_02"
df_quadro_area_02 = pd.read_sql_query(query, conn)

# Remover a coluna 'ROWID' se ela estiver presente
if 'ROWID' in df_quadro_area_02.columns:
    df_quadro_area_02 = df_quadro_area_02.drop(columns=['ROWID'])

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
    ("", "", "", "subcondominio", ""),
    ("", "", "", "unidade_tipo", "19"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO", "", "20"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "21"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "22"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "REAL", "23"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA PRIVATIVA", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "24"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "", "25"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "26"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "27"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL", "28"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "29"),
    ("ÁREA DE DIVISÃO NÃO PROPORCIONAL", "ÁREA DE USO COMUM", "", "AREA TOTAL EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "30"),
    ("", "", "", "Coeficiente de proporcionalidade", "31"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO", "", "32"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "REAL", "33"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "COBERTA PADRÃO DIFERENTE OU DESCOBERTA", "EQUIVALENTE", "34"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "REAL", "35"),
    ("ÁREA DE DIVISÃO PROPORCIONAL", "ÁREA DE USO COMUM", "TOTAIS", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "36"),
    ("ÁREA DA UNIDADE", "", "", "REAL", "37"),
    ("ÁREA DA UNIDADE", "", "", "EQUIVALENTE EM ÁREA DE CUSTO PADRÃO", "38"),
    ("QUANTIDADE", "", "", "(Número de unidades idênticas)")
])

# Atribuir o novo cabeçalho ao dataframe
df_quadro_area_02.columns = columns[:len(df_quadro_area_02.columns)]  # Ajuste dinâmico para garantir compatibilidade

# Extraindo a coluna 'Quantidade' sem o MultiIndex para garantir o alinhamento
quantidade_col = df_quadro_area_02[('QUANTIDADE', '', '', '(Número de unidades idênticas)')].values

# Selecionar as colunas numéricas para multiplicação, exceto a coluna 'Quantidade'
# Aqui garantimos que apenas colunas numéricas sejam consideradas
numeric_cols = df_quadro_area_02.drop(columns=[('', '', '', 'unidade_tipo', '19'), ('QUANTIDADE', '', '', '(Número de unidades idênticas)')])
numeric_cols = numeric_cols.apply(pd.to_numeric, errors='coerce')  # Forçar a conversão para numérico

# Aplicar a multiplicação para cada valor das colunas numéricas pelo valor da coluna `Quantidade`
df_multiplicado = numeric_cols.mul(quantidade_col, axis=0)

# Calcular a soma das colunas multiplicadas
sum_row = df_multiplicado.sum(numeric_only=True)  # Somente colunas numéricas

# Adicionar a coluna de Subcondomínio com valor "Total" na linha de somatório
sum_row[('', '', '', 'subcondominio', '1')] = str("Total")

# Adicionar a linha de somatório ao dataframe original
df_quadro_area_02.loc['Total'] = sum_row

# Agora calcular a soma da coluna 'Quantidade' separadamente
soma_quantidade = df_quadro_area_02[('QUANTIDADE', '', '', '(Número de unidades idênticas)')].sum()

# Substituir o valor da coluna 'Quantidade' na linha de somatório
df_quadro_area_02.at['Total', ('QUANTIDADE', '', '', '(Número de unidades idênticas)')] = soma_quantidade

# Formatar os dados usando pandas Styler
def format_styler(df):
    styler = df.style.set_caption("QUADRO 02 - ÁREA DE DIVISÃO").set_table_styles(
        [
            {'selector': 'thead th', 'props': [('background-color', 'lightgrey'), ('text-align', 'center'), ('font-weight', 'bold')]},
            {'selector': 'tbody td', 'props': [('border', '1px solid black'), ('text-align', 'right')]}
        ]
    ).format(na_rep='-', precision=8)
    
    return styler

# Aplicar a formatação
styled_table = format_styler(df_quadro_area_02)

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
            QUADRO II - Cálculo das Áreas nos Pavimentos e da Área Global - Colunas 19 a 38
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
        <td style="border: 1px solid black;"></td>
        <td style="border: 1px solid black;">{responsavel_tecnico} ({registro_crea})</td>
        <td style="border: 1px solid black;"></td>
    </tr>
</table>
"""

# Gerar o conteúdo completo em HTML, unindo o cabeçalho e a tabela formatada
html_output = html_cabecalho + styled_table._repr_html_()

# Salvar o conteúdo completo em um arquivo HTML
with open("./pre_cri/tabela_quadro_area_02_com_cabecalho.html", "w") as file:
    file.write(html_output)

print("Arquivo HTML gerado com sucesso.")
