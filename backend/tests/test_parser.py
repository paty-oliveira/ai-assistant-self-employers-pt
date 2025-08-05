import pytest
from src.parser import PDFParser

def test_parse_calls_external_parser(mocker):
    # Arrange
    mock_parser_service = mocker.Mock()
    mock_parser_service.parse.return_value = "parsed content"

    parser = PDFParser("dummy_path.pdf", mock_parser_service)

    # Act
    result = parser.parse()

    # Assert
    mock_parser_service.parse.assert_called_once_with("dummy_path.pdf")
    assert result == "parsed content"
