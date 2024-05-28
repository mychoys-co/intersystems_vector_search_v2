from streamlit_app.core.intersystemsdb import CheckIntersystemsDB
# from streamlit_app.core.file_parsing import read_file
# from streamlit_app.core.embedding import FolderIndex
# from streamlit_app.core.chunking import chunk_file
# from streamlit_app.core.qa import get_answer


engine = CheckIntersystemsDB.create_database_engine()
CheckIntersystemsDB.ensure_table_exists(engine)


# import os
# from io import BytesIO
# file_path = "./example_Imatinib_Teva.pdf"
# with open(file_path, "rb") as f:
#     file_content = BytesIO(f.read())
#     file_content.name = file_path

# CheckIntersystemsDB.count_table_records(engine)

# file = read_file(file_content)
# chunked_file = chunk_file(file, chunk_size=800, chunk_overlap=200)

# folder_index = FolderIndex.save_files(files=[chunked_file])
# CheckIntersystemsDB.count_table_records(engine)