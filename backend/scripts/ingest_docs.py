import datetime
import hashlib
import json
import logging
import os

from dotenv import load_dotenv

from src.llama_cloud_service import LlamaCloudService
from src.rag import parsing_and_indexing_documents

load_dotenv(override=True)

LLAMA_CLOUD_API = os.environ.get("LLAMA_CLOUD_API_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None


def create_indexing_state_file(state_file: str):
    initial_state = {
        "version": "1.0",
        "last_updated": None,
        "metadata": {
            "total_files": 0,
            "index_location": "Llama Cloud",
            "processing_stats": {"total_processed": 0, "successful": 0, "failed": 0},
        },
        "index_name": None,
        "files": {},
    }
    with open(state_file, "w") as f:
        json.dump(initial_state, f, indent=4)


def get_indexing_state(current_state: dict, folder_path: str):
    files_preprocessed = current_state.get("files", {})
    if not files_preprocessed:
        logger.info("No files preprocessed. Initializing indexing state...")
        pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]
        current_state["files"] = {}

        for pdf_file in pdf_files:
            file_path = os.path.join(folder_path, pdf_file)
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            file_hash = calculate_file_hash(file_path)
            if file_hash:
                file_size = os.path.getsize(file_path)
                current_state["files"][file_name] = {
                    "hash": file_hash,
                    "size": file_size,
                    "last_indexed": None,
                    "status": "pending",
                    "metadata": {
                        "title": file_name,
                        "author": None,
                        "creation_date": None,
                    },
                }
    else:
        for file_name, file_info in files_preprocessed.items():
            file_path = os.path.join("pdfs", f"{file_name}.pdf")
            current_hash = calculate_file_hash(file_path)
            if current_hash != file_info["hash"]:
                logger.info(f"File {file_name} has changed. Re-indexing...")
                file_info["hash"] = current_hash
                file_info["last_indexed"] = datetime.datetime.now().isoformat()
                file_info["status"] = "pending"
            else:
                logger.info(f"File {file_name} has not changed. Skipping...")

    return current_state


def update_indexing_state(current_state: dict, external_service, index_name):
    files = current_state.get("files", {})
    for file_name, file_info in files.items():
        if file_info["status"] == "pending":
            file_path = os.path.join("pdfs", f"{file_name}.pdf")
            try:
                parsing_and_indexing_documents(
                    pdf_files=[file_path],
                    index_name=index_name,
                    external_service=external_service,
                )
                file_info["status"] = "indexed"
                file_info["last_indexed"] = datetime.datetime.now().isoformat()
                current_state["index_name"] = index_name
                current_state["metadata"]["total_files"] += 1
                current_state["metadata"]["processing_stats"]["total_processed"] += 1
                current_state["metadata"]["processing_stats"]["successful"] += 1
            except Exception as e:
                logger.error(f"Failed to index {file_name}: {e}")
                file_info["status"] = "failed"
                current_state["metadata"]["processing_stats"]["failed"] += 1
            finally:
                current_state["last_updated"] = datetime.datetime.now().isoformat()

    return current_state


def main():
    """Main function to set up indexing for PDF files."""
    if not LLAMA_CLOUD_API:
        logger.error(
            "Llama Cloud API key is not set. Please set the LLAMA_CLOUD_API_KEY environment variable."
        )

    external_service = LlamaCloudService(LLAMA_CLOUD_API)
    indexing_state_file = os.path.abspath("indexing_state.json")

    if not os.path.exists(indexing_state_file):
        create_indexing_state_file(indexing_state_file)

    with open(indexing_state_file, "r") as f:
        index_content = json.load(f)

    current_state = get_indexing_state(index_content, "pdfs")

    updated_state = update_indexing_state(
        current_state, external_service, index_name="rag_index_test"
    )

    with open(indexing_state_file, "w") as f:
        json.dump(updated_state, f, indent=4)


if __name__ == "__main__":
    main()
