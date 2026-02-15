import os
from dotenv import load_dotenv

load_dotenv()

# Airflow
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
EXECUTOR = os.getenv("EXECUTOR", "LocalExecutor")

# Kafka
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "my_topic")

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mydatabase")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "my_collection")

# MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "mydatabase")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
