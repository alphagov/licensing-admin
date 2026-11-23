from pymongo import MongoClient


class BaseFactory:
    collection_name: str
    model = None  # the class to instantiate

    def __init__(self, db_url: str):
        self._client = MongoClient(db_url)
        self._collection = self._client.get_default_database()[self.collection_name]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self._client.close()

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self._collection.insert_one(obj.to_json())
        return obj

    def create_x(self, x: int, **kwargs):
        return [self.create(**kwargs) for _ in range(x)]
