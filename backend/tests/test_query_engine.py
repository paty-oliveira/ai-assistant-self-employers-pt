import pytest

from src.query_engine import QueryEngine


def test_query_engine_external_service_call(mocker):
    # Arrange
    mock_service = mocker.Mock()
    mock_service.execute_query.return_value = "query result"

    query = "Example of query"
    query_engine = QueryEngine(query, mock_service)

    # Act
    result = query_engine.query()

    # Assert
    mock_service.execute_query.assert_called_once_with(query)
    assert result == "query result"
