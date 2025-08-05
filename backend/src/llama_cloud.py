class LlmaCloudService:

    def __init__(self, api_key):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key

    def parse(self, file_path):
        """
        Parses the PDF file using LlamaParse service and returns the content.
        """
        raise NotImplementedError("Subclasses should implement this method.")
