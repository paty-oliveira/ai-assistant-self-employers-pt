from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document

class LlmaCloudService:

    def __init__(self, api_key: str, llm_model="openai-gpt-4-1-mini"):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key
        self.llm_model = llm_model

    def parse(self, files: list[str], result_type: str) -> list[Document]:
        """
        Parses the PDF file using LlamaParse service and returns the content.
        """

        llama_parser = LlamaParse(
            api_key=self.api_key,
            model=self.llm_model,
            result_type=result_type
        )

        file_extractor = {".pdf": llama_parser}

        documents = SimpleDirectoryReader(
            input_files=files,
            file_extractor=file_extractor
            ).load_data()

        return documents
