from pymongo import MongoClient


class MongoDbClient:
    __DATABASE_NAME = 'leak_detection'

    def __init__(self):
        self.__client = MongoClient('localhost', 27017)

    def insert(self, collection_name: str, documents: list[dict[str, object]]):
        database = self.__client.get_database(MongoDbClient.__DATABASE_NAME)
        collection = database.get_collection(collection_name)
        collection.insert_many(documents)
