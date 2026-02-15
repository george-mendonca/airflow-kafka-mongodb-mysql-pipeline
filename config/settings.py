# Configuration settings for the Airflow-Kafka-MongoDB-MySQL pipeline

# Airflow configurations
AIRFLOW_HOME = '/usr/local/airflow'
EXECUTOR = 'LocalExecutor'

# Kafka settings
KAFKA_BROKER_URL = 'localhost:9092'
KAFKA_TOPIC = 'my_topic'

# MongoDB configuration
MONGODB_URI = 'mongodb://localhost:27017/mydatabase'
MONGODB_COLLECTION = 'my_collection'

# MySQL configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'user'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'mydatabase'

# Environment
ENVIRONMENT = 'development'  # Change to 'production' for production settings
