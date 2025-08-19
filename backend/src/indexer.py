from abc import ABC, abstractmethod

from .service import IndexService


class BaseIndexer(ABC):
    def __init__(self, index_name: str):
        """
        Initializes the base indexer with the given index name.
        """
        self.index_name = index_name

    @abstractmethod
    def index(self, documents):
        """
        Abstract method to index documents.
        Should be implemented by subclasses.
        """
        pass


class Indexer(BaseIndexer):
    def __init__(self, index_name: str, index_service: IndexService):
        super().__init__(index_name)
        self.index_service = index_service

    def index(self, documents):
        """
        Indexes the provided documents using the specified index service.
        """

        self.index_service.index_documents(self.index_name, documents)
