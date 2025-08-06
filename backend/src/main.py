import os
from parser import PDFParser

from dotenv import load_dotenv

from indexer import Indexer
from llama_cloud_service import LlmaCloudService

if __name__ == "__main__":
    load_dotenv()
    LLAMA_CLOUD_API = os.getenv("LLAMA_CLOUD_API_KEY")

    if not LLAMA_CLOUD_API:
        raise ValueError("LLAMA_API_KEY environment variable is not set.")

    llama_service = LlmaCloudService(api_key=LLAMA_CLOUD_API)

    pdf_files = [
        os.path.abspath("pdfs/novo_regime.pdf"),
        os.path.abspath("pdfs/perguntas_frequentes.pdf"),
    ]

    pdf_parser = PDFParser(file_paths=pdf_files, parser_service=llama_service, result_type="text")
    documents = pdf_parser.parse()

    index_name = "example_index"
    index_service = Indexer(index_name=index_name, index_service=llama_service)

    index_service.index(documents)
