import streamlit as st
from streamlit_app.core.intersystemsdb import CheckIntersystemsDB
from streamlit_app.core.file_parsing import read_file
from streamlit_app.ui_elements.ui_helper import display_file_read_error
from streamlit_app.core.chunking import chunk_file
from streamlit_app.core.embedding import FolderIndex

engine = CheckIntersystemsDB.create_database_engine()

def sidebar():
    with st.sidebar:
        record_count = CheckIntersystemsDB.count_table_records(engine)
        st.header("Status")

        db_connection_status = st.empty()
        record_count_placeholder = st.empty()
        data_status = st.empty()

        if CheckIntersystemsDB.verify_table_existence(engine):
            db_connection_status.success("Connected to IRIS InterSystems", icon="💚")
        else:
            db_connection_status.error("Failed to connect to IRIS InterSystems")

        record_count_placeholder.info(f"Number of records in DB: {record_count}")

        st.header("Upload File")
        uploaded_file = st.file_uploader(
            "Upload a PDF, DOCX, or TXT file",
            type=["pdf", "docx", "txt"],
            help="Scanned documents are not supported yet!"
        )

        if not uploaded_file and record_count == 0:
            data_status.warning("No data is stored, upload a file to get started")

        if uploaded_file and uploaded_file.name != st.session_state.get('uploaded_file', '-1'):
            try:
                CheckIntersystemsDB.ensure_table_exists(engine)
                file = read_file(uploaded_file)
                chunked_file = chunk_file(file, chunk_size=150, chunk_overlap=15)
                FolderIndex.save_files(files=[chunked_file])
                record_count = CheckIntersystemsDB.count_table_records(engine)
                data_status.success("Data loaded correctly!")
                record_count_placeholder.info(f"Number of records in DB: {record_count}")
                st.session_state.uploaded_file = uploaded_file.name  # Store file name in session state
            except Exception as e:
                display_file_read_error(e, file_name=uploaded_file.name)

        st.header("Persona")

        # Initialize session state for mode if not already set
        if 'mode' not in st.session_state:
            st.session_state.mode = "General"

        # Callback function to update the mode
        def update_mode():
            st.session_state.mode = st.session_state.persona_radio

        # Create the radio button and link it to the session state
        st.radio(
            "Select Persona", 
            options=["General", "Teacher", "Nurse", "Doctor"], 
            index=["General", "Teacher", "Nurse", "Doctor"].index(st.session_state.mode),
            key="persona_radio",
            on_change=update_mode
        )

        st.header("Empty Database")
        clear_all_records = st.button("Delete all records", type="primary")
        if clear_all_records:
            CheckIntersystemsDB.ensure_table_exists(engine)
            record_count_placeholder.info(f"Number of records in DB: {CheckIntersystemsDB.count_table_records(engine)}")
            if 'uploaded_file' in st.session_state:
                del st.session_state.uploaded_file  # Clear session state
            data_status.warning("No data is stored, upload a file to get started")
