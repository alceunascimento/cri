# CRI 3.0 : racionalização e automatização do registro de incorporação imobiliária

## Projeto
Registrar uma incorporação imobiliária com titulo em formato de leitura por máquina (`.xml`).

## Objetivo

O objetivo do projeto é implementar uma solução mais eficiente para o processamento do registro de incorporações imobiliárias.

## Cenário 

O procedimento atual é manual, demorado e sujeito à erros.
O padrão de ingresso dos dados da incorporação no serviço de registro de imóveis é feito de forma eletrônica, mas no formato `.pdf`.
O formato `.pdf` é um formato inadequado para o trãnsito de informações, pois apresenta os dados de forma desestruturada.
Este formato foi amplamente adotado como formato padrão de documentos, dada sua aparência similar à um documento físico, o que empresta uma certa "autoridade" ao formato.
Isto dificulta o trabalho de extração dos dados do registrador.

Fora isto, dentre os documentos necessários para o registro da incorporação, destaca-se os Quadros de Área da NBR 12721:2006.
Esta NBR regula a *Avaliação de custos unitários de construção para incorporação imobiliária e outras disposições para condomínios edilícios – Procedimento*.
O layout adotado pela ABNT para apresentação deste documentos tem foco na leitura humana e não por máquinas, o que cria mais um grau de dificuldade.
Ou seja, o documento apresentado ao registrados está com dados desestruturados e num formato de potencializa o problema da falta de estrutura do formato `.pdf`.

Uma forma que o serviço de registro de imóveis encontrou para processar os dados foi através da criação de uma planilha de Excel (arquivo `.xlsx`) a partir dos documentos apresentados.
Esta planilha é preenchida manualmente, agregando dados de diversas variáveis contidas nos documentos da incorporação.
Trata-se de um trabalho todo manual, demorado e sujeito à erros.

Além disto, é comum que ao registar a incorporação, os incorporadores:
* Adicionem tabelas não previstas na NBR 12721 para "facilitar" o trabalho do registrador, mas gerando duplicidade de dados;
* Apresentem um "memorial de incorporação", no formato PDF, repetindo todos os dados que já estão nos demais documentos;
* Incluam na convenção de condomínio todos os dados do "memorial de incorporação".

>[!NOTE]
> Destacou-se o "memorial de incorporação" dado que, pela lei, não existe um instrumento chamado "memorial de incorporação". O memorial de incorporação é toda a biblioteca documental apresentada ao registro. A presença deste instrumento nos procedimentos de incorporação imobiliári foi uma criação da prática.

Ao final, o registrador recebe uma multiplicidade de documentos redundantes, que demandam uma analise manual e demorada em busca de discrepâncias.


## Proposta 

Desta cenário, a solução adotada foi instrumentalizar os documentos técnicos em um formato que permita a leitura por máquinas.
Especificamente, adotou-se o formato de `.xml` para o título de ingresso no serviço de registro de imóveis.
Este formato já é usado pelo CRI para acesso de títulos e extratos produzidos por instituições financeiras.
O ONR já tem parâmetros de formatação para este tipo de arquivo.
Além disto, o `.xml` permite assinatura digital por certificado ICP-BRASIL e a integridade das assinaturas pode ser feita no Validador do ITI.


## Racionalização do procedimento

Outro ponto importante, foi a racionalização do procedimento.
A prática do procedimento se desenvolveu com excesso de burocracia, sem previsão na legislação e na norma técnica.
O memorial de incorporação, que é a biblioteca documental prevista na lei, passou a ser quase integralmente replicado pelo incorporador em um novo documento, chamado "Memorial de Incorporação" que agrega dados contidos no alvará, no registro imobiliário e nos Quadros de Área NBR.
Além disto, os Quadros de Área da NBR foram incrementados com um "quadro resumo" que replicava informações de outros quadros e do alvará de construção.
Isto implica que os mesmos dados estavam distribuídos em diversas bases, o que forçada o CRI a ter que analisar discrepâncias entre as bases de dados.
Portanto, uma forma de racionalizar isto é deixar este legado e passar a adotar um formato em que não há duplicidade de informação, que é o formato previso na lei de incorporação imobiliária.

### Documentos exigidos pela Lei 4.591/64

No caso, em relação aos documentos técnicos, a lei exige:

Art. 32. O incorporador somente poderá alienar ou onerar as frações ideais de terrenos e acessões que corresponderão às futuras unidades autônomas após o registro, no registro de imóveis competente, do memorial de incorporação composto pelos seguintes documentos:
- d) **projeto** de construção devidamente aprovado pelas autoridades competentes;
- e) cálculo das áreas das edificações, discriminando, além da global, a das partes comuns, e indicando, para cada tipo de unidade a respectiva metragern de área construída;
- g) memorial descritivo das especificações da obra projetada, segundo modêlo a que se refere o inciso IV, do art. 53, desta Lei;
- h) avaliação do ***custo global da obra**, atualizada à data do arquivamento, calculada de acôrdo com a norma do inciso III, do art. 53 com base nos custos unitários referidos no art. 54, discriminando-se, também, o custo de construção de cada unidade, devidamente autenticada pelo profissional responsável pela obra;
- i) instrumento de **divisão do terreno em frações ideais autônomas que contenham a sua discriminação e a descrição, a caracterização e a destinação** das futuras unidades e partes comuns que a elas acederão; 
- j) minuta de **convenção de condomínio** que disciplinará o uso das futuras unidades e partes comuns do conjunto imobiliário;
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

### Quanto ao item i : memorial descritivo
O objetivo é ter uma referencia para a descrição tabular das unidades autônomas e a fração ideal no solo e nas partes comuns que cada uma terá.
Regra geral, a descriçao tabular da unidade autônoma pode ser obtida do projeto (item d), contudo, o formato apresenta dificuldade ao CRI.
Em alguns casos, quando há subcondomínio, é necessário também a descrição das áreas comuns conforme a atribuição delas por subcondomínio.
Portanto, a norma exige que seja apresentado um documento que descreve as características que estão no projeto, portanto, um `memorial descritivo`.

Além disto, o instrumento é essencial para determinar a apropriação de fração ideal no solo e nas partes comuns de cada unidade autônoma.
Esta apropriação é de livre escolha do incorporador, pelo critério que ele escolher.
O fato de haver a apuração de uma fração ideal de solo nos Quadros de Área da NBR não implica que ela seja, obrigatóriamente, adotada.
Contudo, a maioria dos incorporadores adota esta fração ideal, evitando uma nova apuração.
Portanto, é necessário que a informação esteja contida neste instrumento.

Em resumo, o documento precisa ter:
* Discriminação: designação numérica ou alfabética da unidade autônoma;
* Descrição e Caracterização: as caracteríticas observáveis da unidade autônoma;
* Destinação: residencial ou não residencial;

>[!NOTE]
> Quando a lei indica `discriminação` e `destinção`: Pela legislação de referência: *Art. 1º As edificações ou conjuntos de edificações, de um ou mais pavimentos, construídos sob a forma de unidades isoladas entre si, ***destinadas a fins residenciais ou não-residenciais***, poderão ser alienados, no todo ou em parte, objetivamente considerados, e constituirá, cada unidade, propriedade autônoma sujeita às limitações desta Lei. § 1º Cada unidade será assinalada por ***designação especial, numérica ou alfabética, para efeitos de identificação e discriminação***.*

>[!NOTE]
> Quando a lei indica `Descrição e Caracterização` : dada a ausência de definição na legislação de referência, a prática adotou indicar as áreas construídas, a fração ideal no solo e nas partes comuns e a localização (por pavimento e por confrontantes). O conceito de "área construida" não está presente na legislação de referência, o ideal seria adotar o conceito da legislação urbanística, onde *"A área construída de uma edificação é toda área coberta, independentemente de sua destinação, com pé-direito acima de 1,80m, composta de áreas computáveis e não computáveis, incentivos e prêmios"* (CURITIBA. Decreto nº 2.397/23, art. 12.)


Estes dados estarão no `memorial descritivo` contendo a descrição de cada unidade autônoma.
Todos os dados para a confecçaõ do `memorial descritivo` estão na tabela `cri` do banco de dados.
O `memorial descritivo` será gerado pelo CRI, a partir dos dados do banco de dados.
A apresentação de um documento específico `memorial descritivo` iriá minar o esforço de racionalização.


### Quanto ao item j : convenção de condomínio
Estes dados estarão no documento PDF "Convenção de Condomínio".
Não será incluída neste instrumento a repetição dos dados de alvará, memorial descritivo e quadro de áreas, como é feito via legado.

### Quanto ao item p : capacidade da vaga de garagem
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
A implementação se dará por dois agentes:

### Pelo incorporador:
- O incorporador produzirá um banco de dados em `SQLite` com:
    - todos os Quadro de Áreas da ABNT NBR;
    - os dados do alvará de construção;
    - os dados da matrícula do imóvel;
    - os dados para formação do indicador real de cada unidade autônoma da incorporação imobiliária;
- O incorporador emitirá um `.xml` do banco de dados e assinará usando o assinador SERPRO para `.xml`;
- O incorporadora fará o protocolo do `.xml` no CRI em conjunto com os demais documentos da incorporação que ainda são físicos;


### Pelo registrador:

- O registrador executará um código de computador (`python`) que irá:
    - carregar o `.xml` e recriar um banco de dados `SQlite` (`.db`);
        - (emitirá uma saída de log e verificação de erros em `.txt`);
    - obter os dados do alvará de construção direto na prefeitura;
        - (o alvará será salvo em formato `.json`);
    - analisar os dados e responder uma série de perguntar pré-definidas pelo registrador 
        - (saída em `.txt` e arquivo `.xlsx`);
    - criar uma planilha de Excel (`.xlsx`) contendo os Quadros de Área ABNT NBR
        - (no formato tradicional);
    - criar uma arquivo em `.html` contendo o memorial descritivo de cada uma das unidades autônomas;
        - (adotará o formato ONR para "extrato de xml")
- O registrador, após validar a incorporação, poderá utilizar o `.xml` para popular o livro do Indicador Real, atraves do seu ERP;

> Notas: as últimas duas saídas (`.xlsx` e `.html`) servem apenas para o registrador ter um formato capaz de emitir de certidões para leitura humana. O .html poderá ser convertido em PDF diretamente pelas ferramentas padrão do Windows, caso necessário.

A mudança mais radical é que a geração do quadro de áreas e do memorial de incorporação num formato de leitura humana será feito pelo registrador e não entregue pelo incorporador. Se fossem protocolados os dois formatos (`.xml` e `.pdf`) não haveria ganho de eficiência, pois o CRI teria que conferir se os dois instrumentos são idênticos. Não se está deixando de apresentar o quadro de áreas e o memorial descritivo, mas sim apresentando num formato ("layout") de leitura por máquinas. No longo prazo, a ABNT terá que desenvolver um schema de `.xml` para este formato.


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