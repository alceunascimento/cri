import json
import re
import sys

def ajustar_formatos_numericos(dados):
    # Função recursiva para percorrer e ajustar os valores no JSON
    if isinstance(dados, dict):
        return {chave: ajustar_formatos_numericos(valor) for chave, valor in dados.items()}
    elif isinstance(dados, list):
        return [ajustar_formatos_numericos(item) for item in dados]
    elif isinstance(dados, str):
        # Verifica se o valor está no formato numérico esperado e converte para "0000.00"
        if re.match(r'^\d{1,3}(\.\d{3})*,\d{2}$', dados):
            return dados.replace('.', '').replace(',', '.')
        elif re.match(r'^\d{1,3},\d{2}$', dados):
            return dados.replace(',', '.')
    return dados

# Verificar se o nome do arquivo foi passado como argumento
if len(sys.argv) != 2:
    print("Uso: python ajustar_numeros_json.py arquivo.json")
    sys.exit(1)

# Obter o nome do arquivo a partir dos argumentos
arquivo_nome = sys.argv[1]

# Carregar o JSON do arquivo fornecido
with open(arquivo_nome, 'r', encoding='utf-8') as arquivo:
    dados_json = json.load(arquivo)

# Ajustar os formatos numéricos
dados_ajustados = ajustar_formatos_numericos(dados_json)

# Salvar o JSON ajustado em um novo arquivo
arquivo_ajustado_nome = arquivo_nome.replace('.json', '_ajustado.json')
with open(arquivo_ajustado_nome, 'w', encoding='utf-8') as arquivo_ajustado:
    json.dump(dados_ajustados, arquivo_ajustado, indent=4, ensure_ascii=False)