import mysql.connector

class MySQLClient:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create(self, table, data):
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()

    def read(self, table, where=None):
        sql = f"SELECT * FROM {table}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def update(self, table, data, where):
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        self.cursor.execute(sql, tuple(data.values()))
        self.connection.commit()

    def delete(self, table, where):
        sql = f"DELETE FROM {table} WHERE {where}"
        self.cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()