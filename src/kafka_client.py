from kafka import KafkaProducer, KafkaConsumer

class KafkaProducerClient:
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.topic = topic

    def send_message(self, message):
        self.producer.send(self.topic, value=message)
        self.producer.flush()

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)

    def consume_messages(self):
        for message in self.consumer:
            print(f'Consumed message: {message.value}')