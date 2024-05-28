import streamlit as st


def show_references(data):
    if data:
        with st.expander('Show references'):
            for doc in data:
                st.markdown(f"### Page:-{doc.metadata['source'].split('-')[0]}")
                st.markdown(f"**File Name:** {doc.metadata['file_name']}")
                st.markdown(doc.page_content)
                st.markdown("<hr style='border:1px solid black'>", unsafe_allow_html=True)
