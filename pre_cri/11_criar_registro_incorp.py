import sqlite3
import pandas as pd
from pathlib import Path
import locale


def connect_db(db_path='./pre_cri/base_real.db'):
    """Estabelece conexão com o banco de dados."""
    return sqlite3.connect(db_path)

def get_preliminary_info(conn):
    """Obtém informações preliminares da incorporação."""
    query = """
    SELECT 
        nome_incorporador,
        cnpj_incorporador,
        nome_edificio,
        quantidade_unidades_autonomas,
        area_lote,
        numero_alvara_projeto
    FROM informacoes_preliminares
    LIMIT 1
    """
    return pd.read_sql_query(query, conn).iloc[0]

def get_total_area(conn):
    """Obtém a área total construída do alvará."""
    query = """
    SELECT 
        outras_areas_total_global as area_total
    FROM alvara
    LIMIT 1
    """
    return pd.read_sql_query(query, conn).iloc[0]['area_total']

def get_global_cost(conn):
    """Obtains the global cost of construction."""
    query = """
    SELECT valor 
    FROM quadro_area_03 
    WHERE ROWID = 67
    """
    result = pd.read_sql_query(query, conn)
    if not result.empty and result.iloc[0]['valor'] is not None:
        valor = result.iloc[0]['valor']
        # Ensure 'valor' is a float
        valor = float(str(valor).replace(' ', ''))
        return valor
    return None



def format_brazilian_currency(value):
    """Formats a number to the Brazilian currency standard (e.g., 1.234,56)."""
    if value is None:
        return None

    # Attempt to convert value directly to float
    try:
        value = float(str(value).replace(' ', ''))
    except ValueError:
        # If direct conversion fails, handle Brazilian format
        try:
            value_clean = str(value).replace('.', '').replace(',', '.').replace(' ', '')
            value = float(value_clean)
        except ValueError:
            return None  # Could not parse value

    # Format the number to two decimal places
    parts = f"{value:.2f}".split('.')

    # Format the integer part with periods
    integer_part = ""
    for i, digit in enumerate(reversed(parts[0])):
        if i != 0 and i % 3 == 0:
            integer_part = '.' + integer_part
        integer_part = digit + integer_part

    # Return the formatted number with a comma as the decimal separator
    return f"{integer_part},{parts[1]}"






def get_subcondominios_summary(conn):
    """Obtém o resumo dos subcondomínios do quadro_resumo."""
    query = """
    WITH subcondominio_counts AS (
        SELECT 
            subcondominio,
            COUNT(DISTINCT unidade_numero) as total_unidades
        FROM quadro_resumo
        GROUP BY subcondominio
    )
    SELECT 
        subcondominio,
        total_unidades
    FROM subcondominio_counts
    ORDER BY subcondominio
    """
    return pd.read_sql_query(query, conn)



def clean_unit_description(text):
    """
    Limpa a formatação do texto, removendo quebras de linha desnecessárias
    e mantendo apenas a estrutura essencial.
    """
    # Divide o texto em linhas
    lines = text.strip().split('\n')
    cleaned_lines = []
    current_line = []
    
    for line in lines:
        line = line.strip()
        if not line:  # Linha vazia
            if current_line:
                cleaned_lines.append(' '.join(current_line))
                current_line = []
            cleaned_lines.append('')
        elif line.startswith('APARTAMENTO') or line.startswith('LOJA') or line.startswith('VAGA'):
            # Se já temos uma linha atual, salvamos ela primeiro
            if current_line:
                cleaned_lines.append(' '.join(current_line))
                current_line = []
            cleaned_lines.append(line)
        else:
            # Remove caracteres especiais de formatação
            line = line.replace('|', '').strip()
            if line:
                current_line.append(line)
    
    # Adiciona a última linha se existir
    if current_line:
        cleaned_lines.append(' '.join(current_line))
    
    # Junta as linhas com a formatação adequada
    final_text = []
    for line in cleaned_lines:
        if line.startswith(('APARTAMENTO', 'LOJA', 'VAGA')):
            if final_text:  # Adiciona uma linha em branco antes de nova seção
                final_text.append('')
            final_text.append(line)
        elif line:  # Linha não vazia que não é cabeçalho
            final_text.append(line)
    
    return ' '.join(final_text)

def read_unit_descriptions():
    """Lê as descrições das unidades dos arquivos preexistentes."""
    base_path = Path('./pre_cri/output')
    
    unit_texts = []
    
    # Lista de arquivos a serem lidos
    files = [
        ('tipos_apartamentos.txt', 'APARTAMENTOS'),
        ('tipos_lojas.txt', 'LOJAS'),
        ('tipos_vagas.txt', 'VAGAS')
    ]
    
    for filename, section_title in files:
        file_path = base_path / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:  # Só adiciona se houver conteúdo
                    cleaned_content = clean_unit_description(content)
                    unit_texts.append(f"\n{section_title}\n{cleaned_content}")
    
    return "\n".join(unit_texts)

def generate_incorporation_text(db_path='./pre_cri/base_real.db'):
    """Generates the complete incorporation registry text."""
    conn = connect_db(db_path)
    
    # Retrieve all necessary information
    info = get_preliminary_info(conn)
    area_total = get_total_area(conn)
    subcondominios = get_subcondominios_summary(conn)
    custo_global = get_global_cost(conn)
    
    # Format the subcondominiums text
    subcondominio_text = "\n".join([
        f"({i+1}) {row.subcondominio}: {row.total_unidades} unidades,"
        for i, row in subcondominios.iterrows()
    ])
    
    # Read unit descriptions from files
    units_text = read_unit_descriptions()
    
    # Prepare the global cost text
    if custo_global is not None:
        custo_formatado = format_brazilian_currency(custo_global)
        custo_text = f"CUSTO GLOBAL DA CONSTRUÇÃO - O custo global da construção será de R$ {custo_formatado}"
    else:
        custo_text = "CUSTO GLOBAL DA CONSTRUÇÃO - O custo global da construção será apurado ao final da obra"
    
    # Assemble the complete text
    incorporation_text = f"""INCORPORAÇÃO) -
À vista do que consta no memorial de incorporação subscrito pela firma {info.nome_incorporador} ({info.cnpj_incorporador}),
memorial esse que fica arquivado nesta Serventia sob nº [PROTOCOLO]-I, procedo este registro para consignar que no terreno a que se refere esta matrícula será construído 
sob o regime de incorporação, nos termos da Lei nº 4.591/64 e posteriores alterações, um condomínio a ser denominado "{info.nome_edificio}", 
aprovado pelo Alvará nº {info.numero_alvara_projeto}, com a área total a ser construída de {area_total}m², 
será composto de unidades autônomas de propriedade exclusiva e partes comuns, divididas em {len(subcondominios)} subcondomínios:
{subcondominio_text}
que serão assim identificadas e caracterizadas:
UNIDADES AUTONOMAS: {units_text} PRAZO DE CARÊNCIA - Não há prazo de carência; {custo_text}

[[DADOS DO CRI]]
[Dados do CRI serão preenchidos pelo cartório]"""
    
    conn.close()
    return incorporation_text



def save_incorporation_text(text, output_path='./pre_cri/output/registro_incorporacao.txt'):
    """Salva o texto do registro em um arquivo."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    try:
        texto = generate_incorporation_text()
        save_incorporation_text(texto)
        print("Arquivo de registro de incorporação gerado com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar o registro: {str(e)}")