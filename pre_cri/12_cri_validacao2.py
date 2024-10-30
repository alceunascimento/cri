import sqlite3
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

def connect_db(db_path='./pre_cri/base_real.db'):
    """Estabelece conexão com o banco de dados."""
    return sqlite3.connect(db_path)

def round_decimal(value, places=2):
    """Arredonda um número para um determinado número de casas decimais."""
    if value is None:
        return None
    return Decimal(str(value)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def get_areas_info(conn):
    """Obtém informações sobre áreas do empreendimento."""
    # Query para área do terreno
    area_terreno_df = pd.read_sql_query("""
        SELECT area_lote as valor
        FROM informacoes_preliminares 
        LIMIT 1
    """, conn)
    area_terreno = area_terreno_df.iloc[0]['valor'] if not area_terreno_df.empty else None

    # Query para área total construída
    area_total_df = pd.read_sql_query("""
        SELECT (areas_computaveis_total + areas_nao_computaveis_total + 
                areas_recreacao_total + outras_areas_total_global) as valor
        FROM alvara
        LIMIT 1
    """, conn)
    area_total = area_total_df.iloc[0]['valor'] if not area_total_df.empty else None

    # Query para soma das quotas de terreno
    quotas_df = pd.read_sql_query("""
        SELECT SUM(quota_terreno) as valor
        FROM quadro_resumo
    """, conn)
    soma_quotas = quotas_df.iloc[0]['valor'] if not quotas_df.empty else None

    return {
        'area_terreno': area_terreno,
        'area_total_construida': area_total,
        'soma_quotas': soma_quotas
    }

def check_area_terreno(conn):
    """A.1. Verifica se a área do terreno é consistente."""
    areas = get_areas_info(conn)
    area_terreno = areas.get('area_terreno')
    if area_terreno is not None:
        return f"A.1. PENDENTE - Área do terreno no memorial: {area_terreno:.2f}m². " \
               f"Necessário comparar com a matrícula."
    return "A.1. ERRO - Não foi possível obter a área do terreno"

def check_soma_quotas(conn):
    """A.2. Verifica se a soma das quotas de terreno é igual à área do terreno."""
    areas = get_areas_info(conn)
    area_terreno = areas.get('area_terreno')
    soma_quotas = areas.get('soma_quotas')
    
    if area_terreno is None or soma_quotas is None:
        return "A.2. ERRO - Não foi possível obter os dados necessários"
    
    diferenca = abs(area_terreno - soma_quotas)
    
    if round_decimal(diferenca) == 0:
        return f"A.2. SIM - A soma das quotas de terreno ({soma_quotas:.2f}m²) " \
               f"é igual à área do terreno ({area_terreno:.2f}m²)"
    else:
        return f"A.2. NÃO - Há uma diferença de {diferenca:.2f}m² entre a soma das quotas " \
               f"e a área do terreno"

def check_regime_vagas(conn):
    """A.4. Verifica se há indicação do regime jurídico das vagas."""
    df = pd.read_sql_query("""
        SELECT DISTINCT tipo_vaga 
        FROM cri 
        WHERE tipo_vaga IS NOT NULL
    """, conn)
    if not df.empty:
        tipos = ', '.join(df['tipo_vaga'].tolist())
        return f"A.4. SIM - Regime jurídico das vagas está indicado: {tipos}"
    return "A.4. NÃO - Não há indicação do regime jurídico das vagas"

def check_fracao_ideal_soma(conn):
    """B.5. Verifica se a soma das frações ideais é igual a 1."""
    df = pd.read_sql_query("""
        SELECT SUM(fracao_ideal_solo_condominio) as soma_fracoes
        FROM quadro_resumo
    """, conn)
    
    if df.empty or df.iloc[0]['soma_fracoes'] is None:
        return "B.5. ERRO - Não foi possível calcular a soma das frações ideais"
    
    soma = df.iloc[0]['soma_fracoes']
    if round_decimal(soma - 1, 6) == 0:
        return f"B.5. SIM - A soma das frações ideais é 1 (valor exato: {soma:.6f})"
    else:
        return f"B.5. NÃO - A soma das frações ideais é {soma:.6f}"

def check_unidades_por_pavimento(conn):
    """B.18. Lista as unidades por pavimento."""
    df = pd.read_sql_query("""
        SELECT pavimento, GROUP_CONCAT(unidade_numero) as unidades
        FROM cri
        WHERE pavimento IS NOT NULL
        GROUP BY pavimento
        ORDER BY pavimento
    """, conn)
    
    if df.empty:
        return "B.18. ERRO - Não foi possível obter as unidades por pavimento"
    
    result = "B.18. Unidades por pavimento:\n"
    for _, row in df.iterrows():
        result += f"Pavimento {row['pavimento']}: {row['unidades']}\n"
    return result

def check_alvara_numero(conn):
    """B.20. Verifica se consta o número do alvará."""
    df = pd.read_sql_query("""
        SELECT numero_alvara_projeto
        FROM informacoes_preliminares
        LIMIT 1
    """, conn)
    
    if not df.empty and not pd.isna(df.iloc[0]['numero_alvara_projeto']):
        return f"B.20. SIM - Número do alvará: {df.iloc[0]['numero_alvara_projeto']}"
    return "B.20. NÃO - Não consta o número do alvará"

def check_numeros_sequenciais(conn):
    """B.19. Verifica se a numeração das unidades é sequencial."""
    try:
        df = pd.read_sql_query("""
            SELECT subcondominio,
                   MIN(CAST(unidade_numero AS INTEGER)) as inicio,
                   MAX(CAST(unidade_numero AS INTEGER)) as fim
            FROM quadro_resumo
            GROUP BY subcondominio
        """, conn)
        
        if df.empty:
            return "B.19. ERRO - Não foi possível obter dados das unidades"
        
        result = "B.19. Análise de sequência numérica por subcondomínio:\n"
        
        for _, row in df.iterrows():
            inicio = row['inicio']
            fim = row['fim']
            subcondominio = row['subcondominio']
            
            numeros_df = pd.read_sql_query(f"""
                SELECT unidade_numero
                FROM quadro_resumo
                WHERE subcondominio = ?
                ORDER BY CAST(unidade_numero AS INTEGER)
            """, conn, params=[subcondominio])
            
            numeros_existentes = set([int(x) for x in numeros_df['unidade_numero']])
            numeros_esperados = set(range(inicio, fim + 1))
            numeros_ausentes = numeros_esperados - numeros_existentes
            
            if numeros_ausentes:
                result += f"{subcondominio}: Início {inicio}, Fim {fim}, NÃO sequencial\n"
                result += f"Números ausentes: {sorted(numeros_ausentes)}\n"
            else:
                result += f"{subcondominio}: Início {inicio}, Fim {fim}, sequencial\n"
                
        return result
    except Exception as e:
        return f"B.19. ERRO - Erro ao verificar sequência numérica: {str(e)}"


# [Código anterior permanece igual...]

def check_fracao_ideal_por_subcondominio(conn):
    """
    B.6. Verifica se a soma das frações ideais por subcondomínio é igual a 1.
    """
    # Query para obter dados detalhados
    query_detalhes = """
    SELECT 
        subcondominio,
        unidade_tipo as tipo,
        COUNT(*) as quantidade,
        SUM(fracao_ideal_solo_subcondominio) as soma_fracoes
    FROM quadro_resumo
    GROUP BY subcondominio, unidade_tipo
    ORDER BY subcondominio, unidade_tipo
    """
    
    df_detalhes = pd.read_sql_query(query_detalhes, conn)
    
    if df_detalhes.empty:
        return "B.6. ERRO - Não foi possível obter as frações ideais por subcondomínio"
    
    # Query para obter subtotais
    query_subtotais = """
    SELECT 
        subcondominio,
        SUM(fracao_ideal_solo_subcondominio) as subtotal
    FROM quadro_resumo
    GROUP BY subcondominio
    ORDER BY subcondominio
    """
    
    df_subtotais = pd.read_sql_query(query_subtotais, conn)
    
    # Gera o relatório
    result = ["B.6. Verificação da soma das frações ideais por subcondomínio:"]
    
    # Formato da linha da tabela
    header = "{:<15}|{:<20}|{:<20}"
    linha = "{:<15}|{:<20}|{:20.8f}"
    linha_subtotal = "\nSubtotal{:<38}{:.8f}\n"
    separador = "-" * 56
    
    # Para cada subcondomínio
    for subcondominio in sorted(df_detalhes['subcondominio'].unique()):
        result.append(f"\n\nSubcondomínio: {subcondominio}")
        result.append(separador)
        result.append(header.format("subcondominio", "tipo", "fração ideal solo"))
        result.append(separador)
        
        # Dados do subcondomínio
        dados_sub = df_detalhes[df_detalhes['subcondominio'] == subcondominio]
        for _, row in dados_sub.iterrows():
            result.append(linha.format(
                subcondominio if _ == 0 else "",  # Só mostra o nome no primeiro
                f"{row['tipo']} ({row['quantidade']})",
                row['soma_fracoes']
            ))
        
        # Adiciona subtotal
        subtotal = df_subtotais[df_subtotais['subcondominio'] == subcondominio]['subtotal'].iloc[0]
        result.append(separador)
        result.append(linha_subtotal.format("", subtotal))
    
    # Conclusão
    todos_corretos = all(abs(row['subtotal'] - 1) < 0.000001 for _, row in df_subtotais.iterrows())
    
    result.append("\nCONCLUSÃO:")
    if todos_corretos:
        result.append("SIM. Todos os subcondomínios têm soma de frações ideais igual a 1.")
    else:
        result.append("NÃO. Há subcondomínios com soma de frações ideais diferente de 1.")
        
    return "\n".join(result)



def generate_checklist(db_path='./pre_cri/base_real.db'):
    """Gera o relatório completo do checklist."""
    conn = connect_db(db_path)
    
    checklist = [
        "CHECKLIST DE ANÁLISE DA INCORPORAÇÃO\n",
        "=====================================\n",
        "\nA. QUESTÕES DEFINIDAS PELA LEGISLAÇÃO\n",
        check_area_terreno(conn),
        check_soma_quotas(conn),
        "A.3. PENDENTE - Comparação com projeto arquitetônico não disponível",
        check_regime_vagas(conn),
        "\nB. QUESTÕES DEFINIDAS PELO CRI\n",
        check_fracao_ideal_soma(conn),
        check_fracao_ideal_por_subcondominio(conn),  # Nova verificação adicionada
        check_unidades_por_pavimento(conn),
        check_numeros_sequenciais(conn),
        check_alvara_numero(conn)
    ]
    
    conn.close()
    return "\n\n".join(checklist)

# [Resto do código permanece igual...]



def save_checklist(text, output_path='./pre_cri/output/checklist_incorporacao.txt'):
    """Salva o checklist em um arquivo."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    try:
        checklist = generate_checklist()
        save_checklist(checklist)
        print("Checklist de incorporação gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o checklist: {str(e)}")