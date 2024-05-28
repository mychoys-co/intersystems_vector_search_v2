from typing import List
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from langchain.chat_models.base import BaseChatModel
import streamlit_app.config.constants as CONSTANTS

def pop_docs_upto_limit(
    query: str, chain: StuffDocumentsChain, docs: List[Document], max_len: int
) -> List[Document]:
    """Pops documents from a list until the final prompt length is less than the max length."""
    
    print(f"Starting to pop documents to meet max length requirement of {max_len} tokens")
    token_count: int = chain.prompt_length(docs, question=query)
    print(f"Initial token count is {token_count} with {len(docs)} documents")

    while token_count > max_len and docs:
        popped_doc = docs.pop()
        print(f"Popped document with length {len(popped_doc.page_content)}")
        token_count = chain.prompt_length(docs, question=query)
        print(f"New token count is {token_count} with {len(docs)} documents remaining")

    print(f"Final token count is {token_count} with {len(docs)} documents remaining")
    return docs

def get_llm() -> BaseChatModel:
    llm = ChatOpenAI(
        model=CONSTANTS.OPENAI_LLM, 
        temperature=0, 
        api_key=CONSTANTS.OPENAI_API_KEY
    )
    print("Language model initialized successfully")
    return llm
