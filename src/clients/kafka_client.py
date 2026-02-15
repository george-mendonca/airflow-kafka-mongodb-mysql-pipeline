from kafka import KafkaProducer, KafkaConsumer
import json

class KafkaClientProducer:
    """
    Classe KafkaClientProducer para produção de mensagens no Kafka.

    Métodos:
        send_message(topic: str, message: dict) -> None:
            Envia uma mensagem JSON para o tópico especificado no Kafka.
    """

    def __init__(self, bootstrap_servers: list):
        """
        Inicializa o produtor Kafka com os servidores bootstrap.

        Args:
            bootstrap_servers (list): Uma lista de endereços de servidores Kafka.
        """
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                       value_serializer=lambda v: json.dumps(v).encode('utf-8'))

    def send_message(self, topic: str, message: dict) -> None:
        """
        Envia uma mensagem JSON para o tópico especificado no Kafka.

        Args:
            topic (str): O nome do tópico para onde a mensagem será enviada.
            message (dict): O conteúdo da mensagem em formato de dicionário.
        """
        self.producer.send(topic, message)
        self.producer.flush()


class KafkaClientConsumer:
    """
    Classe KafkaClientConsumer para consumo de mensagens do Kafka.

    Métodos:
        consume_messages(topic: str) -> None:
            Consome mensagens do tópico especificado no Kafka.
    """

    def __init__(self, bootstrap_servers: list, group_id: str):
        """
        Inicializa o consumidor Kafka com os servidores bootstrap e o ID do grupo.

        Args:
            bootstrap_servers (list): Uma lista de endereços de servidores Kafka.
            group_id (str): O ID do grupo de consumidores.
        """
        self.consumer = KafkaConsumer(topic,
                                       bootstrap_servers=bootstrap_servers,
                                       group_id=group_id,
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8'))) 

    def consume_messages(self, topic: str) -> None:
        """
        Consome mensagens do tópico especificado no Kafka.

        Args:
            topic (str): O nome do tópico do qual as mensagens serão consumidas.
        """
        for message in self.consumer:
            print(f"Recebido: {message.value}")