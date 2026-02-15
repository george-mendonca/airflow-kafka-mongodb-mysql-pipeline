import mysql.connector
from mysql.connector import Error

class MySQLClient:
    def __init__(self, host='localhost', user='root', password='', database='default_db', port=3306):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            self.cursor = self.connection.cursor()
            print(f"✓ Conectado ao MySQL: {host}:{port}/{database}")
        except Error as e:
            print(f"✗ Erro ao conectar ao MySQL: {e}")
            raise

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = tuple(data.values())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            print(f"✗ Erro ao inserir: {e}")
            raise

    def insert_many(self, table_name, data_list):
        if not data_list:
            return 0
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(data_list[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            for data in data_list:
                values = tuple(data.values())
                self.cursor.execute(query, values)
            self.connection.commit()
            return len(data_list)
        except Error as e:
            self.connection.rollback()
            print(f"✗ Erro ao inserir múltiplos: {e}")
            raise

    def select(self, table_name, where=None):
        query = f"SELECT * FROM {table_name}"
        values = []
        if where:
            conditions = ' AND '.join([f"{k} = %s" for k in where.keys()])
            query += f" WHERE {conditions}"
            values = tuple(where.values())
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchall()
        except Error as e:
            print(f"✗ Erro ao buscar: {e}")
            raise

    def select_one(self, table_name, where):
        query = f"SELECT * FROM {table_name}"
        conditions = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query += f" WHERE {conditions}"
        values = tuple(where.values())
        try:
            self.cursor.execute(query, values)
            return self.cursor.fetchone()
        except Error as e:
            print(f"✗ Erro ao buscar: {e}")
            raise

    def update(self, table_name, data, where):
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        values = tuple(list(data.values()) + list(where.values()))
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            print(f"✗ Erro ao atualizar: {e}")
            raise

    def delete(self, table_name, where):
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        values = tuple(where.values())
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            print(f"✗ Erro ao deletar: {e}")
            raise

    def execute_query(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Error as e:
            self.connection.rollback()
            print(f"✗ Erro ao executar: {e}")
            raise

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("✓ Conexão com MySQL fechada")