# Data Generator

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
### Stack Utilizadas:
- Python
- Mysql/MariaDB
- JinjaSql
- Pandas
- Bash Scripting
- SQL Power Architect
- Datalake

### Decisões tomadas:
- A quantidade de dados armazenados e a quantidade de requisições ao banco implicam diretamente na performance do pipeline. Dessa forma, no caso estudado,
    - a utilização de armazenadores locais temporários (como dicionários) para as tabelas com menor quantidade de dados e que necessitavam de muitas requisições foram preteridas. Requisições podem ser custosas caso sejam realizadas de maneira massante
    - e para casos opostos, optou-se pela requisição direta ao banco por, além de não haver necessidade na utilização de todos os dados, teria-se um aumento proporcial de processamento conforme o aumento de informação nas tabelas. 

### Modelagem do Banco de Dados:
- Modelagem Relacional
- Estrutura:

![Logical Model](imgs/logical_model.PNG) 

### Pontos obeservados no caso estudado:
- A utilização dicionários como estrutura de dados proporcionou uma melhora significativa, em questão de velocidade de tranporte e processamento, no pipeline de dados quando comparado com o pandas dataframe. 
- A carga de dados através de arquivos CSV proporcionou uma inserção de dados no banco de até 10x mais rápida se comprado com a função ```to_sql``` do pandas dataframe.
    - Alguns motivos: 
        - Não há análise de sql,
        - Os dados são lidos em grandes blocos,
        - Os índices não exclusivos da tabela são desabilitados durante a operação caso ela esteja vazia e
        - O engine armazena antes em cache para depois inseri-las em grandes blocos.
        
### Próximos Passos:
- Gerar relatórios para comprovar o insights descritos
- Criar ambiente em docker
- Utilizar um orquestrador/scheduler (Airflow)
- Gerar insights através da base gerada (desenvolver KPIs para monitoramento)
