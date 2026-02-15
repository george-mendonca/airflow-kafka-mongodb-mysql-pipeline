"""
Este script contém um pipeline ETL (Extrair, Transformar, Carregar) utilizando o Apache Airflow, Kafka e MongoDB.
O objetivo é extrair dados de uma fonte, transformá-los conforme necessário e, em seguida, carregá-los em um banco de dados MongoDB.

As seguintes operações são realizadas:
1.  Extração de dados de uma fonte (pode ser um arquivo, API, etc.).
2.  Transformação dos dados extraídos de acordo com as regras de negócio específicas.
3.  Carregamento dos dados transformados no MongoDB.

As funções são documentadas para facilitar a compreensão e a manutenção por outros desenvolvedores.

Autor: George Mendonça
Data: 2026-02-15
"""


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import requests
import pymongo


# Função para extrair dados de uma fonte
def extraindo_dados():
    """
    Esta função extrai dados de uma fonte externa.
    A fonte pode ser uma API ou outro local de onde os dados podem ser coletados.
    """
    response = requests.get('URL_DA_FONTE')  # Substitua pela URL real.
    if response.status_code == 200:
        return response.json()  # Retorna dados em formato JSON.
    else:
        raise Exception('Falha ao extrair dados')


# Função para transformar dados extraídos
def transformando_dados(dados):
    """
    Esta função aplica transformações nos dados extraídos.
    Pode incluir funções de limpeza, formatação e enriquecimento.
    Argumentos:
    dados: Dados que precisam ser transformados.
    """
    # Exemplo de transformação simples
    dados_transformados = [dado for dado in dados if dado['valor'] > 0]  # Filtra dados inválidos.
    return dados_transformados


# Função para carregar dados no MongoDB
def carregando_dados(dados):
    """
    Esta função carrega os dados transformados em uma coleção do MongoDB.
    Argumentos:
    dados: Dados que foram transformados e estão prontos para serem carregados.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['nome_do_banco']  # Substitua pelo nome real do banco.
    collection = db['nome_da_colecao']  # Substitua pelo nome real da coleção.
    collection.insert_many(dados)  # Insere dados em lote.


# Configuração do DAG do Airflow
default_args = {
    'owner': 'george-mendonca',
    'start_date': datetime(2026, 2, 15),
}

dag = DAG('etl_pipeline', default_args=default_args, schedule_interval='@daily')


# Operações do DAG
extraindo = PythonOperator(
    task_id='extraindo_dados',
    python_callable=extraindo_dados,
    dag=dag,
)

transformando = PythonOperator(
    task_id='transformando_dados',
    python_callable=transformando_dados,
    op_kwargs={'dados': extraindo.output},
    dag=dag,
)

carregando = PythonOperator(
    task_id='carregando_dados',
    python_callable=carregando_dados,
    op_kwargs={'dados': transformando.output},
    dag=dag,
)

extraindo >> transformando >> carregando  # Define a ordem das operações.