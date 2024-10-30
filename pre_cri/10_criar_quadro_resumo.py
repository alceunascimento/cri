import sqlite3
import pandas as pd

# Conectar ao banco de dados
db_path = './pre_cri/base_real.db'
conn = sqlite3.connect(db_path)


# Buscar as informações da tabela informacoes_preliminares
query = """
SELECT nome_incorporador, nome_responsavel_tecnico, registro_crea, local_construcao, nome_edificio, cidade_uf
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
cidade_uf = result['cidade_uf']



# Carregar os dados da tabela quadro_resumo com os nomes corretos das colunas
query = """
SELECT 
    subcondominio,
    unidade_tipo as tipo,
    area_alvara_privativa,
    area_alvara_deposito_vinculado,
    area_alvara_comum,
    area_alvara_total,
    fracao_ideal_solo_subcondominio,
    area_comum_descoberta,
    area_total,
    fracao_ideal_solo_condominio,
    quota_terreno,
    unidade_numero
FROM quadro_resumo
"""


df_quadro_resumo = pd.read_sql_query(query, conn)


# Criar as colunas hierárquicas depois de carregar os dados corretamente
columns = pd.MultiIndex.from_tuples([
    ("", "", "SUBCONDOMÍNIO"),
    ("", "", "TIPO"),
    ("ÁREAS DO ALVARÁ", "", "ÁREA PRIVATIVA"),
    ("ÁREAS DO ALVARÁ", "", "DEPÓSITO VINCULADO"),
    ("ÁREAS DO ALVARÁ", "", "ÁREA COMUM"),
    ("ÁREAS DO ALVARÁ", "", "TOTAL ALVARÁ"),
    ("ÁREAS DO ALVARÁ", "", "FRAÇÃO SUBCONDOMÍNIO"),
    ("", "", "ÁREA COMUM DESCOBERTA"),
    ("", "", "ÁREA TOTAL (COB+DESC)"),
    ("", "", "FRAÇÃO IDEAL DE SOLO"),
    ("", "", "QUOTA DE TERRENO"),
    ("", "", "NÚMERO DA UNIDADE")
])


# Reorganizar as colunas do DataFrame para corresponder ao MultiIndex
df_quadro_resumo.columns = columns




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
styled_table = format_styler(df_quadro_resumo)




# ...

# Calcular o subtotal das colunas desejadas
subtotal = df_quadro_resumo.sum(numeric_only=True)

# Adicionar a linha de subtotais diretamente ao DataFrame original usando loc
df_quadro_resumo.loc["Subtotal"] = subtotal

# Preencher as colunas não calculadas com "-"
df_quadro_resumo.loc["Subtotal", ("", "", "SUBCONDOMÍNIO")] = "-"
df_quadro_resumo.loc["Subtotal", ("", "", "TIPO")] = "Total"
df_quadro_resumo.loc["Subtotal", ("ÁREAS DO ALVARÁ", "", "FRAÇÃO SUBCONDOMÍNIO")] = "-"
df_quadro_resumo.loc["Subtotal", ("", "", "NÚMERO DA UNIDADE")] = "-"



# Aplicar a formatação à tabela atualizada
styled_table = format_styler(df_quadro_resumo)

# ...


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
            QUADRO RESUMO
        </td>
    </tr>
    <tr>
        <td style="border: 1px solid black;">Local do Imóvel: {local_construcao}, {cidade_uf}</td>
        <td style="border: 1px solid black;">FOLHA ÚNICA</td>
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
with open("./pre_cri/output/nbr_00_quadro_resumo.html", "w") as file:
    file.write(html_output)


conn.close()
 
print("Arquivo HTML gerado com sucesso.")

