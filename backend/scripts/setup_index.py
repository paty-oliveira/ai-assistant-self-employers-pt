# setup_index.py workflow:
# 1. Check if .indexing_state.json exists
# 2. Compare PDF hashes with previous state
# 3. Only process changed/new PDFs
# 4. Update state file
# 5. Exit with success/failure code

import json
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
        initial_state = {
            "version": "1.0",
            "last_updated": None,
            "metadata": {
                "total_files": 0,
                "index_location": "Llama Cloud",
                "processing_stats": {"total_processed": 0, "successful": 0, "failed": 0, "last_run_duration": None},
            },
            "files": {},
        }
        with open(indexing_state_file, "w") as f:
            json.dump(initial_state, f, indent=4)

    # Check the current state of indexing


main()
