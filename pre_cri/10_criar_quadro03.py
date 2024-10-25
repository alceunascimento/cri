import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)

# Carregar os dados da tabela quadro_area_03
query = "SELECT * FROM quadro_area_03"
df_quadro_area_03 = pd.read_sql_query(query, conn)

# Verificar todas as colunas disponíveis na tabela
print(df_quadro_area_03.columns)

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

# Montar o conteúdo do cabeçalho em HTML
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
            QUADRO III - Avaliação do Custo Global e Unitário da Construção
        </td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Local do Imóvel: {local_construcao}</td>
        <td style="border: 1px solid black;">Folha 4</td>
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

# Gerar a tabela usando pandas Styler para aplicar o estilo correto
def format_styler(df):
    styler = df.style.set_caption("QUADRO III - Avaliação do Custo Global e Unitário da Construção").set_table_styles(
        [
            {'selector': 'thead th', 'props': [('background-color', 'lightgrey'), ('text-align', 'center'), ('font-weight', 'bold')]},
            {'selector': 'tbody td', 'props': [('border', '1px solid black'), ('text-align', 'right')]}
        ]
    ).format(na_rep='-', precision=2)  # Ajuste de precisão se necessário
    
    return styler

# Aplicar a formatação na tabela
styled_table = format_styler(df_quadro_area_03)

# Gerar o conteúdo completo em HTML, unindo o cabeçalho e a tabela formatada
html_output = html_cabecalho + styled_table._repr_html_()

# Salvar o conteúdo completo em um arquivo HTML
with open("./pre_cri/tabela_quadro_area_03_com_cabecalho.html", "w") as file:
    file.write(html_output)

print("Arquivo HTML gerado com sucesso.")
