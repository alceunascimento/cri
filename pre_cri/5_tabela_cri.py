import pandas as pd
import sqlite3
import re

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')

# Ler a tabela 'quadro_resumo' do banco de dados
df = pd.read_sql_query("SELECT * FROM quadro_resumo", conn)

# Função para extrair a parte antes e depois da palavra "TIPO" da variável unidade_tipo
def extrair_especie_unidade(texto):
    match = re.search(r'^(.*?)\s+TIPO', texto)
    return match.group(1).strip() if match else None

def extrair_tipo_unidade(texto):
    match = re.search(r'TIPO\s+(.*)', texto)
    return match.group(1).strip() if match else None

def definir_especie_imovel_doi(especie):
    if especie == 'APARTAMENTO':
        return 'apto'
    elif especie == 'LOJA':
        return 'loja'
    else:
        return 'outros'

# Ler a aba 01 da planilha `base_real_confrontantes`
df_confrontantes = pd.read_excel('./pre_cri/base_real_confrontantes.xlsx', sheet_name='01')

# Criar o DataFrame para a tabela "cri"
df_cri = pd.DataFrame()
df_cri['unidade_numero'] = df['unidade_numero']
df_cri['bloco'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['especie_unidade'] = df['unidade_tipo'].apply(extrair_especie_unidade)
df_cri['tipo_unidade'] = df['unidade_tipo'].apply(extrair_tipo_unidade)
df_cri['pavimento'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['area_total_construida'] = df['area_alvara_total']
df_cri['area_total_descoberta'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['area_privativa'] = df['area_alvara_privativa']
df_cri['area_privativa_descoberta'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['area_vinculada_garagem'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['area_vinculada_outras'] = df['area_alvara_deposito_vinculado']
df_cri['area_comum'] = df['area_alvara_comum']
df_cri['area_comum_descoberta'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['vaga_vinculada_descoberta'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['fracao_ideal_solo_condominio'] = df['fracao_ideal_solo_condominio']
df_cri['quota_terreno_condominio'] = df['quota_terreno']
df_cri['fracao_ideal_unidade_subcondominio'] = df['fracao_ideal_solo_subcondominio']
df_cri['confrontacao_frente'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['confrontacao_direita'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['confrontacao_esquerda'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['confrontacao_fundos'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['tipo_garagem_vinculada'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)
df_cri['localizacao_garagem_vinculada'] = '0'  # Inicialmente preencher com 0 (ajustar conforme necessário)

# Adicionar as novas variáveis fixas
condominio_info = {
    'nome_condominio': "AYA CARLOS DE CARVALHO",
    'tipo_logradouro': "Alameda",
    'nome_logradouro': "Doutor Carlos de Carvalho",
    'numero_logradouro': 256,
    'bairro': "Centro",
    'municipio': "Curitiba",
    'cep': "80.410-170",
    'proprietario': "IPBL CARLOS DE CARVALHO INCORPORAÇÃO DE IMÓVEIS SPE LTDA.",
    'cnpj_cpf': "56.042.453/0001-35",
    'registro_anterior': "0.000 do 0 CRI",
    'lote': "lote M-01",
    'quadra': "não aplicável",
    'planta': "Planta Xavier de Miranda",
    'indicacao_fiscal': "032.000.050-0066",
}

for key, value in condominio_info.items():
    df_cri[key] = value

# Definir a variável 'especie_imovel_doi' com base na variável 'especie_unidade'
df_cri['especie_imovel_doi'] = df_cri['especie_unidade'].apply(definir_especie_imovel_doi)

# Incluir a variável "situacao_obra_doi" na última coluna e preencher com "em construção"
df_cri['situacao_obra_doi'] = 'em construção'

# Mapear as variáveis 'pavimento' e 'confrontacoes' da planilha de confrontantes
for index, row in df_cri.iterrows():
    unidade_numero = row['unidade_numero']
    confrontante_info = df_confrontantes[df_confrontantes['unidade_numero'] == unidade_numero]
    
    if not confrontante_info.empty:
        df_cri.at[index, 'pavimento'] = confrontante_info['pavimento'].values[0]
        df_cri.at[index, 'confrontacao_frente'] = confrontante_info['confrontacao_frente'].values[0]
        df_cri.at[index, 'confrontacao_direita'] = confrontante_info['confrontacao_direita'].values[0]
        df_cri.at[index, 'confrontacao_esquerda'] = confrontante_info['confrontacao_esquerda'].values[0]
        df_cri.at[index, 'confrontacao_fundos'] = confrontante_info['confrontacao_fundos'].values[0]

# Criar a tabela `cri` no banco de dados
df_cri.to_sql('cri', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `cri` criada e populada com sucesso.")