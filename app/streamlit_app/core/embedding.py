from streamlit_app.core.file_parsing import File
from typing import List, Type, Dict, Optional
from langchain.docstore.document import Document
from streamlit_app.core.vectorstore import InterSystemsVectorStore
import streamlit_app.config.constants as CONSTANTS


class FolderIndex:
    """Save data to vectorDB"""

    @staticmethod
    def _combine_files(files: List[File]) -> List[Document]:
        """Combines all the documents in a list of files into a single list."""
        print(f"Combining {len(files)} files")
        all_texts = []
        for file in files:
            for doc in file.docs:
                doc.metadata["file_name"] = file.name
                doc.metadata["file_id"] = file.id
                all_texts.append(doc)
        print(f"Combined into {len(all_texts)} documents")
        return all_texts

    @staticmethod
    def _extract_metadata(docs: List[Document]) -> List[Dict]:
        """Extracts metadata from documents"""
        print(f"Extracting metadata from {len(docs)} documents")
        metadatas = [doc.metadata for doc in docs]
        print(f"Extracted {len(metadatas)} metadata entries")
        return metadatas

    @staticmethod
    def save_files(files: List[File]) -> "FolderIndex":
        """Creates an index from files."""
        print(
            f"Creating FolderIndex from {len(files)} files with embeddings and vector store"
        )
        try:
            all_docs = FolderIndex._combine_files(files)
            all_metadatas = FolderIndex._extract_metadata(all_docs)
            vector_store = InterSystemsVectorStore()
            status = vector_store.add_texts(texts=[doc.page_content for doc in all_docs], metadatas=all_metadatas)
            if status:
                print("Successfully created vector store index from texts")
                return True
            print("Failed to add data to database")
            return False
        except Exception as e:
            print(f"Failed to create FolderIndex: {e}")
            return False
