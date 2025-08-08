from abc import ABC, abstractmethod

from service import QueryEngineService


class BaseQueryEngine(ABC):
    """
    Abstract base class for searchers.
    """

    def __init__(self, query: str):
        """
        Initialize the searcher with a query and a search engine.

        :param query: The search query string.
        """
        self.query = query

    @abstractmethod
    def query(self) -> str:
        """
        Return the search query string.
        """
        pass


class QueryEngine(BaseQueryEngine):
    def __init__(self, query: str, searchEngine: QueryEngineService):
        super().__init__(query)
        self.searchEngine = searchEngine

    def query(self) -> str:
        """
        Return the resulting search query string.

        :return: The search query string.
        """

        results = self.searchEngine.execute_query(self.query)

        return results
