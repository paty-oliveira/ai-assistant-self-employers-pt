import os

from dotenv import load_dotenv

from llama_cloud_service import LlmaCloudService
from rag import parsing_and_indexing_documents, query_documents

LLAMA_CLOUD_API = os.getenv("LLAMA_CLOUD_API_KEY")


def main():
    pdf_files = [
        os.path.abspath("pdfs/novo_regime.pdf"),
        os.path.abspath("pdfs/perguntas_frequentes.pdf"),
    ]

    llama_service = LlmaCloudService(api_key=LLAMA_CLOUD_API)
    index_name = "self_employed_documents"
    parsing_and_indexing_documents(pdf_files, index_name, llama_service)

    query = "What is the new regime for self-employed workers?"
    response = query_documents(query, index_name, llama_service)
    print(f"Query: {query}")
    print(f"Response: {response}")


if __name__ == "__main__":
    load_dotenv()
    main()
