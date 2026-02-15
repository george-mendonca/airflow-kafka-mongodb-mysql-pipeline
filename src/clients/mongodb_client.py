# mongo_client.py

"""
Este arquivo contém a implementação de um cliente MongoDB em Python.
O cliente se conecta a um banco de dados MongoDB e fornece
métodos para interagir com a coleção.

Exemplo de uso:

    from mongo_client import MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    db = client['meu_banco']
    collection = db['minha_colecao']
    client.insert_document({'chave': 'valor'})
"""

from pymongo import MongoClient as PyMongoClient

class MongoClient:
    def __init__(self, uri, db_name):
        self.client = PyMongoClient(uri)
        self.db = self.client[db_name]

    def insert_document(self, document):
        """Insere um documento na coleção padrão."""
        self.db.minha_colecao.insert_one(document)

    def find_document(self, query):
        """Encontra um documento com base na consulta especificada."""
        return self.db.minha_colecao.find_one(query)

    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.client.close()
