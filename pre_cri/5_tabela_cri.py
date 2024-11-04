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
df_confrontantes = pd.read_excel('./pre_cri/data/base_real_desagregada.xlsx', sheet_name='01')

# Ler a aba 01 da planilha `base_real_tipo_vaga`
df_tipo_vaga = pd.read_excel('./pre_cri/data/base_real_desagregada.xlsx', sheet_name='01')

# Criar o DataFrame para a tabela "cri"
df_cri = pd.DataFrame()
df_cri['subcondominio'] = df['subcondominio']
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
df_cri['area_comum_descoberta'] = df['area_comum_descoberta']
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
df_cri['tipo_vaga'] = '0' # Inicialmente preencher com 0 (ajustar na sequencia)

# Adicionar as novas variáveis fixas
condominio_info = {
    'nome_condominio': "AYA CARLOS DE CARVALHO",
    'tipo_logradouro': "Alameda",
    'nome_logradouro': "Doutor Carlos de Carvalho",
    'numero_logradouro': "256",
    'bairro': "Centro",
    'municipio': "Curitiba",
    'cep': "80.410-170",
    'proprietario': "IPBL CARLOS DE CARVALHO INCORPORAÇÃO DE IMÓVEIS SPE LTDA.",
    'cnpj_cpf': "56.042.453/0001-35",
    'matricula': "70.290 do 1º Serviço de Registro de Imóveis da Comarca de Curitiba, Paraná.",
    'registro_anterior': "R-7 da matrícula nº 1.877, datado de 09 de janeiro de 2012 e R-5 das matrículas nºs 33.097, 33.098, 33.099, 33.100, 33.101, 33.102, 33.103, 33.104, 33.105, 33.106, 33.107, 33.108 e 33.109, datados de 12 de dezembro de 2012, referidos nas matrículas nºs 57.256 e 64.954, todas do Registro geral do 1º Serviço de Registro de Imóveis da Comarca de Curitiba, Paraná.",
    'lote': "lote M-01",
    'quadra': "não aplicável",
    'planta': "Planta Xavier de Miranda",
    'indicacao_fiscal': "11.109.032"
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

# Mapear a variável 'tipo_vaga' da `df_tipo_vaga`
for index, row in df_cri.iterrows():
    unidade_numero = row['unidade_numero']
    tipo_vaga_info = df_tipo_vaga[df_tipo_vaga['unidade_numero'] == unidade_numero]
    
    if not tipo_vaga_info.empty:
        df_cri.at[index, 'tipo_vaga'] = tipo_vaga_info['tipo_vaga'].values[0]

# Adicionar os textos fornecidos à tabela 'cri'
partes_comuns_base = (
    "São partes comuns do edifício, insuscetíveis de divisão, alteração ou alienação, ligadas às respectivas unidades autônomas, as referidas no artigo 3º da Lei 4.591/64, e de modo especial:"
)

partes_comuns_geral = (
    "São partes comuns do condomínio geral: o solo no qual estarão localizadas as edificações descritas; as fundações, paredes laterais, paredes mestras, colunas de sustentação, lajes, vigas e telhados; os encanamentos de água, luz, força, esgoto, telefone e automação, bem como as suas respectivas instalações, até os pontos de intercessão com as ligações de propriedade dos condôminos; as calhas, os condutores de águas pluviais, dutos, receptáculos de lixo e suas respectivas instalações; os acessos, embarque e desembarque de passageiros e port cochere, calçadas, jardins e lixeiras; as contenções de cheias, caixas de gordura, gerador, medidores e transformadores todos localizados no subsolo 1; a circulação da galeria comercial no térreo; os barriletes e reservatórios; enfim, tudo o mais que pela própria natureza do serviço ou destinação seja coisa de uso comum a todos os condôminos."
)

partes_comuns_residencial = (
    "São partes comuns do subcondomínio residencial: halls dos elevadores e escadas do subsolo 3 ao subsolo 1; o bicicletário localizado no subsolo 1; os 9 (nove) elevadores respectivos poços, máquinas e acessórios, que dão acesso a torre residencial; as 02 (duas) escadas de emergência que dão acesso à torre residencial; o depósito do condomínio localizado no subsolo 3; o hall de entrada e circulações do térreo ao 33º pavimento; a rampa/eclusa serviço, eclusa/lockers, portaria com I.S., depósito encomendas, hall delivery localizados no térreo; as áreas de recreações cobertas e descobertas localizadas no 2º pavimento e 33º pavimento; o piso técnico e espaços técnicos localizados no térreo e mezanino; enfim, tudo o que mais for de uso comum aos apartamentos deste subcondomínio pela própria natureza do serviço ou destinação."
)

partes_comuns_estacionamento = (
    "São partes comuns do subcondomínio estacionamento: as rampas de acessos aos subsolos; as áreas de circulações de veículos localizados nos subsolos; o elevador, respectivos poços, máquinas e acessórios, que dá acesso do térreo ao subsolo 3; antecâmara e escada de emergência que dá acesso do térreo ao subsolo 3; enfim, tudo o que mais for de uso comum às vagas deste subcondomínio pela própria natureza do serviço ou destinação."
)

partes_comuns_residencial_estacionamento = (
    "São partes comuns dos subcondomínios estacionamento e residencial: copa funcionários, vestiários, administrativo, sala BMS e administrativo localizado no subsolo 1; enfim, tudo o que mais for de uso comum as vagas e apartamentos residenciais pela própria natureza do serviço ou destinação."
)

partes_comuns_galeria = (
    "Não existem partes comuns específicas do subcondomínio galeria."
)




# Adicionar as novas variáveis ao DataFrame
df_cri['partes_comuns_base'] = partes_comuns_base
df_cri['partes_comuns_geral'] = partes_comuns_geral
df_cri['partes_comuns_residencial'] = partes_comuns_residencial
df_cri['partes_comuns_residencial_estacionamento'] = partes_comuns_residencial_estacionamento
df_cri['partes_comuns_estacionamento'] = partes_comuns_estacionamento
df_cri['partes_comuns_galeria'] = partes_comuns_galeria



incorporador = (
    "IPBL CARLOS DE CARVALHO INCORPORAÇÃO DE IMÓVEIS SPE LTDA, pessoa jurídica de direito privado, inscrita no CNPJ sob nº 56.042.453/0001-35, com sede na Rua Kalil Elias Warde nº 219, Bairro Campina do Siqueira, em Curitiba, Estado do Paraná"
)

responsavel_tecnico_construcao = (
    "Willian Matheus Bernsdorf, Engenheiro Civil CREA 139.621-D/PR"
)

responsavel_tecnico_nbr = (
    "Luiz Augusto Brenner Rose, Engenheiro Civil CREA 21.070-D/PR"
)

matricula = (
    "Matrícula nº 70.290 do Registro Geral de Imóveis do 1º Serviço de Registro de Imóveis da Comarca de Curitiba, Paraná."
)

edificio = (
    "O incorporador, sobre o imóvel já descrito, construirá por sua conta e risco, por preço determinável, na forma do Artigo 43, da Lei 4.591, de 16 de dezembro de 1.964, um empreendimento denominado “AYA CARLOS DE CARVALHO”, subdividido em 03 (três) subcondomínios distintos: (i) Subcondomínio Estacionamento, composto por 208 (duzentos e oito) vagas de garagem autônomas, com capacidade para estacionar 257 veículos, o qual localizar-se-á desde o subsolo 3 até o subsolo 1, com acesso de entrada de veículos pela Alameda Doutor Carlos de Carvalho e saída de veículos pela Rua Cruz Machado. O acesso de pedestres será feito pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial; (ii) Subcondomínio Galeria, composto por 08 (oito) unidades de Comércios e Serviços Vicinais designados como LOJAS, todas com destinação comercial, o qual localizar-se-á no térreo e mezanino, com acesso de pedestres pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial; (iii) Subcondomínio Residencial, composto por 574 (quinhentos e setenta e quatro) kitinetes e 308 (trezentos e oito) apartamentos, totalizando 882 (oitocentos e oitenta e dois) unidades residenciais, com destinação de habitação coletiva, o qual localizar-se-á desde o 3º pavimento até o 32º pavimento, com acesso de pedestres pelas Rua Cruz Machado, Rua Visconde de Nacar e Alameda Doutor Carlos de Carvalho, através da circulação da galeria comercial. O edifício será localizado na Alameda Doutor Carlos de Carvalho, 256, com a Rua Visconde de Nacar, 1035 e Rua Cruz Machado, 555, será construído em alvenaria e estrutura em concreto armado, com área total construída de 54.781,50m², conforme projeto aprovado pelo Alvará de Construção nº 405847, datado de 23/10/2024, e terá 38 (trinta e oito) pisos: subsolo 3, subsolo 2, subsolo 1, térreo, mezanino, 2º pavimento, pavimentos Tipo B1 (3º pavimento), pavimentos Tipo B2 (4° e 5° pavimento), Tipo A1 (6° pavimento), pavimentos Tipo A2 (7° e 8° pavimento), pavimentos Tipo A3 (9° pavimento), pavimentos Tipo A4 (10° pavimento), pavimentos Tipo A5 (11° pavimento), pavimentos Tipo A6 (12° e 14° pavimento), pavimentos Tipo A7 (13° pavimento), pavimentos Tipo B3 (15° pavimento), pavimentos Tipo B4 (16° pavimento), pavimentos Tipo A8 (17° pavimento.), pavimentos Tipo C1 (18° pavimento), pavimentos Tipo C2 (19° e 20° pavimento), pavimentos Tipo C3 (21° pavimento), pavimentos Tipo C4 (22° ao 24° pavimento), pavimentos Tipo C5 (25° pavimento), pavimentos Tipo D1 (26° ao 28° pavimento), pavimentos Tipo D2 (29° pavimento), pavimentos Tipo D3 (30° pavimento), pavimentos Tipo D4 (31° e 32° pavimento), piso técnico e 33º pavimento. Os pisos do edifício estarão assim distribuídos: 01º piso ou subsolo 3: Hall elevadores e escadas, hall elevador, antecâmara, 10 (dez) elevadores, 03 (três) escadas de emergência, depósito coletivo sob rampa, 09 (nove) depósitos vinculados às vagas sob nº 176/177, 178/179, 182/183, 184/185, 215/216, 217, 218, 219, 220/221, rampa sobe para subsolo 2, estacionamento com 95 (noventa e cinco) vagas de automóveis sob nº 163 ao 257, sendo 49 (quarenta e nove) vagas simples autônomas e 23 (vinte e três) vagas duplas autônomas; 02º piso ou subsolo 2: Hall elevadores e escadas, hall elevador, antecâmara, 10 (dez) elevadores, 03 (três) escadas de emergência, 09 (nove) depósitos vinculados às vagas sob nº 82/81, 84/83, 88/87, 90/89, 120/121, 122, 123, 124, 125/126, rampa desce para subsolo 3, rampa sobe para subsolo 1, estacionamento com 95 (noventa e cinco) vagas de automóveis sob nº 68 ao 162, sendo 49 (quarenta e nove) vagas simples autônomas e 23 (vinte e três) vagas duplas autônomas; 03º piso ou subsolo 1: Hall elevadores e escadas, hall elevador, antecâmara, 10 (dez) elevadores, 03 (três) escadas de emergência, copa funcionários, vestiário fem., vestiário masc., vestiário acessível, sala BMS, administrativo, bicicletário, espaços técnicos para cisternas, contenção de cheias, caixa de gordura, gerador, medidores e transformadores, depósito vinculado à vaga sob nº 67, rampa desce para subsolo 2, rampa de entrada do térreo, rampa de saída para o térreo, estacionamento com 67 (sessenta e sete) vagas de automóveis sob nº 1 ao 67, sendo 61 (sessenta e uma) vagas simples autônomas e 03 (três) vagas duplas autônomas; 04º piso ou térreo: 04 (quatro) acessos de pedestres comercial/residencial, sendo um pela Rua Cruz Machado, 02 (dois) pela Rua Visconde de Nacar e um pela Alameda Doutor Carlos de Carvalho; acesso embarque e desembarque de passageiros e port cochére comercial/residencial, saída de veículos estacionamento (rampa que sobe do subsolo 1) pela Rua Cruz Machado; acesso de veículos estacionamento (rampa que desce para subsolo 1) pela Alameda Doutor Carlos de Carvalho; rampas e escadas de acessos de pedestres, plataforma PNE, calçadas, jardins, lixeiras, rampa/eclusa serviço, eclusa/lockers, portaria com I.S., depósito encomendas, hall delivery, hall residencial, 10 (dez) elevadores, 03 (três) escadas de emergência, antecâmara, área técnica, galeria comercial e 08 (oito) lojas sob nº 01, 02, 03, 04, 05, 06, 07 e 08; 05º piso ou mezanino: 10 (dez) elevadores (sem parada), 02 (duas) escadas de emergência (sem acesso), 03 (três) espaços técnicos e mezaninos das lojas nº 01, 02, 07 e 08; 06º piso ou 2º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, 02 (dois) I.Ss, DML, 02 (dois) halls, jogos adulto, coworking, 02 (dois) I.S.s A., gourmet 1, gourmet 2, lavanderia, sala de reunião, copa festas, salão de festas com 02 (dois) I.S.s A., churrasqueira 1, churrasqueira 2 e 02 (dois) terraços/recreações descobertos; 07º piso ou 3º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 38 (trinta e oito) kitinetes sob nº 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337 e 338; 08º piso ou 4º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 38 (trinta e oito) kitinetes sob nº 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437 e 438; 09º piso ou 5º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 38 (trinta e oito) kitinetes sob nº 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537 e 538; 10º piso ou 6º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 601, 602, 603, 604, 605, 606, 607, 608, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 631, 632, 633, 634, 635, 636, 637 e 638 e 04 (quatro) apartamentos sob nº 609, 611, 628 e 630; 11º piso ou 7º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 701, 702, 703, 704, 705, 706, 707, 708, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 731, 732, 733, 734, 735, 736, 737 e 738 e 04 (quatro) apartamentos sob nº 709, 711, 728 e 730; 12º piso ou 8º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 801, 802, 803, 804, 805, 806, 807, 808, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 831, 832, 833, 834, 835, 836, 837 e 838 e 04 (quatro) apartamentos sob nº 809, 811, 828 e 830; 13º piso ou 09º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 901, 902, 903, 904, 905, 906, 907, 908, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 931, 932, 933, 934, 935, 936, 937 e 938 e 04 (quatro) apartamentos sob nº 909, 911, 928 e 930; 14º piso ou 10º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1031, 1032, 1033, 1034, 1035, 1036, 1037 e 1038 e 04 (quatro) apartamentos sob nº 1009, 1011, 1028 e 1030; 15º piso ou 11º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1123, 1124, 1125, 1126, 1127, 1131, 1132, 1133, 1134, 1135, 1136, 1137 e 1138 e 04 (quatro) apartamentos sob nº 1109, 1111, 1128 e 1130; 16º piso ou 12º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 1231, 1232, 1233, 1234, 1235, 1236, 1237 e 1238 e 04 (quatro) apartamentos sob nº 1209, 1211, 1228 e 1230; 17º piso ou 13º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes  sob nº 1301, 1302, 1303, 1304, 1305, 1306, 1307, 1308, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1331, 1332, 1333, 1334, 1335, 1336, 1337 e 1338 e 04 (quatro) apartamentos sob nº 1309, 1311, 1328 e 1330; 18º piso ou 14º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 1401, 1402, 1403, 1404, 1405, 1406, 1407, 1408, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1422, 1423, 1424, 1425, 1426, 1427, 1431, 1432, 1433, 1434, 1435, 1436, 1437 e 1438 e 04 (quatro) apartamentos sob nº 1409, 1411, 1428 e 1430; 19º piso ou 15º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 38 (trinta e oito) kitinetes sob nº 1501, 1502, 1503, 1504, 1505, 1506, 1507, 1508, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527, 1528, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1536, 1537 e 1538; 20º piso ou 16º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 38 (trinta e oito) kitinetes sob nº 1601, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630, 1631, 1632, 1633, 1634, 1635, 1636, 1637 e 1638; 21º piso ou 17º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 32 (trinta e duas) kitinetes sob nº 1701, 1702, 1703, 1704, 1705, 1706, 1707, 1708, 1712, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1731, 1732, 1733, 1734, 1735, 1736, 1737 e 1738 e 04 (quatro) apartamentos sob nº 1709, 1711, 1728 e 1730; 22º piso ou 18º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 1807, 1808, 1812, 1813, 1826, 1827, 1831 e 1832 e 16 (dezesseis) apartamentos sob nº 1801, 1803, 1806, 1809, 1811, 1814, 1816, 1819, 1820, 1822, 1825, 1828, 1830, 1833, 1835 e 1838; 23º piso ou 19º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 1907, 1908, 1912, 1913, 1926, 1927, 1931 e 1932 e 16 (dezesseis) apartamentos sob nº 1901, 1903, 1906, 1909, 1911, 1914, 1916, 1919, 1920, 1922, 1925, 1928, 1930, 1933, 1935 e 1938; 24º piso ou 20º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2007, 2008, 2012, 2013, 2026, 2027, 2031 e 2032 e 16 (dezesseis) apartamentos sob nº 2001, 2003, 2006, 2009, 2011, 2014, 2016, 2019, 2020, 2022, 2025, 2028, 2030, 2033, 2035 e 2038; 25º piso ou 21º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2107, 2108, 2112, 2113, 2126, 2127, 2131 e 2132 e 16 (dezesseis) apartamentos sob nº 2101, 2103, 2106, 2109, 2111, 2114, 2116, 2119, 2120, 2122, 2125, 2128, 2130, 2133, 2135 e 2138; 26º piso ou 22º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2207, 2208, 2212, 2213, 2226, 2227, 2231 e 2232 e 16 (dezesseis) apartamentos sob nº 2201, 2203, 2206, 2209, 2211, 2214, 2216, 2219, 2220, 2222, 2225, 2228, 2230, 2233, 2235 e 2238; 27º piso ou 23º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2307, 2308, 2312, 2313, 2326, 2327, 2331 e 2332 e 16 (dezesseis) apartamentos sob nº 2301, 2303, 2306, 2309, 2311, 2314, 2316, 2319, 2320, 2322, 2325, 2328, 2330, 2333, 2335 e 2338; 28º piso ou 24º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2407, 2408, 2412, 2413, 2426, 2427, 2431 e 2432 e 16 (dezesseis) sob nº 2401, 2403, 2406, 2409, 2411, 2414, 2416, 2419, 2420, 2422, 2425, 2428, 2430, 2433, 2435 e 2438; 29º piso ou 25º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações, 08 (oito) kitinetes sob nº 2507, 2508, 2512, 2513, 2526, 2527, 2531 e 2532 e 16 (dezesseis) sob nº 2501, 2503, 2506, 2509, 2511, 2514, 2516, 2519, 2520, 2522, 2525, 2528, 2530, 2533, 2535 e 2538; 30º piso 26º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 2601, 2603, 2606, 2607, 2609, 2611, 2613, 2614, 2616, 2619, 2620, 2622, 2625, 2626, 2628, 2630, 2632, 2633, 2635 e 2638; 31º piso ou 27º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 2701, 2703, 2706, 2707, 2709, 2711, 2713, 2714, 2716, 2719, 2720, 2722, 2725, 2726, 2728, 2730, 2732, 2733, 2735 e 2738; 32º piso ou 28º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 2801, 2803, 2806, 2807, 2809, 2811, 2813, 2814, 2816, 2819, 2820, 2822, 2825, 2826, 2828, 2830, 2832, 2833, 2835 e 2838; 33º piso ou 29º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 2901, 2903, 2906, 2907, 2909, 2911, 2913, 2914, 2916, 2919, 2920, 2922, 2925, 2926, 2928, 2930, 2932, 2933, 2935 e 2938; 34º piso ou 30º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 3001, 3003, 3006, 3007, 3009, 3011, 3013, 3014, 3016, 3019, 3020, 3022, 3025, 3026, 3028, 3030, 3032, 3033, 3035 e 3038; 35º piso ou 31º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 3101, 3103, 3106, 3107, 3109, 3111, 3113, 3114, 3116, 3119, 3120, 3122, 3125, 3126, 3128, 3130, 3132, 3133, 3135 e 3138; 36º piso ou 32º pavimento: 09 (nove) elevadores, 02 (duas) escadas de emergência, hall/circulações e 20 (vinte) apartamentos sob nº 3201, 3203, 3206, 3207, 3209, 3211, 3213, 3214, 3216, 3219, 3220, 3222, 3225, 3226, 3228, 3230, 3232, 3233, 3235 e 3238; 37º piso ou piso técnico:09 (nove) elevadores (sem parada), 02 (duas) escadas de emergência e área técnica; 38º piso ou 33º pavimento: 09 (nove) elevadores, hall elevador, 02 (duas) escadas de emergência, escada serviço cobertura, hall, wellnes, sauna, piscina coberta, academia e recreação/área descoberta de lazer. Na parte superior do edifício situam-se, ainda, o barrilete 1, barrilete 2, casa de máquinas dos elevadores e caixa de água com 02 (dois) reservatórios."
)

acesso_edificio = (
    "O acesso de pedestres será feito por entrada em comum através da circulação da galeria comercial para os Subcondomínio Galeria, Subcondomínio Estacionamento e Subcondomínio Residencial, com quatro entradas, sendo uma pela Alameda Doutor Carlos de Carvalho, duas pela Rua Visconde de Nacar e uma pela Rua Cruz Machado. O acesso de veículos para o Subcondomínio Estacionamento será feito por entrada para os subsolos pela Alameda Dr. Carlos de Carvalho e saída pela Rua Cruz Machado. Também haverá um acesso de veículos para embarque e desembarque, com uma entrada e uma saída pela Rua Cruz Machado."
)


# Adicionar as novas variáveis ao DataFrame
df_cri['incorporador'] = incorporador
df_cri['responsavel_tecnico_construcao'] = responsavel_tecnico_construcao
df_cri['responsavel_tecnico_nbr'] = responsavel_tecnico_nbr
df_cri['matricula'] = matricula
df_cri['edificio'] = edificio
df_cri['acesso_edificio'] = acesso_edificio


# Verificar e remover linhas completamente vazias
df_cri.dropna(how='all', inplace=True)


# Criar a tabela `cri` no banco de dados
df_cri.to_sql('cri', conn, if_exists='replace', index=False)

# Fechar conexão
conn.close()

print("Tabela `cri` criada e populada com sucesso.")
