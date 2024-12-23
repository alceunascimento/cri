# CRI 3.0 : racionalização e automatização do registro de incorporação imobiliária

## Projeto
Registrar uma incorporação imobiliária com titulo em formato de leitura por máquina (`.xml`).

## Objetivo

O objetivo do projeto é implementar uma solução mais eficiente para o processamento do registro de incorporações imobiliárias.

## Cenário 

O procedimento atual é manual, demorado e sujeito à erros.
O padrão de ingresso dos dados da incorporação no serviço de registro de imóveis pode ser feito de forma eletrônica, mas no formato `.pdf`.
O formato `.pdf` é um formato inadequado para o trãnsito de informações, pois apresenta os dados de forma desestruturada.
Este formato foi amplamente adotado como formato padrão de documentos, dada sua aparência similar à um documento físico, o que empresta uma certa "autoridade" ao formato.
Isto dificulta o trabalho de extração dos dados do registrador.

Fora isto, dentre os documentos necessários para o registro da incorporação, destaca-se os Quadros de Área da NBR 12721:2006.
Esta NBR regula a *Avaliação de custos unitários de construção para incorporação imobiliária e outras disposições para condomínios edilícios – Procedimento*.
O layout adotado pela ABNT para apresentação deste documentos tem foco na leitura humana e não por máquinas, o que cria mais um grau de dificuldade.
Ou seja, o documento apresentado aos registradores está com dados desestruturados e num formato de potencializa o problema da falta de estrutura do formato `.pdf`.

Uma forma que alguns serviços de registro de imóveis encontraram para processar os dados foi através da criação de uma planilha de Excel (arquivo `.xlsx`) a partir dos documentos apresentados.
Esta planilha é preenchida manualmente, agregando dados de diversas variáveis contidas nos documentos da incorporação.
Trata-se de um trabalho todo manual, demorado e sujeito à erros.

Além disto, é comum que ao registar a incorporação, os incorporadores:
* Adicionem tabelas não previstas na NBR 12721 para "facilitar" o trabalho do registrador, mas gerando duplicidade de dados;
* Apresentem um "memorial de incorporação", no formato PDF, repetindo todos os dados que já estão nos demais documentos;
* Incluam na convenção de condomínio todos os dados do "memorial de incorporação".

>[!NOTE]
> Destacou-se a expressão "memorial de incorporação" dado que, pela lei, não existe um instrumento chamado "memorial de incorporação". O memorial de incorporação é toda a biblioteca documental apresentada ao registro. A presença deste instrumento nos procedimentos de incorporação imobiliária foi uma criação da prática.

Ao final, o registrador recebe uma multiplicidade de documentos redundantes, que demandam uma analise manual e demorada em busca de discrepâncias.


## Proposta 

Deste cenário, a solução adotada foi instrumentalizar os documentos técnicos em um formato que permita a leitura por máquinas.
Especificamente, adotou-se o formato de `.xml` para o título de ingresso no serviço de registro de imóveis.
Este formato já é usado pelo CRI para acesso de títulos e extratos produzidos por instituições financeiras.
O ONR já tem parâmetros de formatação para este tipo de arquivo.
Além disto, o `.xml` permite assinatura digital por certificado ICP-BRASIL e a integridade das assinaturas pode ser feita no Validador do ITI.


## Racionalização do procedimento

Outro ponto importante, foi a racionalização do procedimento.
A prática do procedimento se desenvolveu com excesso de burocracia, sem previsão na legislação e na norma técnica.
O memorial de incorporação, que é a biblioteca documental prevista na lei, passou a ser quase integralmente replicado pelo incorporador em um novo documento, chamado "Memorial de Incorporação" que agrega dados contidos no alvará, no registro imobiliário e nos Quadros de Área NBR.
Além disto, os Quadros de Área da NBR foram incrementados com um "quadro resumo" que replicava informações de outros quadros e do alvará de construção.
Isto implica que os mesmos dados estão distribuídos em diversas bases, o que forçada o CRI a ter que analisar discrepâncias entre as bases de dados.
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

### Quanto ao item i : "memorial de incorporação" (ou "memorial descritivo")
O objetivo é ter uma referência para a descrição tabular das unidades autônomas e a fração ideal no solo e nas partes comuns que cada uma terá.
Regra geral, a descriçao tabular da unidade autônoma pode ser obtida do projeto (item d), contudo, o formato apresenta dificuldade ao CRI.
Em alguns casos, quando há subcondomínio, é necessário também a descrição das áreas comuns conforme a atribuição delas por subcondomínio.
Portanto, a norma exige que seja apresentado um documento que descreve as características que estão no projeto, portanto, um `memorial descritivo`, ainda que seja, comumente, chamado de "memorial de incorporação"

Em resumo, o documento precisa ter:
* Discriminação: designação numérica ou alfabética da unidade autônoma;
* Descrição e Caracterização: as caracteríticas observáveis da unidade autônoma;
* Destinação: residencial ou não residencial;


Estes dados estarão no `memorial descritivo` contendo a descrição de cada unidade autônoma.
Todos os dados para a confecção do `memorial descritivo` estão na tabela `cri` do banco de dados.
O `memorial descritivo` será gerado pelo CRI, a partir dos dados do banco de dados.
A apresentação de um documento específico `memorial descritivo` iriá minar o esforço de racionalização.


### Quanto ao item j : (minuta) da convenção do futuro condomínio
Estes dados estarão no documento PDF "Minuta da Convenção de Condomínio".
Não será incluída neste instrumento a repetição dos dados de alvará, memorial descritivo e quadro de áreas, como é feito via legado.


### Quanto ao item p : capacidade da vaga de garagem
Estes dados estarão no `memorial descritivo`.




## Implementação 
A implementação se dará por dois agentes:

### Pelo incorporador:
- O incorporador produzirá um banco de dados em `SQLite` com:
    - todos os Quadro de Áreas da ABNT NBR;
    - os dados do alvará de construção;
    - os dados para formação do indicador real de cada unidade autônoma da incorporação imobiliária;
- O incorporador emitirá um `.xml` do banco de dados e assinará usando o assinador SERPRO para `.xml`;
- O incorporadora fará o protocolo do `.xml` no CRI em conjunto com os demais documentos da incorporação que ainda são físicos;

>[!NOTE]
> A especificação das variáveis necessárias para a formação da tabela que contém os dados do indicador real veio do registrador.

### Pelo registrador:

- O registrador executará um código de computador (`python`) embarcado em um juptyer notebook (`.ipynb`) numa máquina virtual (Google Colaboratory) que irá:
    - carregar o `.xml` e recriar um banco de dados `SQlite` (`.db`);
        - (emitirá uma saída de log e verificação de erros em `.txt`);
    - analisar os dados e responder uma série de perguntar pré-definidas pelo registrador, como uma pré-qualificação registal; 
        - (saída em `.txt` e arquivo `.xlsx`);
    - criar uma planilha de Excel (`.xlsx`) de apoio para qualificação;
        - (no formato tradicional Excel);
    - criar diversos arquivos em `.html` contendo os Quadros de Área ABNT NBR;
        - (o formato HTML pode ser convertido para PDF para emissão de futuras certidões)
    - criar um arquivo em `.md` que é convertido em `.docx` contendo memorial descritivo de cada uma das unidades autônomas;
        - (a formatação da saída em `.docx` é de livre escolha do registrador, com base nos parametros de estilo do arquivo `reference.docx`)
        - o documento facilita o ato de registro da incorporação, bem como a abertura das matrículas e indicador real das unidades autônomas.

- O registrador utilizará os arquivos acima para auxiliar na validação da incorporação.
- O registrador utilizará o `.xml` para popular o livro do Indicador Real, atravé de uma rotina de processamento do seu ERP próprio.

>[!NOTE]
> A opção de usar o Google Colaboratory foi para simplificar o procedimento. Permite a execução em qualquer máquina e evita a necessidade de preparação e instalação de componentes em cada máquina. Basta o registrador carregar no GoogleDrive o `.xml` e o jupyter notebook `.ipynb` em uma pasta `Colab_cri` e será produzida a saída em aprox. 2 minutos. O tempo de execução do script é bem menor, mas há uma espera de 60 segundos após a reconstituição do banco de dados para evitar erros de leitura.

>[!IMPORTANT]
> **A mudança mais radical é que a geração do quadro de áreas e do memorial de incorporação num formato de leitura humana será feito pelo registrador e não entregue pelo incorporador. Se fossem protocolados os dois formatos (`.xml` e `.pdf`) não haveria ganho de eficiência, pois o CRI teria que conferir se os dois instrumentos são idênticos. Não se está deixando de apresentar o quadro de áreas e o memorial descritivo em sua forma completa e exigida pela norma técnica, mas sim apresentando num formato ("layout") de leitura por máquinas. No longo prazo, a ABNT poderá que desenvolver um schema de `.xml` para este formato**.

>[!NOTE]
> A prerrogativa legal da ABNT sobre a produção dos documentos técnicos (art. 53, Lei 4591/64) é limitada à critérios de apuração e modelos, a estética dos quadros é apenas um elemento facilitador presente como anexo na NBR.

>[!IMPORTANT]
> **A apresentação dos documentos em `.xml` não significa que os documentos são "extratos" como adotado em alguns instrumentos já utilizados pelo ONR. Neste caso, o `.xml` contém a integridade dos dados, não há qualquer supressão de dados. A mudança é apenas no padrão tecnlógico de transmissão dos dados. Deixa de utilizar um formato em que os dados não são estruturados (`.pdf`) para um formato que os dados são semi-estruturados (`.xml`). É uma mudança estética e funcional que, inclusive, premite reconstituir a estética padrão dos `.pdf` em uma fase de pós-processamento. Além disto, não há qualquer vedação legal à confecção de instrumentos em formato `.xml` ou qualquer norma que afaste a validade legal de instrumentos confecionados neste formato.**


## Procedimento do Registrador

Rodar:
* Ter uma conta no Google;
* Criar uma pasta `Colab_cri` na raiz do GoogleDrive;
* Salvar na pasta `Colab_cri`:
    - `colab_cri.ipynb`
    - `.xml`
    - `reference.docx`
    - uma pasta `output`
* Abrir o `colab_cri.ipynb` com a opção "Google Colaboratory"
![imagem1](./images/image1.png)

* Executar primeiro os itens "Instaçaões base" e "Monta o GoogleDrive para uso":
    - Este primeiro passo é necessário para instalar e carregar os requisitos na máquina virtual;
    - Ao executar o "Monta o GoogleDrive para uso" é preciso autorizar o acesso ao GoogleDrive;

![imagem2](./images/image2.png)

* Executadas as opções acima, basta executar o resto do código;
![imagem3](./images/image3.png)

* Ao final, os documentos de apoio serão gerados nas pastas do `Colab_cri`


## Grupo de trabalho:

- Concerne
    - Alceu Eilert Nascimento

- 1º Serviço de Registro de Imóveis de Curitiba
    - Luis Flávio Fidelis Gonçalves
    - Tayrini Vitali Felisberto Frol
    - Mactus Informática LTDA

- Incorporador
    - InvesPark
    - Michelle Beber
    - Luiz Augusto Brenner Rose
    - Cristiane Bajerski 
    - Dr.ª Vanessa Ponciano
    - Dr.ª Adriana Meneghin


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

{cri.unidade_especie} {cri.unidade_id}: possuindo esta unidade as seguintes áreas construídas: área privativa de {quadro resumo_04B; coluna A) metros quadrados, área comum de {quadro_areas_04B; coluna_E} metros quadrados, perfazendo a área construída de {quadro_areas_04B; coluna_F} metros quadrados; cabendo-lhe, a fração ideal de solo e partes comuns de {quadro_areas_04B; coluna_G} e quota de terreno de {quadro_areas_resumo; coluna_quota_de_terreno}  metros quadrados. Localização: localiza-se no {quadro_areas_05}, sendo que para quem entra na unidade, confronta pela frente com {cri.confrontacao_frente}, pelo lado direito com {cri.confrontacao_direita}, pelo lado esquerdo com {cri.confrontacao_esquerda} e pelo fundo {confrontacao_fundos}.


## Referências