# Poc-eng-dados-Azure-Neobank
## Overview
Welcome!! 🚀

Esse projeto se baseia na tendência onde cada vez mais é necessário riqueza de dados para gerar insights e valor ao negócio. Dessa forma, é proposta uma infraestrutura utilizando a cloud Azure para coletar, processar e armazenar os dados de forma escalável.

Para isso foi uma proposto uma arquitetura utilizando Data lake storage Gen 2 com três camadas sendo a bronze responsável pelo armazenamento dos dados originais em formato CSV, a silver armazenando os dados e utilizando o slow changing dimension tipo 2 para realizar a historização e por fim a camada ouro que estará disponível para armazenar dados mais estruturados para análise, todavia para esse caso a camada ouro será uma cópia da silver. Ainda sobre a arquitetura, o projeto conta com o Azure databricks responsável para realizar as transformações em cada camadas do data lake, Azure Databricks para orquestração e ativação dos notebooks de forma periódica e o Azure Synapse Analytics com a função de copiar e armazenar os dados da camada ouro e disponibilizar-los para a ferramenta de dataviz que será o PowerBi.
