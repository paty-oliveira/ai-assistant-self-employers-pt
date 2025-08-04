from .parser import PDFParser
from .llama_service import LlamaPDFParser

if __name__ == "__main__":
    print("This is the main entry point of the backend application.")

    # Example usage of PDFParser and LlamaPDFParser
    file_path = "path/to/your/file.pdf"

    llama_parser = LlamaPDFParser()
    pdf_parser = PDFParser(file_path, file_parser=llama_parser)
    documents = pdf_parser.parse()
