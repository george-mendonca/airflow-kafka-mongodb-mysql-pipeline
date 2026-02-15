# Documentação de Instalação para o Repositório airflow-kafka-mongodb-mysql-pipeline

Esta documentação fornece instruções sobre como instalar e configurar o pipeline que utiliza Apache Airflow com Kafka, MongoDB e MySQL.

## Requisitos

Antes de iniciar a instalação, verifique se você tem os seguintes pré-requisitos instalados:

- Python 3.6 ou superior
- Apache Airflow
- Kafka
- MongoDB
- MySQL
- Pip 20+ (gerenciador de pacotes de Python)

## Passos para Instalação

### 1. Clonar o Repositório

Clone o repositório usando o comando:
```bash
git clone https://github.com/<owner>/airflow-kafka-mongodb-mysql-pipeline.git
cd airflow-kafka-mongodb-mysql-pipeline
```

### 2. Criar um Ambiente Virtual

Recomendamos criar um ambiente virtual para gerenciar as dependências do projeto:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3. Instalar Dependências

Instale as dependências necessárias com o seguinte comando:
```bash
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados MySQL

Antes de iniciar o pipeline, você precisa configurar o banco de dados MySQL. Siga estes passos:

- Crie um banco de dados no MySQL:
```sql
CREATE DATABASE nome_do_banco;
```
- Configure as credenciais de acesso no arquivo de configuração do Airflow.

### 5. Configurar o MongoDB

Certifique-se de que o MongoDB esteja em execução e crie um banco de dados se necessário:
```bash
mongo
use nome_do_banco;
```

### 6. Iniciar Kafka

Inicie o Kafka e as suas dependências:
```bash
# Inicie o Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties
# Inicie o Kafka
bin/kafka-server-start.sh config/server.properties
```

### 7. Iniciar o Airflow

Finalize a configuração do Airflow:
- Inicialize o banco de dados do Airflow:
```bash
airflow db init
```
- Inicie o servidor web do Airflow:
```bash
airflow webserver --port 8080
```
- Em outro terminal, inicie o executor:
```bash
airflow scheduler
```

### 8. Acessar a Interface do Airflow

Abra seu navegador e acesse `http://localhost:8080` para visualizar a interface do Airflow.

## Conclusão

Após seguir todas as etapas acima, seu pipeline deve estar funcionando corretamente. Para mais informações, consulte a documentação oficial de cada ferramenta: Airflow, Kafka, MongoDB e MySQL.