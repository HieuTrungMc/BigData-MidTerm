import pymongo

class MongoDBHandler:
    def __init__(self, uri, db_name, collection_name):
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_data(self, data):
        self.collection.insert_one(data)