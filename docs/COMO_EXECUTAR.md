# Como Executar o Pipeline

Este documento contém instruções sobre como executar o pipeline de Kafka, MongoDB e MySQL.

## Passo 1: Configurar o Ambiente

1. Certifique-se de ter o Java JDK instalado.
2. Instale o Apache Kafka.
3. Instale o MongoDB.
4. Instale o MySQL.
5. Clonar o repositório: `git clone https://github.com/george-mendonca/airflow-kafka-mongodb-mysql-pipeline`

## Passo 2: Configurar o Kafka

1. Inicie o servidor Kafka.
2. Crie os tópicos necessários usando os comandos do Kafka.

## Passo 3: Configurar o MongoDB e MySQL

1. Inicie o MongoDB e o MySQL.
2. Configure os bancos de dados conforme necessário.

## Passo 4: Executar o Pipeline

1. Navegue até o diretório do projeto: `cd airflow-kafka-mongodb-mysql-pipeline`
2. Execute o pipeline usando o comando: `airflow dags trigger nome_do_dag`

## Considerações Finais

Verifique os logs do Airflow para garantir que o pipeline está sendo executado corretamente.