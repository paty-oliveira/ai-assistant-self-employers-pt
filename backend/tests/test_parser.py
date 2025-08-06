import pytest
from src.parser import PDFParser


def test_parse_calls_external_parser(mocker):
    # Arrange
    mock_parser_service = mocker.Mock()
    mock_parser_service.parse_pdf.return_value = "parsed content"

    parser = PDFParser(["dummy_path.pdf"], mock_parser_service, "text")

    # Act
    result = parser.parse()

    # Assert
    mock_parser_service.parse_pdf.assert_called_once_with(["dummy_path.pdf"], "text")
    assert result == "parsed content"
