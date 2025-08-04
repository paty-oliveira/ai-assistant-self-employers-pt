from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def parse(self):
        """
        Parses the file and returns the content.
        This method should be implemented by subclasses.
        """
        pass


class PDFParser(BaseParser):
    def __init__(self, file_path, file_parser):
        super().__init__(file_path)
        self.file_parser = file_parser

    def parse(self):
        """
        Parses the PDF file and returns the content.
        """
        content = self.file_parser.parse(self.file_path)

        return content
