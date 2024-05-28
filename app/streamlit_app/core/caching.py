import streamlit as st
from streamlit.runtime.caching.hashing import HashFuncsDict

import streamlit_app.core.file_parsing as file_parsing
import streamlit_app.core.chunking as chunking
from streamlit_app.core.embedding import FolderIndex
from streamlit_app.core.file_parsing import File


def file_hash_func(file: File) -> str:
    """Get a unique hash for a file"""
    return file.id


@st.cache_data(show_spinner=False)
def bootstrap_caching():
    """Patch module functions with caching"""

    # Get all substypes of File from module
    file_subtypes = [
        cls
        for cls in vars(file_parsing).values()
        if isinstance(cls, type) and issubclass(cls, File) and cls != File
    ]
    file_hash_funcs: HashFuncsDict = {cls: file_hash_func for cls in file_subtypes}

    file_parsing.read_file = st.cache_data(show_spinner=False)(file_parsing.read_file)
    chunking.chunk_file = st.cache_data(show_spinner=False, hash_funcs=file_hash_funcs)(
        chunking.chunk_file
    )
    FolderIndex.save_files = st.cache_data(
        show_spinner=False, hash_funcs=file_hash_funcs
    )(FolderIndex.save_files)
