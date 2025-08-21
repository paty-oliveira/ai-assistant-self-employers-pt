import logging
from typing import Dict

from llama_cloud_services import LlamaCloudIndex, LlamaParse
from llama_cloud_services.parse.types import Document

from .service import IndexService, PDFParserService, QueryEngineService


class LlamaCloudService(IndexService, PDFParserService, QueryEngineService):
    def __init__(self, api_key: str, llm_model="openai-gpt-4-1-mini"):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key
        self.llm_model = llm_model
        self._indexes: Dict[str, LlamaCloudIndex] = {}
        self._logger = logging.getLogger(__name__)

    def _get_or_create_index(self, index_name: str) -> LlamaCloudIndex:
        """
        Gets an existing index or creates a new one with the given name.
        """
        if not index_name:
            raise ValueError("Index name cannot be empty")

        if index_name in self._indexes and self._indexes[index_name] is not None:
            self._logger.info(f"Using existing index: {index_name}")
            return self._indexes[index_name]

        try:
            self._logger.info(f"Creating new index: {index_name}")
            index = LlamaCloudIndex.create_index(api_key=self.api_key, name=index_name, verbose=True)
            self._indexes[index_name] = index
            return index
        except Exception as e:
            self._logger.error(f"Failed to create index {index_name}: {e}")

    def parse_pdf(self, files: list[str], result_type: str) -> list[dict]:
        """
        Parses the PDF file using LlamaParse service and returns the content.
        """
        if not files:
            raise ValueError("Files list cannot be empty")

        try:
            llama_parser = LlamaParse(api_key=self.api_key, model=self.llm_model, result_type=result_type)

            self._logger.info(f"Parsing {len(files)} files")
            results = llama_parser.parse(files)

            content = []
            for document in results:
                self._logger.info(f"Getting text content from Job ID: {document.job_id}")
                text_documents = document.get_text_documents(split_by_page=True)

                content.append(
                    {"job_id": document.job_id, "file_name": document.file_name, "file_content": text_documents}
                )

                self._logger.info(f"Parsed {len(text_documents)} documents from {document.file_name}")

            return content
        except Exception as e:
            self._logger.error(f"Error parsing PDF files: {e}")

    def index_documents(self, index_name: str, documents: list[Document]) -> None:
        """
        Indexes the documents in the default vector database provided by
        IlamaCloud.
        """
        if not documents:
            raise ValueError("Documents list cannot be empty")

        try:
            index = self._get_or_create_index(index_name)
            index.from_documents(documents, name=index_name)

            self._logger.info(
                f"Successfully loaded {len(documents)} documents to index '{index_name}' "
                f"with pipeline ID: {index.pipeline.id}"
            )

        except Exception as e:
            self._logger.error(f"Error loading documents to index '{index_name}': {e}")

    def execute_query(self, query: str, index_name: str) -> str:
        """
        Executes a query against the specified index.
        """
        if not query.strip():
            return "Query cannot be empty"

        try:
            index = self._get_or_create_index(index_name)
            query_engine = index.as_query_engine()

            self._logger.info(f"Executing query on index '{index_name}': {query[:50]}...")
            response = query_engine.query(query)

            return str(response) if response else "No response from query engine."

        except Exception as e:
            error_msg = f"Error executing query on index '{index_name}': {e}"
            self._logger.error(error_msg)
            return error_msg
