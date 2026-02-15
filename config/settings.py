"""
Application Settings Configuration

This module centralizes all configuration settings for the ETL pipeline.
Settings are loaded from environment variables with sensible defaults.

IMPORTANT NOTES:

1. DOCKER COMPOSE vs LOCAL DEVELOPMENT:
   - Default values use Docker service names (mysql, mongodb, kafka)
   - These work when running inside Docker containers
   - For local development outside Docker, override these with localhost in .env
   
2. CONTAINER-AWARE DEFAULTS:
   - MYSQL_HOST defaults to "mysql" (Docker service name)
   - MONGODB_URI defaults to "mongodb://mongodb:27017" (Docker service name)
   - KAFKA_BROKER_URL defaults to "kafka:9092" (Docker service name)
   
3. USAGE:
   Inside Docker Compose:
     - Use default values (already configured for Docker)
   
   Local Development:
     - Create .env file from .env.example
     - Set hosts to localhost:
       MYSQL_HOST=localhost
       MONGODB_URI=mongodb://localhost:27017/mydatabase
       KAFKA_BROKER_URL=localhost:9092

PRODUCTION DEPLOYMENT CHECKLIST:

[ ] Use environment-specific .env files (.env.production, .env.staging)
[ ] Store sensitive credentials in a secure vault (AWS Secrets Manager, HashiCorp Vault)
[ ] Never commit .env files with real credentials to version control
[ ] Use SSL/TLS for database connections in production
[ ] Implement proper authentication for Kafka (SASL, SSL)
[ ] Set LOG_LEVEL to WARNING or ERROR in production
[ ] Configure proper backup strategies for MongoDB and MySQL
[ ] Set up monitoring and alerting for all services
[ ] Use connection pooling for database connections
[ ] Implement retry logic with exponential backoff
[ ] Configure resource limits in Docker Compose for production
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# AIRFLOW CONFIGURATION
# =============================================================================
AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", "/usr/local/airflow")
EXECUTOR = os.getenv("EXECUTOR", "LocalExecutor")

# =============================================================================
# KAFKA CONFIGURATION
# =============================================================================
# Docker service name: kafka
# For local development: localhost:9092
KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "kafka:9092")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "my_topic")
KAFKA_TOPIC_RAW = os.getenv("KAFKA_TOPIC_RAW", "raw_data")
KAFKA_TOPIC_PROCESSED = os.getenv("KAFKA_TOPIC_PROCESSED", "processed_data")

# =============================================================================
# MONGODB CONFIGURATION
# =============================================================================
# Docker service name: mongodb
# For local development: mongodb://localhost:27017/mydatabase
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://mongodb:27017/mydatabase")
MONGODB_HOST = os.getenv("MONGODB_HOST", "mongodb")
MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "mydatabase")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "my_collection")
MONGODB_USER = os.getenv("MONGODB_USER", "")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "")

# =============================================================================
# MYSQL CONFIGURATION
# =============================================================================
# Docker service name: mysql
# For local development: localhost
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "mydatabase")

# =============================================================================
# PIPELINE CONFIGURATION
# =============================================================================
PIPELINE_BATCH_SIZE = int(os.getenv("PIPELINE_BATCH_SIZE", "100"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# =============================================================================
# ENVIRONMENT
# =============================================================================
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
