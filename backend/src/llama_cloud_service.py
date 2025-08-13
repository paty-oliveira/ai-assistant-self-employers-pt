from llama_cloud_services import LlamaCloudIndex, LlamaParse
from llama_cloud_services.parse.types import Document

from service import IndexService, PDFParserService, QueryEngineService


class LlmaCloudService(IndexService, PDFParserService, QueryEngineService):
    def __init__(self, api_key: str, llm_model="openai-gpt-4-1-mini"):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key
        self.llm_model = llm_model
        self._indexes = {}

    def _get_or_create_index(self, index_name: str) -> LlamaCloudIndex:
        """
        Creates an index with the given name.
        """

        if index_name in self._indexes:
            return self._indexes[index_name]

        index = LlamaCloudIndex(api_key=self.api_key, name=index_name, verbose=True)
        self._indexes[index_name] = index

        return index

    def parse_pdf(self, files: list[str], result_type: str) -> list[dict]:
        """
        Parses the PDF file using LlamaParse service and returns the content.
        """

        llama_parser = LlamaParse(api_key=self.api_key, model=self.llm_model, result_type=result_type)

        results = llama_parser.parse(files)

        content = []

        for document in results:
            print(f"Getting text content from Job ID: {document.job_id}")
            text_document = document.get_text_documents(split_by_page=True)
            content.append({"job_id": document.job_id, "file_name": document.file_name, "file_content": text_document})
            print(f"Parsed {len(text_document)} documents from {document.file_name}")

        return content

    def index_documents(self, index_name: str, documents: list[Document]) -> None:
        """
        Indexes the documents in the default vector database provided by
        IlamaCloud.
        """

        try:
            index = self._get_or_create_index(index_name)
            index.from_documents(documents, name=index_name)

            print(f"Documents loaded on {index_name} with id {self.index.pipeline.id} successfully.")
        except Exception as e:
            print(f"Error loading documents on index {index_name}: {e}")

    def execute_query(self, query: str, index_name: str) -> str:
        """
        Executes a query against the specified index.
        """
        try:
            index = self._get_or_create_index(index_name)
            query_engine = index.as_query_engine()
            response = query_engine.query(query)
            return str(response) if response else "No response from query engine."

        except Exception as e:
            print(f"Error executing query on index {index_name}: {e}")
            return f"Index {index_name} not found or error occurred: {e}"
