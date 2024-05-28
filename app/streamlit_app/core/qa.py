from typing import List
from langchain.docstore.document import Document
from streamlit_app.core.vectorstore import InterSystemsVectorStore
from streamlit_app.core.prompts import PROMPT_TEMPLATE
from pydantic.v1 import BaseModel, Field
from streamlit_app.core.llm import get_llm
from langchain.chains import create_structured_output_runnable

class GetAnswerBasedOnInputContext(BaseModel):
    """
    Returns 2 things:
    1) Short answer based on the provided context which is to the point.
    2) Sources used to answer the question out of multiple input sources else empty string.
    """
    answer: str = Field(
        ..., 
        description="Simple, to-the-point, easy to understand, intuitive answer based on provided context. "
                    "If not able to answer, then return 'I don't have context for this answer.'"
    )
    sources: str = Field(
        ..., 
        description="Single string joined by double commas (,,) of multiple given sources. "
                    "Return only those which are used to generate the answer."
    )

class AnswerWithSources(BaseModel):
    answer: str
    sources: List[Document]

def get_answer(query: str, custom_persona: str) -> AnswerWithSources:
    print(f"Querying vector store with query='{query}'")

    vector_store = InterSystemsVectorStore()
    relevant_docs = vector_store.similarity_search(query=query, k=10)
    print(f"Found {len(relevant_docs)} relevant documents")

    llm = get_llm()
    structured_llm = create_structured_output_runnable(
        GetAnswerBasedOnInputContext,
        llm,
        mode="openai-tools",
        return_single=True,
        prompt=PROMPT_TEMPLATE
    )
    
    print("Invoking structured LLM with relevant documents and query")
    result = structured_llm.invoke({
        "summaries": [doc.page_content for doc in relevant_docs], 
        "question": query,
        "custom_persona": custom_persona,
    })
    print("Structured LLM chain executed successfully")

    sources = get_sources(result.sources, relevant_docs)
    print(f"Filtered to {len(sources)} source documents")
    
    return AnswerWithSources(answer=result.answer, sources=sources)

def get_sources(sources: str, relevant_docs: List[Document]) -> List[Document]:
    """Retrieves the docs that were used to answer the question with the generated answer."""
    print("Retrieving sources for the generated answer")
    
    source_keys = sources.split(",,")
    source_docs = [doc for doc in relevant_docs if doc.page_content in source_keys]
    
    print(f"Retrieved {len(source_docs)} source documents")
    return source_docs
