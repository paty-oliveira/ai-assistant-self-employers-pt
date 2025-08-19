from abc import ABC, abstractmethod

from .service import QueryEngineService


class BaseQueryEngine(ABC):
    """
    Abstract base class for searchers.
    """

    def __init__(self, query_text: str):
        """
        Initialize the searcher with a query and a search engine.

        :param query: The search query string.
        """
        self.query_text = query_text

    @abstractmethod
    def query(self) -> str:
        """
        Return the search query string.
        """
        pass


class QueryEngine(BaseQueryEngine):
    def __init__(self, query_text: str, search_engine: QueryEngineService, index_name: str):
        super().__init__(query_text)
        self.search_engine = search_engine
        self.index_name = index_name

    def query(self) -> str:
        """
        Return the resulting search query string.

        :return: The search query string.
        """

        results = self.search_engine.execute_query(self.query_text, self.index_name)

        return results
