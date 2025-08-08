from unittest.mock import Mock

import pytest

from src.query_engine import QueryEngine


def test_query_engine_returns_results():
    mock_search_engine = Mock()
    mock_search_engine.execute_query.return_value = "mocked results"
    query = "test query"
    engine = QueryEngine(query, mock_search_engine)

    result = engine.query()

    mock_search_engine.execute_query.assert_called_once_with(query)
    assert result == "mocked results"


def test_query_engine_with_empty_query():
    mock_search_engine = Mock()
    mock_search_engine.execute_query.return_value = ""
    query = ""
    engine = QueryEngine(query, mock_search_engine)

    result = engine.query()

    mock_search_engine.execute_query.assert_called_once_with(query)
    assert result == ""


def test_query_engine_with_none_result():
    mock_search_engine = Mock()
    mock_search_engine.execute_query.return_value = None
    query = "something"
    engine = QueryEngine(query, mock_search_engine)

    result = engine.query()

    mock_search_engine.execute_query.assert_called_once_with(query)
    assert result is None
