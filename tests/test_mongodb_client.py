"""
Unit Tests for MongoDB Client

Tests for the MongoDBClient class covering basic CRUD operations.
Uses unittest.mock to avoid requiring an actual MongoDB instance.
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from src.clients.mongodb_client import MongoDBClient


class TestMongoDBClient(unittest.TestCase):
    """Test cases for MongoDBClient"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the MongoClient to avoid actual database connections
        self.mock_mongo_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()
        
        # Setup mock chain
        self.mock_mongo_client.get_database.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_collection
        
        # Patch MongoClient in the mongodb_client module
        with patch('src.clients.mongodb_client.MongoClient', return_value=self.mock_mongo_client):
            self.client = MongoDBClient("mongodb://localhost:27017/testdb")
    
    def test_insert_document(self):
        """Test inserting a document into MongoDB"""
        # Arrange
        test_data = {"name": "John Doe", "age": 30, "email": "john@example.com"}
        expected_id = "507f1f77bcf86cd799439011"
        
        mock_result = Mock()
        mock_result.inserted_id = expected_id
        self.mock_collection.insert_one.return_value = mock_result
        
        # Act
        result = self.client.create("users", test_data)
        
        # Assert
        self.assertEqual(result, expected_id)
        self.mock_collection.insert_one.assert_called_once_with(test_data)
    
    def test_find_one_document(self):
        """Test finding a single document in MongoDB"""
        # Arrange
        query = {"name": "John Doe"}
        expected_document = {
            "_id": "507f1f77bcf86cd799439011",
            "name": "John Doe",
            "age": 30,
            "email": "john@example.com"
        }
        self.mock_collection.find_one.return_value = expected_document
        
        # Act
        result = self.client.read("users", query)
        
        # Assert
        self.assertEqual(result, expected_document)
        self.mock_collection.find_one.assert_called_once_with(query)
    
    def test_find_one_not_found(self):
        """Test finding a document that doesn't exist"""
        # Arrange
        query = {"name": "Nonexistent User"}
        self.mock_collection.find_one.return_value = None
        
        # Act
        result = self.client.read("users", query)
        
        # Assert
        self.assertIsNone(result)
        self.mock_collection.find_one.assert_called_once_with(query)
    
    def test_update_one_document(self):
        """Test updating a document in MongoDB"""
        # Arrange
        query = {"name": "John Doe"}
        update_data = {"age": 31, "email": "john.doe@example.com"}
        
        mock_result = Mock()
        mock_result.modified_count = 1
        self.mock_collection.update_one.return_value = mock_result
        
        # Act
        result = self.client.update("users", query, update_data)
        
        # Assert
        self.assertEqual(result, 1)
        self.mock_collection.update_one.assert_called_once_with(query, {'$set': update_data})
    
    def test_update_no_documents_modified(self):
        """Test updating when no documents match the query"""
        # Arrange
        query = {"name": "Nonexistent User"}
        update_data = {"age": 31}
        
        mock_result = Mock()
        mock_result.modified_count = 0
        self.mock_collection.update_one.return_value = mock_result
        
        # Act
        result = self.client.update("users", query, update_data)
        
        # Assert
        self.assertEqual(result, 0)
    
    def test_delete_one_document(self):
        """Test deleting a document from MongoDB"""
        # Arrange
        query = {"name": "John Doe"}
        
        mock_result = Mock()
        mock_result.deleted_count = 1
        self.mock_collection.delete_one.return_value = mock_result
        
        # Act
        result = self.client.delete("users", query)
        
        # Assert
        self.assertEqual(result, 1)
        self.mock_collection.delete_one.assert_called_once_with(query)
    
    def test_delete_no_documents_found(self):
        """Test deleting when no documents match the query"""
        # Arrange
        query = {"name": "Nonexistent User"}
        
        mock_result = Mock()
        mock_result.deleted_count = 0
        self.mock_collection.delete_one.return_value = mock_result
        
        # Act
        result = self.client.delete("users", query)
        
        # Assert
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
