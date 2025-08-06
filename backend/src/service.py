from abc import ABC, abstractmethod

class IndexService(ABC):
    @abstractmethod
    def index_documents(self, index_name: str, documents: list):
        """
        Abstract method to index documents in a specific service.
        Should be implemented by subclasses.
        """
        pass
