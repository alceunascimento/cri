import sqlite3
from fpdf import FPDF

# Função para gerar o texto do memorial descritivo com base nos dados do banco de dados
def gerar_memorial_descritivo(row):
    # Começar a formatar o texto para o memorial descritivo
    especie = row['especie_unidade']
    if especie is None:
        especie_formatado = "ESPECIE NÃO DEFINIDA"
    else:
        especie_formatado = especie.upper()

    memorial = (
        f"{especie_formatado} {row['unidade_numero']}: "
        f"possuindo esta unidade as seguintes áreas construídas: " 
        f"área privativa de {row['area_privativa']:.6f} metros quadrados, "
        f"área comum de {row['area_comum']:.6f} metros quadrados, "
        f"perfazendo a área construída de {row['area_total_construida']:.6f} metros quadrados; "
        f"cabendo-lhe, a fração ideal de solo e partes comuns de {row['fracao_ideal_solo_condominio']:.8f} "
        f"e quota de terreno de {row['quota_terreno_condominio']:.6f} metros quadrados. "
        f"Possuindo, ainda, direito de uso das seguintes áreas descobertas: "
    )
    
    # Verificar se `area_privativa_vinculada_deposito` é maior que 0
    if row['area_vinculada_outras'] and row['area_vinculada_outras'] > 0:
        memorial += f"área privativa de {row['area_vinculada_outras']:.6f} metros quadrados e "

    # Verificar se `area_comum_descoberta_recreacao` é maior que 0
    if row['area_comum_descoberta'] and row['area_comum_descoberta'] > 0:
        memorial += f"recreação comum descoberta de {row['area_comum_descoberta']:.6f} metros quadrados. "

    # Continuar o texto do memorial
    memorial += (
        f"Localização: localiza-se no {row['pavimento']}º pavimento, "
        f"sendo que para quem entra no apartamento pelo elevador, confronta " 
        f"pela frente com {row['confrontacao_frente']}, "
        f"pelo lado direito com {row['confrontacao_direita']}, "
        f"pelo lado esquerdo com {row['confrontacao_esquerda']} "
        f"e pelo fundo com {row['confrontacao_fundos']}.\n"
    )
    return memorial

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('./cri/base_cri.db')

# Definir o cursor para execução de comandos SQL
cursor = conn.cursor()

# Selecionar os dados relevantes da tabela 'unidades'
cursor.execute("""
    SELECT 
        unidade_numero, especie_unidade, pavimento, area_privativa, area_comum, area_total_construida, 
        fracao_ideal_solo_condominio, quota_terreno_condominio, area_vinculada_outras, 
        area_comum_descoberta, confrontacao_frente, confrontacao_direita, 
        confrontacao_esquerda, confrontacao_fundos
    FROM cri
    ORDER BY 
        CASE 
            WHEN especie_unidade = 'LOJA' THEN 1
            WHEN especie_unidade = 'APARTAMENTO' THEN 2
            WHEN especie_unidade = 'VAGA' THEN 3
        END,
        CAST(unidade_numero AS INTEGER);
""")

# Recuperar todos os dados em uma lista de dicionários
rows = cursor.fetchall()
colunas = [col[0] for col in cursor.description]
dados = [dict(zip(colunas, row)) for row in rows]

# Fechar a conexão com o banco de dados
conn.close()

# Gerar o memorial descritivo para cada unidade
memoriais = [gerar_memorial_descritivo(row) for row in dados]

# Obter os dados para o cabeçalho da tabela 'alvara'
conn = sqlite3.connect('./cri/base_cri.db')
cursor = conn.cursor()
cursor.execute("SELECT interessado, localizacao FROM alvara LIMIT 1;")
alvara = cursor.fetchone()
conn.close()

# Salvar o memorial descritivo em um arquivo de texto com o cabeçalho
e_protocolo = "ACxxxxxxxxxx"
cabecalho = (
    "Relatório de Documento Eletrônico em XML\n"
    "Extrato - Registro de Incorporação\n"
    f"e-Protocolo N°: {e_protocolo}\n"
    "Apresentante / Contato\n"
    f"Incorporador: {alvara[0]}\n"
    f"Endereço: {alvara[1]}\n"
    "___________________________________________________________________\n"
    f"Apresentante: {alvara[0]}\n"
    "CNPJ: \n"
    "Endereço: \n"
    "E-mail: \n"
    "Dados do Título\n"
    "Natureza: Memorial Descritivo\n"
    "Local: Curitiba\n"
    "Data em que foi firmado: [x]\n"
    "Memorial de Incorporação\n"
)

# Salvar o memorial descritivo em um arquivo de texto
with open('./cri/memorial_descritivo_unidades.txt', 'w') as f:
    f.write(cabecalho + "\n")
    for memorial in memoriais:
        f.write(memorial + "\n")
        
# Salvar o memorial descritivo em um arquivo PDF
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.multi_cell(0, 10, cabecalho)
for memorial in memoriais:
    pdf.multi_cell(0, 10, memorial)
pdf.output("./cri/memorial_descritivo_unidades.pdf")

print("Memorial descritivo gerado com sucesso e salvo em '/cri/memorial_descritivo.txt'.")