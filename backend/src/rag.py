from .indexer import Indexer
from .parser import PDFParser
from .query_engine import QueryEngine


def parsing_and_indexing_documents(pdf_files, index_name, external_service):
    """
    Parses PDF documents and indexes their content using the provided external service.
    Args:
        pdf_files (list): List of paths to PDF files to be parsed.
        index_name (str): Name of the index where the parsed content will be stored.
        external_service: An instance of the external service used for parsing and indexing.
    """

    pdf_parser = PDFParser(file_paths=pdf_files, parser_service=external_service, result_type="text")
    documents_payload = pdf_parser.parse()

    index_service = Indexer(index_name=index_name, index_service=external_service)

    try:
        for document in documents_payload:
            index_service.index(document["file_content"])
            print(f"Indexed document: {document['file_name']} in index: {index_name}")
    except Exception as e:
        print(f"Error indexing documents: {e}")


def query_documents(query_text, index_name, external_service):
    """
    Queries the indexed documents using the provided query text.
    Args:
        query_text (str): The text to query against the indexed documents.
        index_name (str): The name of the index to search in.
        external_service: An instance of the external service used for querying.
    """
    query_engine = QueryEngine(query_text=query_text, search_engine=external_service, index_name=index_name)
    response = query_engine.query()
    return response
