from unittest.mock import MagicMock, patch

import pytest

from src.llama_cloud_service import LlmaCloudService


def test_init_sets_api_key_and_model():
    service = LlmaCloudService("test-key", llm_model="test-model")
    assert service.api_key == "test-key"
    assert service.llm_model == "test-model"


@patch("src.llama_cloud_service.LlamaParse")
def test_parse_calls_llama_parse_and_simple_directory_reader(mock_llama_parse):
    # Arrange
    mock_document = MagicMock()
    mock_document.job_id = "job123"
    mock_document.file_name = "file1.pdf"
    mock_document.get_text_documents.return_value = ["page1 text", "page2 text"]

    mock_llama_instance = MagicMock()
    mock_llama_instance.parse.return_value = [mock_document]
    mock_llama_parse.return_value = mock_llama_instance

    service = LlmaCloudService("api-key", llm_model="llama-model")
    files = ["file1.pdf"]
    result_type = "text"

    # Act
    result = service.parse_pdf(files, result_type)

    # Assert
    mock_llama_parse.assert_called_once_with(api_key="api-key", model="llama-model", result_type=result_type)
    mock_llama_instance.parse.assert_called_once_with(files)
    assert result == [{"job_id": "job123", "file_name": "file1.pdf", "file_content": ["page1 text", "page2 text"]}]


@patch("src.llama_cloud_service.LlamaCloudIndex")
def test_index_documents_creates_index_successfully(mock_llama_index):
    # Arrange
    mock_index_instance = MagicMock()
    mock_llama_index.from_documents.return_value = mock_index_instance
    mock_index_instance.pipeline.id = "index-id"

    service = LlmaCloudService("api-key")
    documents = ["doc1", "doc2"]
    index_name = "test-index"

    # Act
    service.index_documents(index_name, documents)

    # Assert
    mock_llama_index.from_documents.assert_called_once_with(
        api_key="api-key", documents=documents, name=index_name, verbose=True
    )

    assert mock_index_instance.pipeline.id == "index-id"
