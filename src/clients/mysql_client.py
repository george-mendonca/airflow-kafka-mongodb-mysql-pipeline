"""
Cliente MySQL para operações CRUD no banco de dados.

Este módulo fornece uma interface simplificada para realizar operações
de Create, Read, Update e Delete (CRUD) em um banco de dados MySQL.
"""

import mysql.connector
from typing import Dict, List, Any, Optional, Tuple


class MySQLClient:
    """
    Cliente para operações CRUD em banco de dados MySQL.
    
    Esta classe fornece métodos para conectar, criar, ler, atualizar
    e deletar registros em um banco de dados MySQL.
    """
    
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        Inicializa a conexão com o banco de dados MySQL.
        
        Args:
            host: Endereço do servidor MySQL
            user: Nome de usuário para conexão
            password: Senha para conexão
            database: Nome do banco de dados
            port: Porta do servidor MySQL (padrão: 3306)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """
        Estabelece conexão com o banco de dados MySQL.
        
        Raises:
            mysql.connector.Error: Se houver erro na conexão
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def create(self, table: str, data: Dict[str, Any]) -> int:
        """
        Insere um novo registro na tabela especificada.
        
        Args:
            table: Nome da tabela
            data: Dicionário com os dados a serem inseridos (coluna: valor)
        
        Returns:
            ID do registro inserido
        
        Raises:
            mysql.connector.Error: Se houver erro na inserção
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()
        
        return self.cursor.lastrowid
    
    def read(self, table: str, where: Optional[str] = None, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Busca registros da tabela especificada.
        
        Args:
            table: Nome da tabela
            where: Cláusula WHERE para filtrar resultados (opcional)
            params: Tupla com parâmetros para a cláusula WHERE (opcional)
        
        Returns:
            Lista de dicionários com os registros encontrados
        
        Raises:
            mysql.connector.Error: Se houver erro na consulta
        """
        sql = f"SELECT * FROM {table}"
        if where:
            sql += f" WHERE {where}"
        
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        return self.cursor.fetchall()
    
    def read_one(self, table: str, where: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Busca um único registro da tabela especificada.
        
        Args:
            table: Nome da tabela
            where: Cláusula WHERE para filtrar o resultado
            params: Tupla com parâmetros para a cláusula WHERE (opcional)
        
        Returns:
            Dicionário com o registro encontrado ou None se não encontrado
        
        Raises:
            mysql.connector.Error: Se houver erro na consulta
        """
        sql = f"SELECT * FROM {table} WHERE {where}"
        
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        return self.cursor.fetchone()
    
    def update(self, table: str, data: Dict[str, Any], where: str, params: Optional[Tuple] = None) -> int:
        """
        Atualiza registros na tabela especificada.
        
        Args:
            table: Nome da tabela
            data: Dicionário com os dados a serem atualizados (coluna: valor)
            where: Cláusula WHERE para identificar os registros
            params: Tupla com parâmetros adicionais para a cláusula WHERE (opcional)
        
        Returns:
            Número de registros afetados
        
        Raises:
            mysql.connector.Error: Se houver erro na atualização
        """
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        values = tuple(data.values())
        if params:
            values = values + params
        
        self.cursor.execute(sql, values)
        self.connection.commit()
        
        return self.cursor.rowcount
    
    def delete(self, table: str, where: str, params: Optional[Tuple] = None) -> int:
        """
        Remove registros da tabela especificada.
        
        Args:
            table: Nome da tabela
            where: Cláusula WHERE para identificar os registros a serem removidos
            params: Tupla com parâmetros para a cláusula WHERE (opcional)
        
        Returns:
            Número de registros removidos
        
        Raises:
            mysql.connector.Error: Se houver erro na remoção
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        
        self.connection.commit()
        
        return self.cursor.rowcount
    
    def execute_query(self, query: str, params: Optional[Tuple] = None):
        """
        Executa uma consulta SQL customizada.
        
        Args:
            query: Consulta SQL a ser executada
            params: Tupla com parâmetros para a consulta (opcional)
        
        Raises:
            mysql.connector.Error: Se houver erro na execução
        """
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        self.connection.commit()
    
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Executa uma consulta SELECT e retorna todos os resultados.
        
        Args:
            query: Consulta SQL SELECT
            params: Tupla com parâmetros para a consulta (opcional)
        
        Returns:
            Lista de dicionários com os registros encontrados
        
        Raises:
            mysql.connector.Error: Se houver erro na consulta
        """
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchall()
    
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Executa uma consulta SELECT e retorna um único resultado.
        
        Args:
            query: Consulta SQL SELECT
            params: Tupla com parâmetros para a consulta (opcional)
        
        Returns:
            Dicionário com o registro encontrado ou None se não encontrado
        
        Raises:
            mysql.connector.Error: Se houver erro na consulta
        """
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        
        return self.cursor.fetchone()
    
    def close(self):
        """
        Fecha a conexão com o banco de dados MySQL.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
