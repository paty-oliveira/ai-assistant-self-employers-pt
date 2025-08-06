from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.schema import Document
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from service import IndexService, PDFParserService

class LlmaCloudService(IndexService, PDFParserService):

    def __init__(self, api_key: str, llm_model="openai-gpt-4-1-mini"):
        """
        Initializes the LlamaParse service with the provided API key.
        """
        self.api_key = api_key
        self.llm_model = llm_model

    def parse_pdf(self, files: list[str], result_type: str) -> list[Document]:
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

        print(f"Parsed {len(documents)} documents from {files}")

        return documents

    def index_documents(self, index_name, documents: list[Document]) -> None:
        """
        Indexes the documents in the default vector database provided by
        IlamaCloud.
        """

        try:
            print(f"Creating index {index_name} with {len(documents)} documents...")
            index = LlamaCloudIndex.from_documents(
                api_key=self.api_key,
                documents=documents,
                name=index_name,
                verbose=True
            )

            print(f"Index {index_name} with id {index.pipeline.id} created successfully.")
        except Exception as e:
            print(f"Error creating index {index_name}: {e}")
