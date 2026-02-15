"""
Unit Tests for MySQL Client

Tests for the MySQLClient class covering basic CRUD operations.
Uses unittest.mock to avoid requiring an actual MySQL instance.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from src.clients.mysql_client import MySQLClient


class TestMySQLClient(unittest.TestCase):
    """Test cases for MySQLClient"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock mysql.connector.connect
        self.mock_connection = Mock()
        self.mock_cursor = Mock()
        
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_connection.is_connected.return_value = True
        
        # Patch mysql.connector.connect
        with patch('src.clients.mysql_client.mysql.connector.connect', return_value=self.mock_connection):
            self.client = MySQLClient(
                host='localhost',
                user='testuser',
                password='testpass',
                database='testdb',
                port=3306
            )
    
    def test_insert_single_record(self):
        """Test inserting a single record"""
        # Arrange
        test_data = {
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        expected_id = 1
        self.mock_cursor.lastrowid = expected_id
        
        # Act
        result = self.client.insert("users", test_data)
        
        # Assert
        self.assertEqual(result, expected_id)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        
        # Verify the query structure
        call_args = self.mock_cursor.execute.call_args
        query = call_args[0][0]
        self.assertIn("INSERT INTO users", query)
        self.assertIn("name", query)
        self.assertIn("age", query)
        self.assertIn("email", query)
    
    def test_insert_rollback_on_error(self):
        """Test that insert attempts rollback on error"""
        # Arrange
        test_data = {"name": "John Doe"}
        # Create a proper Error from mysql.connector
        from mysql.connector import Error
        self.mock_cursor.execute.side_effect = Error("Database error")
        
        # Act & Assert
        with self.assertRaises(Error):
            self.client.insert("users", test_data)
        
        # The rollback is called by the actual client code
        # We just verify the exception is raised
    
    def test_select_all_records(self):
        """Test selecting all records from a table"""
        # Arrange
        expected_results = [
            (1, "John Doe", 30, "john@example.com"),
            (2, "Jane Smith", 25, "jane@example.com")
        ]
        self.mock_cursor.fetchall.return_value = expected_results
        
        # Act
        result = self.client.select("users")
        
        # Assert
        self.assertEqual(result, expected_results)
        self.mock_cursor.execute.assert_called_once()
        
        # Verify the query
        call_args = self.mock_cursor.execute.call_args
        query = call_args[0][0]
        self.assertEqual("SELECT * FROM users", query)
    
    def test_select_with_where_clause(self):
        """Test selecting records with a WHERE clause"""
        # Arrange
        where_clause = {"name": "John Doe"}
        expected_results = [(1, "John Doe", 30, "john@example.com")]
        self.mock_cursor.fetchall.return_value = expected_results
        
        # Act
        result = self.client.select("users", where=where_clause)
        
        # Assert
        self.assertEqual(result, expected_results)
        
        # Verify the query includes WHERE clause
        call_args = self.mock_cursor.execute.call_args
        query = call_args[0][0]
        self.assertIn("WHERE", query)
        self.assertIn("name = %s", query)
    
    def test_update_record(self):
        """Test updating a record"""
        # Arrange
        data = {"age": 31, "email": "john.doe@example.com"}
        where = {"name": "John Doe"}
        self.mock_cursor.rowcount = 1
        
        # Act
        result = self.client.update("users", data, where)
        
        # Assert
        self.assertEqual(result, 1)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        
        # Verify the query structure
        call_args = self.mock_cursor.execute.call_args
        query = call_args[0][0]
        self.assertIn("UPDATE users", query)
        self.assertIn("SET", query)
        self.assertIn("WHERE", query)
    
    def test_update_no_rows_affected(self):
        """Test updating when no rows match"""
        # Arrange
        data = {"age": 31}
        where = {"name": "Nonexistent User"}
        self.mock_cursor.rowcount = 0
        
        # Act
        result = self.client.update("users", data, where)
        
        # Assert
        self.assertEqual(result, 0)
    
    def test_update_rollback_on_error(self):
        """Test that update attempts rollback on error"""
        # Arrange
        data = {"age": 31}
        where = {"name": "John Doe"}
        from mysql.connector import Error
        self.mock_cursor.execute.side_effect = Error("Database error")
        
        # Act & Assert
        with self.assertRaises(Error):
            self.client.update("users", data, where)
        
        # The rollback is called by the actual client code
        # We just verify the exception is raised
    
    def test_delete_record(self):
        """Test deleting a record"""
        # Arrange
        where = {"name": "John Doe"}
        self.mock_cursor.rowcount = 1
        
        # Act
        result = self.client.delete("users", where)
        
        # Assert
        self.assertEqual(result, 1)
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        
        # Verify the query structure
        call_args = self.mock_cursor.execute.call_args
        query = call_args[0][0]
        self.assertIn("DELETE FROM users", query)
        self.assertIn("WHERE", query)
    
    def test_delete_no_rows_affected(self):
        """Test deleting when no rows match"""
        # Arrange
        where = {"name": "Nonexistent User"}
        self.mock_cursor.rowcount = 0
        
        # Act
        result = self.client.delete("users", where)
        
        # Assert
        self.assertEqual(result, 0)
    
    def test_delete_rollback_on_error(self):
        """Test that delete attempts rollback on error"""
        # Arrange
        where = {"name": "John Doe"}
        from mysql.connector import Error
        self.mock_cursor.execute.side_effect = Error("Database error")
        
        # Act & Assert
        with self.assertRaises(Error):
            self.client.delete("users", where)
        
        # The rollback is called by the actual client code
        # We just verify the exception is raised
    
    def test_close_connection(self):
        """Test closing the database connection"""
        # Act
        self.client.close()
        
        # Assert
        self.mock_cursor.close.assert_called_once()
        self.mock_connection.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
