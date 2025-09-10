An AI assistant that helps self-employed people in Portugal get **clear and reliable answers about Social Security, taxes, and labor regulations.**

Navigating Social Security, taxes, and labor rules can be confusing and time-consuming. This project aims to **make bureaucracy simpler** by putting all the essential information in one place, explained clearly and in the user's preferred language.


### What it does?
- Chat with the assistant in Portuguese or English
- Get simplified explanations about rights and obligations
- Uses information from official government documents

### Who it helps?
- Self-employed worked in Portugal
- Freelancers and small business owners
- Anyone who wants to better understand their rights and obligations without digging through complex documents

### Technologies behind
- **Python** - core programming language of the project
- **LlamaIndex** - parsing and indexing official PDF documents for efficient retrieval
- **Retrieval-Augmented Generation (RAG)** - combines document retrieval with AI to generate grounded answers
- **OpenAI API** - powers natural language understanding and multilingual support (Portuguese + English)
- **FastAPI** - backend API to serve the assistant and handle chat requests
- **Streamlit** - interactive web interface for users to chat with the assistant
- **Docker** - containerization for easy deployment and reproducibility
