from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class MongoDBController:
    """
    Controller for managing MongoDB database connections and operations.
    """

    def __init__(self, mongo_uri: str, db_name: str):
        """
        Initializes the MongoDBController with a database connection.

        Args:
           mongo_uri (str): The MongoDB connection URI (e.g., "mongodb://user:pass@host:port/").
           db_name (str): The name of the database to use.
        """
        if not mongo_uri or not db_name:
            raise ValueError("MongoDB URI and database name cannot be empty.")

        self._client: MongoClient = MongoClient(mongo_uri)
        self._db = self._client[db_name]
        print(f"Connected to MongoDB database '{db_name}' at '{mongo_uri}'.")

    def get_database(self) -> Database:
        """
        Returns the PyMongo Database handle.
        This is the equivalent of a session/connection in the SQL world,
        allowing interaction with all collections.
        """
        return self._db

    def get_collection(self, collection_name: str) -> Collection:
        """
        A convenience method to get a specific collection handle from the database.

        Args:
                collection_name (str): The name of the collection to access.

        Returns:
                Collection: A PyMongo Collection object.
        """
        if not collection_name:
            raise ValueError("Collection name cannot be empty.")
        return self._db[collection_name]

    def create_indexes(self, indexes: list[dict[str, list]]) -> None:
        """
        Creates indexes on specified collections.

        Args:
                indexes (list): A list of dictionaries, each containing:
                        - collection_name (str): The name of the collection.
                        - indexes (list): A list of index specifications.
        """
        for item in indexes:
            if "collection_name" not in item or "indexes" not in item:
                raise ValueError(
                    "Each item must contain 'collection_name' and 'indexes'."
                )
            collection = self.get_collection(item["collection_name"])
            for index in item["indexes"]:
                collection.create_index(index)
            print(f"Indexes created for collection '{item['collection_name']}'.")

    def close_connection(self) -> None:
        """
        Closes the connection to the MongoDB server.
        This should be called when the application is shutting down.
        """
        if self._client:
            self._client.close()
            print("MongoDB connection closed.")
