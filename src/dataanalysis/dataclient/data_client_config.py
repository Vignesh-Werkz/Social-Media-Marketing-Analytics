"""Module for DataClientConfig"""


class DataClientConfig:
    """
    This class serves as a Config object to define the details needed for a database client.
    """
    def __init__(self, db_type: str, uri: str, db_name: str, collection: str):
        self.db_type = db_type
        self.uri = uri
        self.db_name = db_name
        self.collection = collection
