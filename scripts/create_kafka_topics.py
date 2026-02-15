from kafka import KafkaAdminClient
from kafka.admin import NewTopic


def create_kafka_topics():
    admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')

    topics = [
        NewTopic(name='raw_events', num_partitions=3, replication_factor=1),
        NewTopic(name='processed_events', num_partitions=3, replication_factor=1),
        NewTopic(name='error_events', num_partitions=1, replication_factor=1)
    ]

    admin_client.create_topics(topics)
    print("Topics created successfully")

if __name__ == '__main__':
    create_kafka_topics()