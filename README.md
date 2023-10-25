# Poc-eng-dados-Azure-Neobank
## Overview
Welcome!! 🚀

Esse projeto se baseia na tendência onde cada vez mais é necessário riqueza, qualidade, escalabilidade e segurança dos dados para gerar insights e valor ao negócio. Dessa forma, é proposta uma infraestrutura utilizando a cloud Azure para coletar, processar e armazenar os dados de forma escalável.

Para isso foi uma proposto uma arquitetura utilizando Data lake storage Gen 2 com três camadas sendo a bronze responsável pelo armazenamento dos dados originais em formato CSV, a silver armazenando os dados e utilizando o slow changing dimension tipo 2 para realizar a historização e por fim a camada ouro que estará disponível para armazenar dados mais estruturados para análise, será utilizada para remoção de dados sensíveis que não podem ser disponibilizados diretamente para os analistas.
Ainda sobre a arquitetura, o projeto conta com o Azure databricks responsável para realizar as transformações em cada camadas do data lake, Azure Factory para ingestão dos dados, orquestração e ativação dos notebooks de forma periódica e o Azure Synapse Analytics com a função de copiar e armazenar os dados da camada ouro e disponibilizar-los para a ferramenta de dataviz que será o PowerBi.


<img src="/Imagens/azure-pipeline-schematic.drawio.png">

### Contexto do negócio
NeoBank é um banco que está disparando seu crescimento. Visto isso, a empresa está investindo em testes relacionados a cloud para crescer sua infraestrutura dentro da nuvem gerando soluções que escalem de acordo com a velocidade do seu crescimento. Visto isso, foi direcionado para o time de engenharia de dados, realizar uma poc(prova de conceito) disponibilizando dados relacionados a clientes do banco para que o time de análise de dados possa criar relatórios e extrair informações valiosas dos novos clientes e continuar a monitorar os anitigos. 

### Base de dados
A base é um arquivo .csv anexado neste repositório onde possui 16 colunas e 10000 linhas de dados realcionados aos clientes do banco Neobank. Esta poc inclui a ingestão, transformação e carregamento desta dimensão.  

### Grupo de recursos
Para começar o desenvolvimento do projeto, foi criado um grupo de recursos destinado a manter os recursos que compõem a solução. Esse recurso também traz o benefício de monitorar todos os custos relacionados ao projeto.

### Storage account
Por meio da criação de containers foram criados as três camadas do data lake em modo privado:

<img src="/Imagens/containers.PNG">


## Ingestão 
Para extração dos dados e ingestão no data lake foi criado a partir da atividade Copy do Azure Datafactory onde o Source foi definido como uma fonte HTTP o qual está relacionada ao link do arquivo csv disponibilizado neste mesmo repositório e o Source do fluxo conectado a camada bronze do datalake gerando um arquivo com o mesmo nome da fonte. Para realizar esse processo, foi necessário a criação de um link de serviço conectando a storage account ao data factory.


<img src="/Imagens/copy.PNG">

## Transformação
Após a ingestão os dados estarão disponíveis para transformação, foi utilizado Azure databricks conectadose conectando ao data lake para tranformação dos dados gerando três scripts.


## Carregamento 

## Orquestração 

<img src="/Imagens/pipelineADF.PNG">

## Dashboard



  



## Informações da autor
<li>Nome: Emanuel de Almeida Alves</li>
<li>E-mail: emanuelalmeidaalves123@gmail.com</li>
<li>Linkedin: https://www.linkedin.com/in/emanueldealmeida/</li>
