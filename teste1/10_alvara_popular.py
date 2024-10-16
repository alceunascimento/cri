import json
import sqlite3

# Caminho para o arquivo JSON
json_file_path = './data/alvara.json'

# Carregar os dados do JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Criar uma conexão com o banco de dados SQLite
conn = sqlite3.connect('base_real.db')
c = conn.cursor()

# Inserir os dados do JSON na tabela `alvara`
c.execute('''
    INSERT INTO alvara (
        numero_documento,
        tipo_documento,
        finalidade,
        interessado,
        localizacao,
        inscricao_imobiliaria,
        indicacao_fiscal,
        autor_projeto_nome,
        autor_projeto_numero_art_rrt,
        responsavel_tecnico_nome,
        responsavel_tecnico_numero_art_rrt,
        construtora,
        limite_inicio_obra,
        limite_conclusao_obra,
        processo_emissao_alvara,
        data_expedicao_primeira_emissao,
        condicionantes_vistoria_conclusao_obras,
        observacoes_folha_alvara,
        indicacao_fiscal_lote,
        zoneamento,
        sistema_viario,
        quadricula,
        area_atingida,
        area_remanescente,
        area_total,
        area_original_lote,
        coeficiente_aproveitamento_aprovado,
        numero_cepacs,
        aca_area_construcao_adicional,
        qtde_pavimentos,
        qtde_elevadores,
        qtde_subsolos,
        extensao_muro_frontal,
        qtde_blocos,
        referencia_nivel_lote,
        qtde_vagas_estac_coberto,
        altura_total_edificacao,
        qtde_vagas_estac_descoberto,
        uso_subuso_edificacao,
        qtde_unidades,
        area_total_destinada_uso,
        estrutura_vedacao,
        areas_computaveis_total,
        areas_nao_computaveis_total,
        areas_recreacao_total,
        outras_areas_total_global,
        parametros_zoneamento_permeabilidade,
        parametros_zoneamento_taxa_ocupacao_lote,
        parametros_zoneamento_coeficiente_aprov,
        parametros_zoneamento_taxa_ocupacao_torre,
        parametros_zoneamento_densidade_lote
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    data.get("Número do Documento:"),
    data.get("Tipo do Documento:"),
    data.get("Finalidade:"),
    data.get("Interessado:"),
    data.get("Localização:"),
    data.get("Inscrição Imobiliária:"),
    data.get("Indicação Fiscal:"),
    data["Autor Projeto:"].get("Nome"),
    data["Autor Projeto:"].get("Número ART/RRT:"),
    data["Responsável Técnico:"].get("Nome"),
    data["Responsável Técnico:"].get("Número ART/RRT:"),
    data.get("Construtora:"),
    data.get("Limite Início Obra:"),
    data.get("Limite Conclusão Obra:"),
    data.get("Processo de Emissão do Alvará:"),
    data.get("Data Expedição da Primeira Emissão:"),
    data.get("Condicionantes para Vistoria de Conclusão de Obras:"),
    data.get("Observações Folha Alvará:"),
    data["DadosLote"].get("Indicação Fiscal"),
    data["DadosLote"].get("Zoneamento"),
    data["DadosLote"].get("Sistema Viário"),
    data["DadosLote"].get("Quadrícula"),
    data.get("Área Atingida:"),
    data.get("Área Remanescente:"),
    data.get("Área Total (m2):"),
    data.get("Área Original do Lote (m2):"),
    data.get("Coeficiente de Aproveitamento Aprovado:"),
    data.get("Número de CEPACs:"),
    data.get("ACA-Área de Construção Adicional (m2):"),
    data.get("Qtde de Pavimentos:"),
    data.get("Qtde de Elevadores:"),
    data.get("Qtde de Subsolos:"),
    data.get("Extenção do Muro Frontal:"),
    data.get("Qtde de Blocos:"),
    data.get("Referência de Nível do Lote-rn(m):"),
    data.get("Qtde Vagas Estac. Coberto:"),
    data.get("Altura total da Edificação(m):"),
    data.get("Qtde Vagas Estac. Descoberto:"),
    data["DadosEdificacao"].get("Uso/Subuso da Edificação"),
    data["DadosEdificacao"].get("Qtde Unidades"),
    data["DadosEdificacao"].get("Área Total Destinada ao Uso"),
    data["DadosEdificacao"].get("Estrutura / Vedação"),
    data["Áreas Computáveis (m2)"].get("Total:"),
    data["Áreas Não Computáveis (m2)"].get("Total:"),
    data["Áreas De Recreção (m2)"].get("Total:"),
    data["Outras Áreas (m2)"].get("Total Global:"),
    data["Parâmentros Do Zoneamento"].get("Permeabilidade do Lote (%):"),
    data["Parâmentros Do Zoneamento"].get("Taxa de Ocupação do Lote:"),
    data["Parâmentros Do Zoneamento"].get("Coeficiente de Aprov. Lote:"),
    data["Parâmentros Do Zoneamento"].get("Taxa de Ocupação da Torre:"),
    data["Parâmentros Do Zoneamento"].get("Densidade do Lote (Hab./Hect.):")
))

# Commitar as mudanças e fechar a conexão
conn.commit()
conn.close()