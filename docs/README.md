# Airflow Kafka MongoDB MySQL Pipeline

## Overview
This project provides a robust data pipeline leveraging Apache Airflow for orchestration, Kafka for data streaming, and both MongoDB and MySQL as storage solutions. The primary objective is to streamline the process of moving data between these systems efficiently and reliably.

## Description
The pipeline is designed to automate the extraction, transformation, and loading (ETL) of data from various sources into MongoDB and MySQL databases. It utilizes Kafka as an intermediary to ensure data is processed in real-time, allowing for live data updates.

## Technologies Used
- **Apache Airflow**: For orchestrating the workflow.
- **Apache Kafka**: For real-time data streaming.
- **MongoDB**: NoSQL database for storing semi-structured data.
- **MySQL**: Relational database for structured data storage.
- **Python**: Primary programming language used for interaction with these technologies.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/george-mendonca/airflow-kafka-mongodb-mysql-pipeline.git
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables for database connections and Kafka.

## Usage
- Start your Kafka server and ensure your topics are created.
- Start MongoDB and MySQL services.
- Run Airflow to initiate the pipeline:
   ```bash
   airflow scheduler
   airflow webserver
   ```
- Trigger the DAG through the Airflow UI to start processing.

## Contributing
Contributions are welcome! Please fork the repo and submit a pull request for any updates or improvements.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
