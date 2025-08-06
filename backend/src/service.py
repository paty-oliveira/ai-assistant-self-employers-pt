from abc import ABC, abstractmethod


class IndexService(ABC):
    @abstractmethod
    def index_documents(self, index_name: str, documents: list):
        """
        Abstract method to index documents in a specific service.
        Should be implemented by subclasses.
        """
        pass


class PDFParserService(ABC):
    @abstractmethod
    def parse_pdf(self, file_paths: list[str], result_type: str):
        """
        Abstract method to parse files and return their content.
        Should be implemented by subclasses.
        """
        pass
