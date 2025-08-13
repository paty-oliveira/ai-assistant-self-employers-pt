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
    mock_llama_index.return_value = mock_index_instance
    mock_index_instance.pipeline.id = "index-id"

    service = LlmaCloudService("api-key")
    index_name = "test-index"
    documents = ["doc1", "doc2"]

    # Act
    service.index_documents(index_name, documents)

    # Assert
    mock_llama_index.assert_called_once_with(api_key="api-key", name=index_name, verbose=True)
    mock_index_instance.from_documents.assert_called_once_with(documents, name=index_name)
    assert mock_index_instance.pipeline.id == "index-id"


@patch("src.llama_cloud_service.LlamaCloudIndex")
def test_execute_query_calls_query_engine(mock_llama_index):
    # Arrange
    mock_index_instance = MagicMock()
    mock_llama_index.return_value = mock_index_instance
    mock_query_engine = MagicMock()
    mock_index_instance.as_query_engine.return_value = mock_query_engine
    mock_query_engine.query.return_value = "The capital of France is Paris."

    # Act
    service = LlmaCloudService("api-key")
    index_name = "test-index"
    query = "What is the capital of France?"
    result = service.execute_query(query, index_name)

    # Assert
    mock_llama_index.assert_called_once_with(api_key="api-key", name=index_name, verbose=True)
    mock_index_instance.as_query_engine.assert_called_once()
    mock_query_engine.query.assert_called_once_with(query)
    assert result == "The capital of France is Paris."
