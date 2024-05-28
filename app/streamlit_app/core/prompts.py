from langchain_core.prompts import ChatPromptTemplate
import streamlit_app.config.constants as CONSTANTS

PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", '{custom_persona}'+CONSTANTS.PERSONA),
        ('human', 'Sources: {summaries}'),
        ('assistant', f'Understood, go ahead and ask question'),
        ('human', "{question}")
    ]
)
