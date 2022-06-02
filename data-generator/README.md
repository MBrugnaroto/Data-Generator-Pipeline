# Data Generator
Projeto pessoal em desenvolvimento para estudo dos principais conceitos e stacks utilizados na área de Engenharia de Dados (ED). O projeto consiste no desenvolvimento de um gerador de dados, alimentação de um banco de dados estruturado e na modelagem de visualizações de Key Performance Indicators (KPIs).

### Objetivos:
- Aumento na compreensão acerca de pipelines de dados
- Aprimoramento na utilização das seguintes stacks:
    - Apache Airflow
    - Docker
    - Python
    - Apache Spark
    - Jinja Templates
    - SQL

### Estrutura de diretórios
```
├── /src (data-generator)
|   ├── /app
|   |   ├── /dags
|   |   ├── /plugins
|   |   |   ├── /hooks
|   |   |   ├── /operators
|   |   |   ├── /utils
|   ├── /datalake
|   |   ├── /silver (preprocessed)
|   |   |   ├── /DB_NAME
|   |   |   |   ├── /SUBFOLDER1
|   |   |   |   ├── ...
|   ├── /imgs
```
### Stack Utilizadas até o momento:
- Python
- Mysql/MariaDB
- JinjaSql
- Pandas
- Bash Scripting
- SQL Power Architect
- Datalake

### Modelagem do Banco de Dados:
- Modelagem Relacional
- Estrutura:

![Logical Model](imgs/logical_model.PNG) 

### Decisões tomadas:
- A quantidade de dados armazenados e a quantidade de requisições ao banco implicam diretamente na performance do pipeline. Dessa forma, para que o processo de geração de dados se tornasse escalável
    - a utilização de armazenadores locais temporários (como dicionários) foram preteridos para as tabelas com menor quantidade de dados e que necessitavam de muitas requisições. Requisições ao banco podem ser custosas caso sejam realizadas de maneira massante.
    - Para casos opostos, optou-se pela requisição direta ao banco porque, além de não haver necessidade na utilização de todos os dados, teria-se um aumento proporcial de processamento conforme o aumento de informação nessas tabelas. 

### Pontos obeservados no caso estudado:
- A utilização dicionários como estrutura de dados proporcionou uma melhora significativa, em questão de velocidade de transporte e processamento, no pipeline de dados quando comparado com o pandas dataframe. 
- A carga de dados através de arquivos CSV proporcionou uma inserção de dados no banco de até 10x mais rápida se comprado com a função ```to_sql``` do pandas dataframe.
    - Principalmente por dois motivos: 
        - Não há análise de sql e
        - O engine armazena antes em cache para depois inseri as informações em grandes blocos.
        
### Próximos Passos:
- Gerar relatórios para comprovar o insights descritos
- Criar ambiente em docker
- Utilizar um orquestrador/scheduler (Airflow)
- Gerar insights através da base gerada (desenvolver KPIs para monitoramento)
