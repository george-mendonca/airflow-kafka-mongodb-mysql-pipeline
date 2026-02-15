# Kafka Client

## Produtor Kafka

Este código implementa um produtor Kafka em Python. O produtor é responsável por enviar mensagens para um tópico Kafka.

```python
from kafka import KafkaProducer
import json

class KafkaProducerClient:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send_message(self, topic, message):
        self.producer.send(topic, value=message)
        self.producer.flush()

# Exemplo de uso do produtor
producer = KafkaProducerClient('localhost:9092')
producer.send_message('meu_topico', {'key': 'value'})
```

## Consumidor Kafka

Este código implementa um consumidor Kafka em Python. O consumidor é responsável por ler mensagens de um tópico Kafka.

```python
from kafka import KafkaConsumer
import json

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers, topic):
        self.consumer = KafkaConsumer(topic,
                                       bootstrap_servers=bootstrap_servers,
                                       value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    def consume_messages(self):
        for message in self.consumer:
            print(f'Recebido: {message.value}')

# Exemplo de uso do consumidor
consumer = KafkaConsumerClient('localhost:9092', 'meu_topico')
consumer.consume_messages()
```
