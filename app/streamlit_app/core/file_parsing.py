from io import BytesIO
from typing import List, Any, Optional
import re

import docx2txt
from langchain.docstore.document import Document
import fitz
from hashlib import md5

from abc import abstractmethod, ABC
from copy import deepcopy


class File(ABC):
    """Represents an uploaded file comprised of Documents"""

    def __init__(
        self,
        name: str,
        id: str,
        metadata: Optional[dict[str, Any]] = None,
        docs: Optional[List[Document]] = None,
    ):
        self.name = name
        self.id = id
        self.metadata = metadata or {}
        self.docs = docs or []
        print(f"Initialized File: {self}")

    @classmethod
    @abstractmethod
    def from_bytes(cls, file: BytesIO) -> "File":
        """Creates a File from a BytesIO object"""

    def __repr__(self) -> str:
        return (f"File(name={self.name}, id={self.id},"
                " metadata={self.metadata}, docs={self.docs})")

    def __str__(self) -> str:
        return f"File(name={self.name}, id={self.id}, metadata={self.metadata})"

    def copy(self) -> "File":
        """Create a deep copy of this File"""
        copy = self.__class__(
            name=self.name,
            id=self.id,
            metadata=deepcopy(self.metadata),
            docs=deepcopy(self.docs),
        )
        return copy


def strip_consecutive_newlines(text: str) -> str:
    """Cleans up text for better markdown formatting"""
    
    # Remove extra newlines but keep paragraph separation
    text = re.sub(r'\n{3,}', '\n\n', text)  # Reduce multiple newlines to two (for Markdown paragraph separation)
    
    # Fix broken sentences or words
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # Replace single newlines within sentences/words with a space
    
    # Normalize any other excessive whitespace
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'\s*\n\s*', '\n', text)  # Strip spaces around newlines
    
    # Strip leading and trailing whitespace
    stripped_text = text.strip()
    
    print(f"Stripped consecutive newlines and cleaned up text")
    return stripped_text


class DocxFile(File):

    @classmethod
    def from_bytes(cls, file: BytesIO) -> "DocxFile":
        print(f"Processing DOCX file: {file.name}")
        text = docx2txt.process(file)
        # text = strip_consecutive_newlines(text)
        doc = Document(page_content=text.strip())
        doc.metadata["source"] = "p-1"
        file.seek(0)
        docx_file = cls(name=file.name, id=md5(file.read()).hexdigest(), docs=[doc])
        print(f"Created DocxFile: {docx_file}")
        return docx_file


class PdfFile(File):

    @classmethod
    def from_bytes(cls, file: BytesIO) -> "PdfFile":
        print(f"Processing PDF file: {file.name}")
        pdf = fitz.open(stream=file.read(), filetype="pdf")  # type: ignore
        docs = []
        for i, page in enumerate(pdf):
            text = page.get_text(sort=True)
            # text = strip_consecutive_newlines(text)
            doc = Document(page_content=text.strip())
            doc.metadata["page"] = i + 1
            doc.metadata["source"] = f"p-{i+1}"
            docs.append(doc)
            print(f"Processed page {i+1} of PDF")
        # file.read() mutates the file object, which can affect caching
        # so we need to reset the file pointer to the beginning
        file.seek(0)
        pdf_file = cls(name=file.name, id=md5(file.read()).hexdigest(), docs=docs)
        print(f"Created PdfFile: {pdf_file}")
        return pdf_file


class TxtFile(File):

    @classmethod
    def from_bytes(cls, file: BytesIO) -> "TxtFile":
        print(f"Processing TXT file: {file.name}")
        text = file.read().decode("utf-8", errors="replace")
        # text = strip_consecutive_newlines(text)
        file.seek(0)
        doc = Document(page_content=text.strip())
        doc.metadata["source"] = "p-1"
        txt_file = cls(name=file.name, id=md5(file.read()).hexdigest(), docs=[doc])
        print(f"Created TxtFile: {txt_file}")
        return txt_file


def read_file(file: BytesIO) -> File:
    """Reads an uploaded file and returns a File object"""
    print(f"Reading file: {file.name}")
    if file.name.lower().endswith(".docx"):
        file_obj = DocxFile.from_bytes(file)
    elif file.name.lower().endswith(".pdf"):
        file_obj = PdfFile.from_bytes(file)
    elif file.name.lower().endswith(".txt"):
        file_obj = TxtFile.from_bytes(file)
    else:
        raise NotImplementedError(
            f"File type {file.name.split('.')[-1]} not supported"
        )
    print(f"File read successfully: {file_obj}")
    return file_obj
