# setup_index.py workflow:
# 1. Check if .indexing_state.json exists
# 2. Compare PDF hashes with previous state
# 3. Only process changed/new PDFs
# 4. Update state file
# 5. Exit with success/failure code

import os

from dotenv import load_dotenv

from src.llama_cloud_service import LlmaCloudService
from src.rag import parsing_and_indexing_documents

LLAMA_CLOUD_API = os.getenv("LLAMA_CLOUD_API_KEY")


def main():
    load_dotenv()
    pdf_files = [
        os.path.abspath("pdfs/novo_regime.pdf"),
        os.path.abspath("pdfs/perguntas_frequentes.pdf"),
    ]

    indexing_state_file = os.path.abspath("indexing_state.json")

    if not os.path.exists(indexing_state_file):
        print("Indexing state file does not exist. Creating a new one.")
        with open(indexing_state_file, "w") as f:
            f.write("{}")

    # Check the current state of indexing


main()
