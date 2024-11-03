import sqlite3
from pathlib import Path
from datetime import datetime
from num2words import num2words
import re
import os

def format_decimal(value):
    return str(value).replace('.', ',')

def extract_numbers(s):
    nums = re.findall(r'\d+', s)
    return [int(n) for n in nums] if nums else [float('inf')]

def pluralize(word, count):
    if count == 1:
        return word
    else:
        # Simple pluralization for Portuguese
        if word.endswith('m'):
            return word[:-1] + 'ns'
        elif word.endswith('l'):
            return word[:-1] + 'is'
        elif word.endswith('ão'):
            return word[:-3] + 'ões'
        elif word.endswith('z'):
            return word + 'es'
        else:
            return word + 's'

def number_to_extenso(number):
    return num2words(number, lang='pt_BR', to='cardinal')

def get_enterprise_info(conn):
    cursor = conn.cursor()
    # Fetch necessary fields from 'cri' table
    cursor.execute("""
        SELECT
            nome_condominio,
            matricula,
            incorporador,
            responsavel_tecnico_construcao,
            responsavel_tecnico_nbr,
            edificio,
            acesso_edificio
        FROM cri
        LIMIT 1
    """)
    cri_info = cursor.fetchone()

    # Fetch 'alvara_numero' and 'alvara_data' from 'alvara' table
    cursor.execute("""
        SELECT
            numero_documento AS alvara_numero,
            data_expedicao_primeira_emissao AS alvara_data,
            outras_areas_total_global as area_total_construida
        FROM alvara
        LIMIT 1
    """)
    alvara_info = cursor.fetchone()

    # Combine the information into a single dictionary
    enterprise_info = {}
    if cri_info:
        enterprise_info.update(dict(cri_info))
    if alvara_info:
        enterprise_info.update(dict(alvara_info))

    return enterprise_info

def get_unit_counts(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT especie_unidade, COUNT(*) as count
        FROM cri
        GROUP BY especie_unidade
    """)
    return {row['especie_unidade']: row['count'] for row in cursor.fetchall()}

def get_units_by_floor(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT pavimento, especie_unidade, unidade_numero
        FROM cri
        ORDER BY pavimento, especie_unidade, unidade_numero
    """)
    units = {}
    for row in cursor.fetchall():
        floor = row['pavimento']
        unit_type = row['especie_unidade']
        unit_number = row['unidade_numero']
        units.setdefault(floor, {}).setdefault(unit_type, []).append(unit_number)
    return units

def get_addresses(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT tipo_logradouro, nome_logradouro, numero_logradouro
        FROM cri
        WHERE tipo_logradouro IS NOT NULL AND nome_logradouro IS NOT NULL AND numero_logradouro IS NOT NULL
    """)
    addresses = []
    for row in cursor.fetchall():
        address = f"{row['tipo_logradouro']} {row['nome_logradouro']}, {row['numero_logradouro']}"
        addresses.append(address)
    return addresses

def prepare_subcondominios_description(conn, unit_counts):
    descricao = []

    # Subcondominio Estacionamento
    vagas_count = unit_counts.get('VAGA', 0)
    vagas_count_extenso = number_to_extenso(vagas_count)
    vagas_capacity = calculate_parking_capacity(conn)
    vagas_capacity_extenso = number_to_extenso(vagas_capacity)
    descricao.append(f"(i) Subcondomínio Estacionamento, composto por {vagas_count} ({vagas_count_extenso}) vagas de garagem autônomas, com capacidade para estacionar {vagas_capacity} ({vagas_capacity_extenso}) veículos, o qual localizar-se-á desde o subsolo 3 até o subsolo 1, com acesso de entrada de veículos pela Alameda Doutor Carlos de Carvalho e saída de veículos pela Rua Cruz Machado. O acesso de pedestres será feito pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial")

    # Subcondominio Galeria
    lojas_count = unit_counts.get('LOJA', 0)
    lojas_count_extenso = number_to_extenso(lojas_count)
    descricao.append(f"(ii) Subcondomínio Galeria, composto por {lojas_count} ({lojas_count_extenso}) unidades de comércios e serviços vicinais designados como lojas, todas com destinação comercial, o qual localizar-se-á no térreo e mezanino, com acesso de pedestres pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial")

    # Subcondominio Residencial
    kitinetes_count = unit_counts.get('KITINETE', 0)
    kitinetes_count_extenso = number_to_extenso(kitinetes_count)
    apartamentos_count = unit_counts.get('APARTAMENTO', 0)
    apartamentos_count_extenso = number_to_extenso(apartamentos_count)
    residencial_total = kitinetes_count + apartamentos_count
    residencial_total_extenso = number_to_extenso(residencial_total)
    descricao.append(f"(iii) Subcondomínio Residencial, composto por {kitinetes_count} ({kitinetes_count_extenso}) kitinetes e {apartamentos_count} ({apartamentos_count_extenso}) apartamentos, totalizando {residencial_total} ({residencial_total_extenso}) unidades residenciais, com destinação de habitação coletiva, o qual localizar-se-á desde o 3º pavimento até o 32º pavimento, com acesso de pedestres pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial")

    return '; '.join(descricao)

def calculate_parking_capacity(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tipo_vaga, COUNT(*) as count
        FROM cri
        WHERE especie_unidade = 'VAGA'
        GROUP BY tipo_vaga
    """)
    capacity = 0
    for row in cursor.fetchall():
        if row['tipo_vaga'] == 'simples':
            capacity += row['count'] * 1
        elif row['tipo_vaga'] == 'dupla':
            capacity += row['count'] * 2
        else:
            # If 'tipo_vaga' is None or unknown, assume it's 'simples'
            capacity += row['count'] * 1
    return capacity

def prepare_lista_pisos(units_by_floor):
    floors = sorted(units_by_floor.keys(), key=extract_numbers)
    floor_list = ', '.join(floors)
    return floor_list

def prepare_pisos_descricao(units_by_floor):
    pisos_descriptions = []

    for floor in sorted(units_by_floor.keys(), key=extract_numbers):
        units = units_by_floor[floor]
        floor_description = f"{floor}: "

        for unit_type in units:
            unit_numbers = sorted(units[unit_type], key=extract_numbers)
            count = len(unit_numbers)
            count_extenso = number_to_extenso(count)
            unit_type_plural = pluralize(unit_type.lower(), count)
            unit_numbers_str = ', '.join(unit_numbers)
            floor_description += f"{count} ({count_extenso}) {unit_type_plural} sob nº {unit_numbers_str}; "

        pisos_descriptions.append(floor_description.strip())

    return ' '.join(pisos_descriptions)

# Template for the text
text_template = """
O incorporador, sobre o imóvel já descrito, construirá por sua conta e risco, por preço determinável, na forma do Artigo 43, da Lei 4.591, de 16 de dezembro de 1.964, um empreendimento denominado “{enterprise_name}”, subdividido em {num_subcondominios} ({num_subcondominios_extenso}) subcondomínios distintos: {subcondominios_descricao}. O edifício será localizado na {enderecos}, será construído em {tipo_construcao}, com área total construída de {area_total_construida}m², conforme projeto aprovado pelo Alvará de Construção nº {alvara_numero}, datado de {alvara_data}, e terá {total_pavimentos} ({total_pavimentos_extenso}) pisos: {lista_pisos}. Os pisos do edifício estarão assim distribuídos: {pisos_descricao}
"""

def main():
    conn = sqlite3.connect('./pre_cri/base_real.db')
    conn.row_factory = sqlite3.Row

    try:
        enterprise_info = get_enterprise_info(conn)
        unit_counts = get_unit_counts(conn)
        units_by_floor = get_units_by_floor(conn)
        addresses = get_addresses(conn)

        # Prepare data for the template
        enterprise_name = enterprise_info['nome_condominio'] if enterprise_info and enterprise_info['nome_condominio'] else 'NOME DO EMPREENDIMENTO'
        num_subcondominios = 3
        num_subcondominios_extenso = number_to_extenso(num_subcondominios)
        tipo_construcao = 'alvenaria e estrutura em concreto armado'

        area_total_construida = format_decimal(enterprise_info['area_total_construida']) if enterprise_info and enterprise_info['area_total_construida'] else '0,00'

        alvara_numero = enterprise_info['alvara_numero'] if enterprise_info and 'alvara_numero' in enterprise_info and enterprise_info['alvara_numero'] else 'NÚMERO DO ALVARÁ'
        alvara_data = enterprise_info['alvara_data'] if enterprise_info and 'alvara_data' in enterprise_info and enterprise_info['alvara_data'] else 'DATA DO ALVARÁ'

        if alvara_data != 'DATA DO ALVARÁ':
            try:
                # Try parsing the date in 'dd/mm/yyyy' format
                parsed_date = datetime.strptime(alvara_data, '%d/%m/%Y')
            except ValueError:
                try:
                    # If that fails, try 'yyyy-mm-dd' format
                    parsed_date = datetime.strptime(alvara_data, '%Y-%m-%d')
                except ValueError:
                    # If parsing fails, keep the date as is
                    parsed_date = None
            if parsed_date:
                alvara_data = parsed_date.strftime('%d/%m/%Y')
            else:
                # If parsing failed, use the original date string
                pass

        total_pavimentos = len(units_by_floor)
        total_pavimentos_extenso = number_to_extenso(total_pavimentos)

        enderecos = '; '.join(addresses)

        subcondominios_descricao = prepare_subcondominios_description(conn, unit_counts)
        lista_pisos = prepare_lista_pisos(units_by_floor)
        pisos_descricao = prepare_pisos_descricao(units_by_floor)

        # Fill in the template
        text = text_template.format(
            enterprise_name=enterprise_name,
            num_subcondominios=num_subcondominios,
            num_subcondominios_extenso=num_subcondominios_extenso,
            subcondominios_descricao=subcondominios_descricao,
            area_total_construida=area_total_construida,
            alvara_numero=alvara_numero,
            alvara_data=alvara_data,
            total_pavimentos=total_pavimentos,
            total_pavimentos_extenso=total_pavimentos_extenso,
            lista_pisos=lista_pisos,
            enderecos=enderecos,
            tipo_construcao=tipo_construcao,
            pisos_descricao=pisos_descricao
        )

        print(text)
        
                # Write the text to './pre_cri/output/edificio.txt'
        output_dir = './pre_cri/output'
        output_file = os.path.join(output_dir, 'edificio.txt')

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text.strip())

        print(f"Arquivo '{output_file}' criado com sucesso.")
        

    finally:
        conn.close()

if __name__ == "__main__":
    main()
