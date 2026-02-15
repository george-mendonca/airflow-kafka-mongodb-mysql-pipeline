import pymongo

class MongoDBClient:
    def __init__(self, uri, db_name):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def insert_many(self, collection_name, documents):
        collection = self.db[collection_name]
        return collection.insert_many(documents)

    def find(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find(query)

    def find_one(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.find_one(query)

    def update(self, collection_name, query, update_values):
        collection = self.db[collection_name]
        return collection.update_one(query, {'$set': update_values})

    def delete(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_one(query)

    def close(self):
        self.client.close()