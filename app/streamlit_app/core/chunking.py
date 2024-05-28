from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from streamlit_app.core.file_parsing import File

def chunk_file(file: File,
               chunk_size: int = 150,
               chunk_overlap: int = 15,
               model_name="gpt-4-turbo") -> File:
    """Chunks each document in a file into smaller documents
    according to the specified chunk size and overlap
    where the size is determined by the number of tokens for the specified model.
    """
    print(f"Chunking file '{file.name}' with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}, model_name='{model_name}'")

    # split each document into chunks
    chunked_docs = []
    for doc in file.docs:
        print(f"Splitting document with content length {len(doc.page_content)}")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=model_name,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        chunks = text_splitter.split_text(doc.page_content)
        print(f"Document split into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunk_doc = Document(
                page_content=chunk,
                metadata={
                    "page": doc.metadata.get("page", 1),
                    "chunk": i + 1,
                    "source": f"{doc.metadata.get('page', 1)}-{i + 1}",
                },
            )
            chunked_docs.append(chunk_doc)
            print(f"Created chunk {i + 1} with length {len(chunk)}")

    chunked_file = file.copy()
    chunked_file.docs = chunked_docs
    print(f"File '{file.name}' chunked into {len(chunked_docs)} documents")
    return chunked_file
