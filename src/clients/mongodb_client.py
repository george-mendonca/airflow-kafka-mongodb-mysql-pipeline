"""
Cliente MongoDB para operações CRUD no banco de dados.

Este módulo fornece uma interface simplificada para realizar operações
de Create, Read, Update e Delete (CRUD) em um banco de dados MongoDB.
"""

from pymongo import MongoClient as PyMongoClient
from typing import Dict, List, Any, Optional


class MongoDBClient:
    """
    Cliente para operações CRUD em banco de dados MongoDB.
    
    Esta classe fornece métodos para conectar, criar, ler, atualizar
    e deletar documentos em coleções MongoDB.
    """
    
    def __init__(self, uri: str, db_name: str):
        """
        Inicializa a conexão com o banco de dados MongoDB.
        
        Args:
            uri: URI de conexão do MongoDB (ex: 'mongodb://localhost:27017/')
            db_name: Nome do banco de dados
        """
        self.uri = uri
        self.db_name = db_name
        self.client = PyMongoClient(uri)
        self.db = self.client[db_name]
    
    def insert_document(self, collection_name: str, document: Dict[str, Any]) -> str:
        """
        Insere um documento na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            document: Documento a ser inserido (dicionário)
        
        Returns:
            ID do documento inserido (string)
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na inserção
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return str(result.inserted_id)
    
    def insert_many(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """
        Insere múltiplos documentos na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            documents: Lista de documentos a serem inseridos
        
        Returns:
            Lista de IDs dos documentos inseridos (strings)
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na inserção
        """
        collection = self.db[collection_name]
        result = collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    def find(self, collection_name: str, query: Optional[Dict[str, Any]] = None, 
             projection: Optional[Dict[str, int]] = None, limit: int = 0) -> List[Dict[str, Any]]:
        """
        Busca documentos na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro de busca (opcional, padrão: {})
            projection: Dicionário especificando quais campos incluir/excluir (opcional)
            limit: Número máximo de documentos a retornar (0 = sem limite)
        
        Returns:
            Lista de documentos encontrados
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na busca
        """
        collection = self.db[collection_name]
        query = query or {}
        
        cursor = collection.find(query, projection)
        
        if limit > 0:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def find_one(self, collection_name: str, query: Dict[str, Any], 
                 projection: Optional[Dict[str, int]] = None) -> Optional[Dict[str, Any]]:
        """
        Busca um único documento na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro de busca
            projection: Dicionário especificando quais campos incluir/excluir (opcional)
        
        Returns:
            Documento encontrado ou None se não encontrado
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na busca
        """
        collection = self.db[collection_name]
        return collection.find_one(query, projection)
    
    def update(self, collection_name: str, query: Dict[str, Any], 
               update_values: Dict[str, Any]) -> int:
        """
        Atualiza um documento na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro para encontrar o documento
            update_values: Dicionário com os valores a serem atualizados
        
        Returns:
            Número de documentos modificados
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na atualização
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update_values})
        return result.modified_count
    
    def update_many(self, collection_name: str, query: Dict[str, Any], 
                    update_values: Dict[str, Any]) -> int:
        """
        Atualiza múltiplos documentos na coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro para encontrar os documentos
            update_values: Dicionário com os valores a serem atualizados
        
        Returns:
            Número de documentos modificados
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na atualização
        """
        collection = self.db[collection_name]
        result = collection.update_many(query, {'$set': update_values})
        return result.modified_count
    
    def delete(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Remove um documento da coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro para encontrar o documento
        
        Returns:
            Número de documentos removidos
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na remoção
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
    
    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
        """
        Remove múltiplos documentos da coleção especificada.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro para encontrar os documentos
        
        Returns:
            Número de documentos removidos
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na remoção
        """
        collection = self.db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count
    
    def count_documents(self, collection_name: str, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Conta o número de documentos na coleção que correspondem ao filtro.
        
        Args:
            collection_name: Nome da coleção
            query: Dicionário com o filtro de busca (opcional, padrão: {})
        
        Returns:
            Número de documentos encontrados
        
        Raises:
            pymongo.errors.PyMongoError: Se houver erro na contagem
        """
        collection = self.db[collection_name]
        query = query or {}
        return collection.count_documents(query)
    
    def close(self):
        """
        Fecha a conexão com o banco de dados MongoDB.
        """
        if self.client:
            self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
