import sqlite3

# Conectando ao banco de dados existente ou criando se não existir
conn = sqlite3.connect('./pre_cri/base_real.db')
cursor = conn.cursor()

# Criando a tabela informacoes_preliminares se ela ainda não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS informacoes_preliminares (
        id INTEGER PRIMARY KEY,
        nome_incorporador TEXT,
        cnpj_incorporador TEXT,
        endereco_incorporador TEXT,
        nome_responsavel_tecnico TEXT,
        registro_crea TEXT,
        art TEXT,
        endereco_responsavel_tecnico TEXT,
        nome_edificio TEXT,
        local_construcao TEXT,
        cidade_uf TEXT,
        designacao_projeto_padrao TEXT,
        quantidade_unidades_autonomas INTEGER,
        padrao_acabamento TEXT,
        numero_pavimentos INTEGER,
        vagas_total INTEGER,
        vagas_unidade_autonoma INTEGER,
        vagas_acessorio_unidade_autonoma INTEGER,
        vagas_uso_comum INTEGER,
        area_lote REAL,
        data_aprovacao_projeto DATE,
        numero_alvara_projeto TEXT,
        data_local_assinaturas DATE,
        nota TEXT
    )
''')

# Inserindo os dados na tabela
cursor.execute('''
    INSERT INTO informacoes_preliminares (
        nome_incorporador, cnpj_incorporador, endereco_incorporador, nome_responsavel_tecnico, registro_crea, art, endereco_responsavel_tecnico, 
        nome_edificio, local_construcao, cidade_uf, designacao_projeto_padrao, quantidade_unidades_autonomas, padrao_acabamento, numero_pavimentos, 
        vagas_total, vagas_unidade_autonoma, vagas_acessorio_unidade_autonoma, vagas_uso_comum, area_lote, data_aprovacao_projeto, numero_alvara_projeto, 
        data_local_assinaturas, nota
    ) VALUES (
        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
    )
''', (
    'IPBL CARLOS DE CARVALHO INCORPORAÇÃO DE IMÓVEIS SPE LTDA', 
    '56.042.453/0001-35', 
    'Rua Kalil Elias Warde, 219, Campina do Siqueira, Curitiba, Paraná',
    'Ana Lucia Bajerski', 
    '24.075-D/PR', 
    '1720246147770', 
    'Rua Emiliano Perneta, 725, conj. 502, Centro, Curitiba, Paraná', 
    'AYA CARLOS DE CARVALHO', 
    'Alameda Doutor Carlos de Carvalho, 256; Rua Visconde de Nacar, 1035; Rua Cruz Machado, 555',
    'Curitiba, Paraná.',
    'R16N', 
    890, 
    'Normal', 
    33, 
    257, 
    208, 
    49, 
    0, 
    3231.16, 
    '2024-10-23', 
    405847, 
    '2024-10-23',
    'Cf. ABNT 12.721: 2006 Item 3.17 nota 2: "As eventuais diferenças entre as áreas reais calculadas nos quadros desta Norma com outras áreas constantes nos projetos, alvarás e/ou habite-se, devem-se aos diferentes critérios estabelecidos nas respectivas metodologias de cálculo.'
))

# Salvando (commit) as alterações e fechando a conexão
conn.commit()
conn.close()

print("Dados inseridos com sucesso na tabela informacoes_preliminares.")
