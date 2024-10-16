import sqlite3

# Criar uma conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')
c = conn.cursor()

# Criar a tabela `alvara` com as variáveis como chaves do JSON
c.execute('''
    CREATE TABLE IF NOT EXISTS alvara (
        numero_documento TEXT,
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
        area_atingida TEXT,
        area_remanescente TEXT,
        area_total TEXT,
        area_original_lote TEXT,
        coeficiente_aproveitamento_aprovado TEXT,
        numero_cepacs TEXT,
        aca_area_construcao_adicional TEXT,
        qtde_pavimentos TEXT,
        qtde_elevadores TEXT,
        qtde_subsolos TEXT,
        extensao_muro_frontal TEXT,
        qtde_blocos TEXT,
        referencia_nivel_lote TEXT,
        qtde_vagas_estac_coberto TEXT,
        altura_total_edificacao TEXT,
        qtde_vagas_estac_descoberto TEXT,
        uso_subuso_edificacao TEXT,
        qtde_unidades TEXT,
        area_total_destinada_uso TEXT,
        estrutura_vedacao TEXT,
        areas_computaveis_total TEXT,
        areas_nao_computaveis_total TEXT,
        areas_recreacao_total TEXT,
        outras_areas_total_global TEXT,
        parametros_zoneamento_permeabilidade TEXT,
        parametros_zoneamento_taxa_ocupacao_lote TEXT,
        parametros_zoneamento_coeficiente_aprov TEXT,
        parametros_zoneamento_taxa_ocupacao_torre TEXT,
        parametros_zoneamento_densidade_lote TEXT
    )
''')

# Commitar as mudanças e fechar a conexão
conn.commit()
conn.close()