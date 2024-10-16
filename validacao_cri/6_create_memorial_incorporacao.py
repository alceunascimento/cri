import sqlite3

# Função para gerar o texto do memorial descritivo com base nos dados do banco de dados
def gerar_memorial_descritivo(row):
    # Começar a formatar o texto para o memorial descritivo
    memorial = (
        f"{row['especie'].upper()} {row['unidades']}: "
        f"possuindo esta unidade as seguintes áreas construídas: " 
        f"área privativa de {row['area_privativa']:.6f} metros quadrados, "
        f"área comum de {row['area_comum']:.6f} metros quadrados, "
        f"perfazendo a área construída de {row['area_total_global_coberta_e_descoberta']:.6f} metros quadrados; "
        f"cabendo-lhe, a fração ideal de solo e partes comuns de {row['fracao_ideal_condominio']:.8f} "
        f"e quota de terreno de {row['cota_terreno']:.6f} metros quadrados. "
        f"Possuindo, ainda, direito de uso das seguintes áreas descobertas: "
    )

    # Verificar se `area_privativa_vinculada_deposito` é maior que 0
    if row['area_privativa_vinculada_deposito'] > 0:
        memorial += f"área privativa de {row['area_privativa_vinculada_deposito']:.6f} metros quadrados e "

    # Verificar se `area_comum_descoberta_recreacao` é maior que 0
    if row['area_comum_descoberta_recreacao'] > 0:
        memorial += f"recreação comum descoberta de {row['area_comum_descoberta_recreacao']:.6f} metros quadrados. "

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
conn = sqlite3.connect('./data/base_cris_desagregado.db')

# Definir o cursor para execução de comandos SQL
cursor = conn.cursor()

# Selecionar os dados relevantes da tabela 'unidades'
cursor.execute("""
    SELECT 
        unidades, especie, pavimento, area_privativa, area_comum, area_total_global_coberta_e_descoberta, 
        fracao_ideal_condominio, cota_terreno, area_privativa_vinculada_deposito, 
        area_comum_descoberta_recreacao, confrontacao_frente, confrontacao_direita, 
        confrontacao_esquerda, confrontacao_fundos
    FROM unidades
    ORDER BY 
        CASE 
            WHEN especie = 'LOJA' THEN 1
            WHEN especie = 'APARTAMENTO' THEN 2
            WHEN especie = 'VAGA' THEN 3
        END,
        CAST(unidades AS INTEGER);
""")

# Recuperar todos os dados em uma lista de dicionários
rows = cursor.fetchall()
colunas = [col[0] for col in cursor.description]
dados = [dict(zip(colunas, row)) for row in rows]

# Fechar a conexão com o banco de dados
conn.close()

# Gerar o memorial descritivo para cada unidade
memoriais = [gerar_memorial_descritivo(row) for row in dados]

# Salvar o memorial descritivo em um arquivo de texto
with open('./producao_minima/memorial_descritivo.txt', 'w') as f:
    for memorial in memoriais:
        f.write(memorial + "\n")

print("Memorial descritivo gerado com sucesso e salvo em '/producao_minima/memorial_descritivo.txt'.")
