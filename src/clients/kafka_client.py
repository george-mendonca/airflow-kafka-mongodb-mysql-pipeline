"""
Cliente Kafka para produção e consumo de mensagens.

Este módulo fornece implementações de cliente Kafka para produzir e consumir
mensagens de tópicos Kafka.
"""

from kafka import KafkaProducer, KafkaConsumer
import json
from typing import Any, Dict, Optional, Callable


class KafkaClientProducer:
    """
    Cliente produtor Kafka para enviar mensagens para tópicos.
    
    Este cliente é responsável por enviar mensagens para um tópico Kafka,
    com serialização automática para JSON.
    """
    
    def __init__(self, bootstrap_servers: str, topic: Optional[str] = None):
        """
        Inicializa o produtor Kafka.
        
        Args:
            bootstrap_servers: Endereço do servidor Kafka (ex: 'localhost:9092')
            topic: Tópico padrão para envio de mensagens (opcional)
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def send_message(self, message: Dict[str, Any], topic: Optional[str] = None):
        """
        Envia uma mensagem para o tópico Kafka.
        
        Args:
            message: Mensagem a ser enviada (será serializada para JSON)
            topic: Tópico para onde a mensagem será enviada (usa o tópico padrão se não especificado)
        
        Raises:
            ValueError: Se nenhum tópico for especificado
        """
        target_topic = topic or self.topic
        if not target_topic:
            raise ValueError("Tópico não especificado. Forneça um tópico ou defina um tópico padrão.")
        
        self.producer.send(target_topic, value=message)
        self.producer.flush()
    
    def close(self):
        """Fecha a conexão com o produtor Kafka."""
        if self.producer:
            self.producer.close()


class KafkaClientConsumer:
    """
    Cliente consumidor Kafka para receber mensagens de tópicos.
    
    Este cliente é responsável por consumir mensagens de um tópico Kafka,
    com deserialização automática de JSON.
    """
    
    def __init__(self, bootstrap_servers: str, topic: str, group_id: Optional[str] = None):
        """
        Inicializa o consumidor Kafka.
        
        Args:
            bootstrap_servers: Endereço do servidor Kafka (ex: 'localhost:9092')
            topic: Tópico do qual consumir mensagens
            group_id: ID do grupo de consumidores (opcional)
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        
        consumer_config = {
            'bootstrap_servers': bootstrap_servers,
            'value_deserializer': lambda x: json.loads(x.decode('utf-8'))
        }
        
        if group_id:
            consumer_config['group_id'] = group_id
        
        self.consumer = KafkaConsumer(topic, **consumer_config)
    
    def consume_messages(self, callback: Optional[Callable[[Any], None]] = None):
        """
        Consome mensagens do tópico Kafka.
        
        Args:
            callback: Função opcional para processar cada mensagem recebida.
                     Se não fornecida, as mensagens serão impressas no console.
        """
        for message in self.consumer:
            if callback:
                callback(message.value)
            else:
                print(f'Recebido: {message.value}')
    
    def close(self):
        """Fecha a conexão com o consumidor Kafka."""
        if self.consumer:
            self.consumer.close()
