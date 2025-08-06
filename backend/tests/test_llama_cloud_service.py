import pytest
from unittest.mock import patch, MagicMock
from src.llama_cloud_service import LlmaCloudService

def test_init_sets_api_key_and_model():
    service = LlmaCloudService("test-key", llm_model="test-model")
    assert service.api_key == "test-key"
    assert service.llm_model == "test-model"

@patch("src.llama_cloud_service.LlamaParse")
@patch("src.llama_cloud_service.SimpleDirectoryReader")
def test_parse_calls_llama_parse_and_simple_directory_reader(mock_reader, mock_llama_parse):
    # Arrange
    mock_llama_instance = MagicMock()
    mock_llama_parse.return_value = mock_llama_instance
    mock_reader_instance = MagicMock()
    mock_reader.return_value = mock_reader_instance
    mock_reader_instance.load_data.return_value = ["doc1", "doc2"]

    service = LlmaCloudService("api-key", llm_model="llama-model")
    files = ["file1.pdf"]
    result_type = "text"

    # Act
    result = service.parse(files, result_type)

    # Assert
    mock_llama_parse.assert_called_once_with(
        api_key="api-key",
        model="llama-model",
        result_type=result_type
    )
    mock_reader.assert_called_once_with(
        input_files=files,
        file_extractor={".pdf": mock_llama_instance}
    )
    mock_reader_instance.load_data.assert_called_once()
    assert result == ["doc1", "doc2"]

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
        api_key="api-key",
        documents=documents,
        name=index_name,
        verbose=True
    )

    assert mock_index_instance.pipeline.id == "index-id"
