from llama_cloud_services import LlamaCloudIndex, LlamaParse
from llama_cloud_services.parse.types import Document

from service import IndexService, PDFParserService


class LlmaCloudService(IndexService, PDFParserService):

    def __init__(self, api_key: str, llm_model="openai-gpt-4-1-mini"):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key
        self.llm_model = llm_model

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

    def index_documents(self, index_name, documents: list[Document]) -> None:
        """
        Indexes the documents in the default vector database provided by
        IlamaCloud.
        """

        try:
            print(f"Creating index {index_name} with {len(documents)} documents...")
            index = LlamaCloudIndex.from_documents(
                api_key=self.api_key, documents=documents, name=index_name, verbose=True
            )

            print(f"Index {index_name} with id {index.pipeline.id} created successfully.")
        except Exception as e:
            print(f"Error creating index {index_name}: {e}")
