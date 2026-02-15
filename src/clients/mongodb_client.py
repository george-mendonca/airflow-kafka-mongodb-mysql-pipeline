# MongoDB CRUD Implementation

from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client.get_database()

    def create(self, collection_name, data):
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id

    def read(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.find_one(query)
        return result

    def update(self, collection_name, query, update_data):
        collection = self.db[collection_name]
        result = collection.update_one(query, {'$set': update_data})
        return result.modified_count

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
