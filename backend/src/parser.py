from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, file_paths: list[str]):
        self.file_paths = file_paths

    @abstractmethod
    def parse(self):
        """
        Parses the file and returns the content.
        This method should be implemented by subclasses.
        """
        pass


class PDFParser(BaseParser):
    def __init__(self, file_paths: list[str], parser_service, result_type: str):
        super().__init__(file_paths)
        self.parser_service = parser_service
        self.result_type = result_type

    def parse(self):
        """
        Parses the PDF file and returns the content in plain text.
        """
        content = self.parser_service.parse(self.file_paths, self.result_type)

        return content
