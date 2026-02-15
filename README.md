# Airflow-Kafka-MongoDB-MySQL Pipeline

A production-ready ETL pipeline integrating Apache Airflow, Kafka, MongoDB, and MySQL. This project demonstrates modern data engineering practices with proper security, testing, and documentation.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for local development)
- Git

### Windows (PowerShell)

```powershell
# Clone the repository
git clone https://github.com/george-mendonca/airflow-kafka-mongodb-mysql-pipeline.git
cd airflow-kafka-mongodb-mysql-pipeline

# Copy environment variables
Copy-Item .env.example .env

# Edit .env with your credentials (use your preferred editor)
notepad .env

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### Linux/Mac (Bash)

```bash
# Clone the repository
git clone https://github.com/george-mendonca/airflow-kafka-mongodb-mysql-pipeline.git
cd airflow-kafka-mongodb-mysql-pipeline

# Copy environment variables
cp .env.example .env

# Edit .env with your credentials
nano .env  # or vim, code, etc.

# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

## 📋 Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Airflow Connections Setup](#airflow-connections-setup)
- [Service Access URLs](#service-access-urls)
- [Kafka Usage](#kafka-usage)
- [Database Clients](#database-clients)
- [Running Tests](#running-tests)
- [Security Best Practices](#security-best-practices)
- [Development Guide](#development-guide)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   MongoDB   │────▶│   Airflow   │────▶│    MySQL    │
│  (Source)   │     │  (Orchestr) │     │ (Warehouse) │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Kafka    │
                    │ (Streaming) │
                    └─────────────┘
```

**Data Flow:**
1. **Extract**: Read data from MongoDB collections
2. **Transform**: Apply business logic and data cleansing
3. **Load**: Write to MySQL warehouse and stream to Kafka topics

## 📁 Project Structure

```
airflow-kafka-mongodb-mysql-pipeline/
├── config/
│   ├── airflow_connections.py  # Airflow connection management
│   └── settings.py             # Application configuration
├── dags/
│   └── etl_pipeline.py         # Airflow DAG definitions
├── data/
│   ├── sample_input.json       # Example input data
│   └── sample_output.json      # Example transformed data
├── src/
│   ├── clients/
│   │   ├── kafka_client.py     # Kafka producer/consumer
│   │   ├── mongodb_client.py   # MongoDB CRUD operations
│   │   └── mysql_client.py     # MySQL CRUD operations
│   ├── services/
│   │   └── etl_service.py      # ETL business logic
│   └── utils/
│       └── logger.py           # Centralized logging
├── tests/
│   ├── test_mongodb_client.py  # MongoDB unit tests
│   ├── test_mysql_client.py    # MySQL unit tests
│   └── test_etl_service.py     # ETL service tests
├── docker-compose.yml          # Service orchestration
├── requirements.txt            # Python dependencies
└── .env.example               # Environment variables template
```

## 🔗 Airflow Connections Setup

Airflow needs connection configurations to interact with external services.

### Method 1: Command Line (Recommended)

```bash
# Run the connection setup script
python config/airflow_connections.py

# Or view UI instructions
python config/airflow_connections.py --ui-instructions
```

### Method 2: Airflow Web UI

1. Access Airflow at http://localhost:8080
2. Navigate to **Admin > Connections**
3. Click the **+** button to add connections

**MySQL Connection:**
- Conn Id: `mysql_default`
- Conn Type: `MySQL`
- Host: `mysql` (Docker service name)
- Schema: `mydatabase`
- Login: `user`
- Password: `password`
- Port: `3306`

**MongoDB Connection:**
- Conn Id: `mongodb_default`
- Conn Type: `Mongo`
- Host: `mongodb`
- Port: `27017`
- Extra: `{"uri": "mongodb://mongodb:27017/"}`

**Kafka Connection:**
- Conn Id: `kafka_default`
- Conn Type: `Generic`
- Extra: `{"bootstrap_servers": "kafka:9092"}`

## 🌐 Service Access URLs

When running with Docker Compose:

| Service   | URL                          | Purpose                          |
|-----------|------------------------------|----------------------------------|
| Airflow   | http://localhost:8080        | DAG management and monitoring    |
| MongoDB   | mongodb://localhost:27017    | Document database                |
| MySQL     | localhost:3306               | Relational warehouse             |
| Kafka     | localhost:9092               | Message streaming                |
| Zookeeper | localhost:2181               | Kafka coordination               |

**Default Credentials:**
- MySQL: `user` / `password`
- MongoDB: No authentication (development mode)
- Airflow: Set up on first access

## 📨 Kafka Usage

### Creating Topics

```bash
# Enter Kafka container
docker exec -it <kafka_container_id> bash

# Create a topic
kafka-topics.sh --create \
  --topic my_topic \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092
```

### Producer Example (Python)

```python
from src.clients.kafka_client import KafkaClientProducer

# Initialize producer
producer = KafkaClientProducer(bootstrap_servers=['kafka:9092'])

# Send message
message = {
    "id": 123,
    "event": "order_created",
    "timestamp": "2024-01-20T10:30:00Z"
}
producer.send_message('my_topic', message)
```

### Consumer Example (Python)

```python
from src.clients.kafka_client import KafkaClientConsumer

# Initialize consumer
consumer = KafkaClientConsumer(
    bootstrap_servers=['kafka:9092'],
    group_id='my_consumer_group'
)

# Consume messages
consumer.consume_messages('my_topic')
```

### Console Consumer (Testing)

```bash
# Enter Kafka container
docker exec -it <kafka_container_id> bash

# Consume messages from topic
kafka-console-consumer.sh \
  --topic my_topic \
  --bootstrap-server localhost:9092 \
  --from-beginning
```

## 🗄️ Database Clients

### MongoDB Client

```python
from src.clients.mongodb_client import MongoDBClient

# Initialize client
mongo = MongoDBClient("mongodb://mongodb:27017/mydatabase")

# Create document
doc_id = mongo.create("users", {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
})

# Read document
user = mongo.read("users", {"name": "John Doe"})

# Update document
mongo.update("users", 
    {"name": "John Doe"}, 
    {"age": 31, "email": "john.doe@example.com"}
)

# Delete document
mongo.delete("users", {"name": "John Doe"})
```

### MySQL Client

```python
from src.clients.mysql_client import MySQLClient

# Initialize client
mysql = MySQLClient(
    host='mysql',
    user='user',
    password='password',
    database='mydatabase'
)

# Insert record
user_id = mysql.insert("users", {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 25
})

# Select records
users = mysql.select("users", where={"age": 25})

# Update record
mysql.update("users", 
    {"age": 26}, 
    where={"name": "Jane Smith"}
)

# Delete record
mysql.delete("users", where={"name": "Jane Smith"})

# Close connection
mysql.close()
```

### ETL Service

```python
from src.services.etl_service import ETLService
from src.clients.mongodb_client import MongoDBClient
from src.clients.mysql_client import MySQLClient
from src.clients.kafka_client import KafkaClientProducer

# Initialize clients
mongo = MongoDBClient("mongodb://mongodb:27017/mydatabase")
mysql = MySQLClient(host='mysql', user='user', password='password', database='mydatabase')
kafka = KafkaClientProducer(bootstrap_servers=['kafka:9092'])

# Initialize ETL service
etl = ETLService(mongo, mysql, kafka)

# Run ETL pipeline
etl.run()
```

## 🧪 Running Tests

The project includes unit tests for all major components.

### Run All Tests

```bash
# From project root
python -m pytest tests/

# With verbose output
python -m pytest tests/ -v

# With coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test Files

```bash
# MongoDB client tests
python -m pytest tests/test_mongodb_client.py

# MySQL client tests
python -m pytest tests/test_mysql_client.py

# ETL service tests
python -m pytest tests/test_etl_service.py
```

### Run Individual Tests

```bash
# Run a specific test
python -m pytest tests/test_mongodb_client.py::TestMongoDBClient::test_insert_document
```

## 🔐 Security Best Practices

### 1. Environment Variables

**Never commit `.env` files with real credentials!**

✅ **DO:**
- Use `.env.example` as a template
- Store actual `.env` locally (it's in `.gitignore`)
- Use different credentials for each environment

❌ **DON'T:**
- Commit `.env` to version control
- Use default passwords in production
- Share credentials in plain text

### 2. Credential Management

**Windows (PowerShell):**
```powershell
# Store in Windows Credential Manager
cmdkey /generic:MyApp /user:username /pass:password

# Use environment variables (session only)
$env:MYSQL_PASSWORD = "your_secure_password"
```

**Linux/Mac:**
```bash
# Use direnv (recommended)
# Install: https://direnv.net/
echo 'export MYSQL_PASSWORD="your_secure_password"' >> .envrc
direnv allow

# Or use pass (password manager)
pass insert mysql/password
```

### 3. Production Deployment

- [ ] Use SSL/TLS for all database connections
- [ ] Enable authentication for MongoDB
- [ ] Use SASL/SSL for Kafka
- [ ] Implement network segmentation
- [ ] Set up VPN or bastion hosts for database access
- [ ] Use secrets management (AWS Secrets Manager, Vault)
- [ ] Enable audit logging
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Backup encryption

### 4. Docker Compose Security

For production, update `docker-compose.yml`:

```yaml
services:
  mongodb:
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
  
  mysql:
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
```

## 💻 Development Guide

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking (if using mypy)
mypy src/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/my-feature`
2. Write tests first (TDD approach)
3. Implement feature
4. Run tests: `pytest tests/`
5. Update documentation
6. Submit pull request

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs

# Check specific service
docker-compose logs mongodb
docker-compose logs kafka

# Restart services
docker-compose restart
```

### Connection Refused Errors

**Inside Docker containers:** Use service names (`mysql`, `mongodb`, `kafka`)
**From host machine:** Use `localhost`

```python
# Inside Docker container
MongoDBClient("mongodb://mongodb:27017")

# From host machine
MongoDBClient("mongodb://localhost:27017")
```

### Kafka Topics Not Found

```bash
# List topics
docker exec -it <kafka_container> kafka-topics.sh --list --bootstrap-server localhost:9092

# Create missing topic
docker exec -it <kafka_container> kafka-topics.sh --create --topic my_topic --bootstrap-server localhost:9092
```

### Permission Denied

```bash
# Fix file permissions
chmod +x config/airflow_connections.py

# Fix directory permissions
chmod -R 755 logs/
```

## 📚 Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

See [CONTRIBUTING.md](docs/CONTRIBUINDO.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 📧 Contact

George Mendonça - [GitHub Profile](https://github.com/george-mendonca)

Project Link: https://github.com/george-mendonca/airflow-kafka-mongodb-mysql-pipeline

---

**Built with ❤️ for the data engineering community**
