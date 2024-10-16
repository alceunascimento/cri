# CRI 3.0 : racionalização e automatização do registro de incorporação imobiliária

## Projeto
Registrar uma incorporação imobiliária com titulo em formato de leitura por máquina (XML).

## Objetivo

O objetivo do projeto é implementar uma solução mais eficiente para o processamento do registro de incorporações imobiliárias.
O procedimento atual é manual, demorado e sujeito à erros.
O padrão de ingresso dos dados da incorporação no serviço de registro de imóveis é feito de forma eletrônica, mas no formato PDF.
Isto dificulta o trabalho de extração dos dados do registrador.
Dentre os documentos necessários para o registro da incorporação, destaca-se os Quadros de Área da NBR 12721:2006.
Esta NBR regula a *Avaliação de custos unitários de construção para incorporação imobiliária e outras disposições para condomínios edilícios – Procedimento*.
O layout adotado pela ABNT para apresentação deste documentos tem foco na leitura humana e não por máquinas, o que cria mais um grau de dificuldade.

Uma forma que o serviço de registro de imóveis encontrou para processar os dados foi através de uma planilha de Excel (arquivo `.xlsx`).
Esta planilha é preenchida manualmente, agregando dados de diversas variáveis contidas nos documentos da incorporação.
Há pouco ganho de produtividade com isto, dado que o trabalho é todo manual e sujeito à erros.

A solução adotada foi instrumentalizar os documentos técnicos em um formato de leitura por máquinas.
Especificamente, adotou-se o formato de `.xml` para o título de ingresso no serviço de registro de imóveis.
Este formato já é usado pelo CRI para acesso de títulos e extratos produzidos por instituições financeiras.
O ONR já tem parâmetros de formatação para este tipo de arquivo.
Além disto, o `.xml` permite assinatura digital por certificado ICP-BRASIL e a integridade das assinaturas pode ser feita no Validador do ITI.


## Racionalização do procedimento

Outro ponto importante, foi a racionalização do procedimento.
A prática dos incorporadores e CRI se desenvolveu com excesso de burocracia, sem previsão na legislação e na norma técnica.
O memorial de incorporação, que é a biblioteca documental prevista na lei, passou a ser quase integralmente replicado em um novo documento, chamado "Memorial de Incorporação" que agrega dados contidos no alvará, no registro imobiliário e nos Quadros de Área NBR.
Além disto, os Quadros de Área da NBR eram incrementados com um "quadro resumo" que replicava informações de outros quadros e do alvará de construção.
Isto implica que os mesmos dados estavam distribuídos em diversas bases, o que forçada o CRI a ter que analisar discrepâncias entre as bases de dados.
Portanto, uma forma de racionalizar isto é deixar este legado e passar a adotar um formato em que não há duplicidade de informação, que é o formato previso na lei de incorporação imobiliária.
No caso, em relação aos documentos técnicos, a lei exige:

* Art. 32. O incorporador somente poderá alienar ou onerar as frações ideais de terrenos e acessões que corresponderão às futuras unidades autônomas após o registro, no registro de imóveis competente, do memorial de incorporação composto pelos seguintes documentos:
    - d) projeto de construção devidamente aprovado pelas autoridades competentes;
    - e) cálculo das áreas das edificações, discriminando, além da global, a das partes comuns, e indicando, para cada tipo de unidade a respectiva metragern de área construída;
    - g) memorial descritivo das especificações da obra projetada, segundo modêlo a que se refere o inciso IV, do art. 53, desta Lei;
    - h) avaliação do custo global da obra, atualizada à data do arquivamento, calculada de acôrdo com a norma do inciso III, do art. 53 com base nos custos unitários referidos no art. 54, discriminando-se, também, o custo de construção de cada unidade, devidamente autenticada pelo profissional responsável pela obra;
    - i) instrumento de divisão do terreno em frações ideais autônomas que contenham a sua discriminação e a descrição, a caracterização e a destinação das futuras unidades e partes comuns que a elas acederão; 
    - j) minuta de convenção de condomínio que disciplinará o uso das futuras unidades e partes comuns do conjunto imobiliário;
    - p) declaração, acompanhada de plantas elucidativas, sôbre o número de veículos que a garagem comporta e os locais destinados à guarda dos mesmos.  


A legislação é atendida desta forma:

### Quanto ao item d
Os projetos serão juntados normalmente, em formato PDF.

### Quanto ao item e
Estes dados estão no Quadro 02 do Quadro de Áreas da NBR

### Quanto ao item g
Estes dados estão nos Quadros 06, 07 e 08 do Quadro de Áreas da NBR.

### Quanto ao item h
Estes dados estão no Quadro 03 do Quadro de Áreas da NBR.

### Quanto ao item i
Estes dados estarão no `memorial descritivo` contendo a descrição de cada unidade autônoma.
Todos os dados para a confecçaõ do `memorial descritivo` estão na tabela `cri` do banco de dados.
O `memorial descritivo` será gerado pelo CRI, a partir dos dados do banco de dados.
A apresentação de um documento específico `memorial descritivo` iriá minar o esforço de racionalização.


### Quanto ao item j
Estes dados estarão no documento PDF "Convenção de Condomínio".
Não será incluída neste instrumento a repetição dos dados de alvará, memorial descritivo e quadro de áreas, como é feito via legado.

### Quanto ao item p
Estes dados estarão no `memorial descritivo`.


## Validação dos dados


### Memorial descritivo:

Formato atual:

APARTAMENTO 531: possuindo esta unidade as seguintes áreas construídas: área privativa de 24.280000 metros quadrados, área comum de 12.020098 metros quadrados, perfazendo a área construída de 37.378277 metros quadrados; cabendo-lhe, a fração ideal de solo e partes comuns de 0.00071126 e quota de terreno de 2.298195 metros quadrados. Possuindo, ainda, direito de uso das seguintes áreas descobertas: recreação comum descoberta de 1.078179 metros quadrados. Localização: localiza-se no 0º pavimento, sendo que para quem entra no apartamento pelo elevador, confronta pela frente com terreno do condomínio, pelo lado direito com apartamento 530, pelo lado esquerdo com apartamento 532 e pelo fundo com circulação comum.

Formato sugerido:

APARTAMENTO 531. Subcondomínio: [...]. Áreas construídas: privativa de 24.280000 m², comum de 12.020098 m², total de 37.378277 m². Fração ideal no solo e nas partes comuns: 0.00071126. Quota de terreno: 2.298195 metros quadrados. Localização:  [...]º pavimento, sendo que para quem entra na unidade autônoma, confronta pela frente com [...]], pelo lado direito com [...], pelo lado esquerdo com [...] e pelo fundo com [...].


Referencia: { “nome do quadro de áreas” ; “coluna no quadro de áreas” }
`unidade_especie` = vaga, loja, apartamento, etc.
`unidade_id` = é o número da unidade

Texto para validar:

{unidade_especie} {unidade_id}: possuindo esta unidade as seguintes áreas construídas: área privativa de {quadro resumo_04B; coluna A) metros quadrados, área comum de {quadro_areas_04B; coluna_E} metros quadrados, perfazendo a área construída de {quadro_areas_04B; coluna_F} metros quadrados; cabendo-lhe, a fração ideal de solo e partes comuns de {quadro_areas_04B; coluna_G} e quota de terreno de {quadro_areas_resumo; coluna_quota_de_terreno}  metros quadrados. Localização: localiza-se no {sem referencia no quadro; referencia no projeto}, sendo que para quem entra na unidade, confronta pela frente com {confrontacao_frente}, pelo lado direito com {confrontacao_direita}, pelo lado esquerdo com {confrontacao_esquerda} e pelo fundo {confrontacao_fundos}.



## Implementação 
A implementação se dará em duas etapas:

* 1ª (mínima): 
    - O incorporador produzirá um banco de dados em `SQLite` com:
        - todos os Quadro de Áreas da ABNT NBR;
        - os dados do alvará de construção;
        - os dados da matrícula do imóvel;
        - os dados para formação do indicador real de cada unidade autônoma da incorporação imobiliária;
    - O incorporador emitirá um `.xml` do banco de dados e assinará usando o assinador SERPRO para `.xml`;
    - O incorporadora fará o protocolo do `.xml` no CRI em conjunto com os demais documentos da incorporação que ainda são físicos;
    - O registrador executará um código de computador (`python`) que irá:
        - carregar o `.xml` e recriar um banco de dados `SQlite` (`.db`) (emitirá uma saída de log e verificação de erros em `.txt`);
        - obter os dados do alvará de construção direto na prefeitura (o alvará será salvo em formato `.json`);
        - analisar os dados e responder uma série de perguntar pré-definidas pelo registrador (saída em `.txt` e arquivo `.xlsx`);
        - criar uma planilha de Excel (`.xlsx`) contendo os Quadros de Área ABNT NBR, no formato tradicional;
        - criar uma arquivo em `.html` contendo o memorial descritivo de cada uma das unidades autônomas;
    - O registrador, após validar a incorporação, poderá utilizar o `.xml` para popular o livro do Indicador Real, atraves do seu ERP;

> Notas: as últimas duas saídas (.xlsx e .html) servem apenas para o registrador ter um formato capaz de emitir de certidões para leitura humana. O .html poderá ser convertido em PDF diretamente pelas ferramentas padrão do Windows, caso necessário.



* 2ª (ideal): 
    - O incorporador produzirá um banco de dados (SQLite) com todas as informações;
    - O incorporador emitirá e assinará um XML com os dados que o registrador precisa para registrar a incorporação (quadro de áreas NBR e memorial de incorporação);
    - O XML será protocolado no CRI em conjunto com os demais documentos da incorporação;
    - O XML será lido por um sistema que irá:
        - Emitir um relatório de análise de validação dos dados (integridade de quantitativos);
        - Emitir o Quadro de Áreas em formato PDF (caso seja necessário para expedição de certidões);
        - Emitir o Memorial de Incorporação em formato PDF (caso seja necessário para expedição de certidões);
    - Um script carregará os dados do XML no banco de dados do CRI;
    - O XML será arquivado como um título normal;

>[!NOTE]
> A mudança mais radical é que a geração do quadro de áreas e do memorial de incorporação num formato de leitura humana será feito pelo registrador e não entregue pelo incorporador. Se fossem protocolados os dois formatos (XML e PDF) não haveria ganho de eficiência, pois o CRI teria que conferir se os dois instrumentos são idênticos. Não se está deixando de apresentar o quadro de áreas e o memorial, mas sim apresentando num formato (layout) de leitura por máquinas. No longo prazo, a ABNT terá que desenvolver um schema de XML para este formato.


## Instruções

A planilha base de apoio à confecção dos quadro de áreas da NBR (`base_real.xlsx`) devem ser ajustados:

* Copiar e colar os dados em uma nova aba chamada `ajuste`;
* Excluir formatação;

>[!NOTE]
> A planilha vem com vínculos que quebram os dados com mais de 3 linhas. Verificar integridade !


## Script do Incorporador

Rodar o `0_source.py` no `pre_cri` que ele irá gerar as saídas.
A saída mais importante é o `titulo_cri.xml` que servirá de instrumento de acesso ao registro de imóveis.


## Script do Registrador

Rodar:
* o `0_carregar_xml_to_db.py` para gerar um `base_cri.db` na raiz e um `log_leitura_xml.txt`.
* o `/alvara/main.py` para obter o `{numero do alvara}.json` com o alvará de construção direto da prefeitura;
* o `1_validar_incorporacao.py` para ler o `base_cri.db` e fazer as verificações gerando um `validacao.txt`;
* o `2_gerar_memorial_incorporacao.py` para ler o `base_cri.db` e gerar o memorial de incorporação em fomato `.html`;
* o `3_criar_xlsx.py` para gerar os Quadros de Área NBR em formato `.xlsx` e o `3_ajustar_xlsx.py` para ajustes de formatação;


## Referências