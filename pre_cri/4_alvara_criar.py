import sqlite3

# Criar uma conexão com o banco de dados SQLite
conn = sqlite3.connect('./pre_cri/base_real.db')
c = conn.cursor()

# Criar a tabela `alvara` com as variáveis como chaves do JSON
c.execute('''
    CREATE TABLE IF NOT EXISTS alvara (
        numero_documento INTEGER,
        tipo_documento TEXT,
        finalidade TEXT,
        interessado TEXT,
        localizacao TEXT,
        inscricao_imobiliaria TEXT,
        indicacao_fiscal TEXT,
        autor_projeto_nome TEXT,
        autor_projeto_numero_art_rrt TEXT,
        responsavel_tecnico_nome TEXT,
        responsavel_tecnico_numero_art_rrt TEXT,
        construtora TEXT,
        limite_inicio_obra TEXT,
        limite_conclusao_obra TEXT,
        processo_emissao_alvara TEXT,
        data_expedicao_primeira_emissao TEXT,
        condicionantes_vistoria_conclusao_obras TEXT,
        observacoes_folha_alvara TEXT,
        indicacao_fiscal_lote TEXT,
        zoneamento TEXT,
        sistema_viario TEXT,
        quadricula TEXT,
        area_atingida REAL,
        area_remanescente REAL,
        area_total REAL,
        area_original_lote REAL,
        coeficiente_aproveitamento_aprovado REAL,
        numero_cepacs INTEGER,
        aca_area_construcao_adicional REAL,
        qtde_pavimentos INTEGER,
        qtde_elevadores INTEGER,
        qtde_subsolos INTEGER,
        extensao_muro_frontal REAL,
        qtde_blocos INTEGER,
        referencia_nivel_lote REAL,
        qtde_vagas_estac_coberto INTEGER,
        altura_total_edificacao REAL,
        qtde_vagas_estac_descoberto INTEGER,
        uso_subuso_edificacao TEXT,
        qtde_unidades INTEGER,
        area_total_destinada_uso REAL,
        estrutura_vedacao TEXT,
        areas_computaveis_total REAL,
        areas_nao_computaveis_total REAL,
        areas_recreacao_total REAL,
        outras_areas_total_global REAL,
        parametros_zoneamento_permeabilidade REAL,
        parametros_zoneamento_taxa_ocupacao_lote REAL,
        parametros_zoneamento_coeficiente_aprov REAL,
        parametros_zoneamento_taxa_ocupacao_torre REAL,
        parametros_zoneamento_densidade_lote REAL
    )
''')

# Commitar as mudanças e fechar a conexão
conn.commit()
conn.close()