from langchain.vectorstores import VectorStore
from langchain.docstore.document import Document
import pandas as pd
import streamlit_app.config.constants as CONSTANTS
from sqlalchemy.exc import SQLAlchemyError
from typing import Iterable, List, Optional, Dict, Any, Type
from sqlalchemy import create_engine, text
from langchain_community.embeddings import HuggingFaceEmbeddings


class InterSystemsVectorStore(VectorStore):

    def __init__(self):
        print("Initializing InterSystemsVectorStore")
        self.embedding = HuggingFaceEmbeddings(
            model_name=CONSTANTS.EMBEDDING_MODEL)
        print("HuggingFaceEmbeddings model initialized successfully with model: ", CONSTANTS.EMBEDDING_MODEL)
        self.engine = self.create_database_engine()

    def create_database_engine(self):
        """
        Creates and returns a SQLAlchemy engine using a connection string from constants.
        """
        try:
            connection_string = CONSTANTS.CONNECTION_STRING
            print(f"Creating database engine with connection string: {connection_string}")
            engine = create_engine(connection_string)
            print("Database engine created successfully")
            return engine
        except Exception as e:
            print(f"Failed to create database engine: {e}")
            return None

    def add_texts(self,
                  texts: List[str],
                  metadatas: Optional[List[Dict]] = None,
                  **kwargs: Any) -> List[str]:
        """
        Run more texts through the embeddings and add to the vectorstore.
        """
        print(f"Starting to add {len(texts)} texts to the vectorstore")
        try:
            embeddings = self.embedding.embed_documents(list(texts))
            print("Documents embedded successfully")
            data = [{
                'text': text,
                'metadata': metadatas[i] if metadatas else {},
                'text_vector': embedding
            } for i, (text, embedding) in enumerate(zip(texts, embeddings))]
            df = pd.DataFrame(data)
            print("DataFrame created successfully with embedded documents and metadata")
            self.insert_table_data(df)
            print("Texts and metadata added to the vectorstore successfully")
            return True
        except Exception as e:
            print(f"Failed to add texts and metadata to the vectorstore: {e}")
            return False

    def insert_table_data(self, df):
        """
        Inserts data from a DataFrame into the specified table.
        """
        print(f"Attempting to insert data into table: {CONSTANTS.IRIS_TABLE_NAME}")
        if self.engine:
            try:
                with self.engine.connect() as conn:
                    print(f"Database connection established successfully for table: {CONSTANTS.IRIS_TABLE_NAME}")
                    with conn.begin():
                        for index, row in df.iterrows():
                            insert_sql = text("""
                                INSERT INTO {table_name}
                                (text, text_vector, metadata)
                                VALUES (:text, TO_VECTOR(:text_vector), :metadata)
                            """.format(table_name=CONSTANTS.IRIS_TABLE_NAME))
                            conn.execute(
                                insert_sql, {
                                    'text': row['text'],
                                    'text_vector': str(row['text_vector']),
                                    'metadata': str(row['metadata'])
                                })
                print("Data inserted successfully into table: ", CONSTANTS.IRIS_TABLE_NAME)
                return True
            except SQLAlchemyError as e:
                print(f"Data insertion into table {CONSTANTS.IRIS_TABLE_NAME} failed: {e}")
                return False
        print("Database engine is not available for inserting data")
        return False

    def similarity_search(self,
                          query: str,
                          k: int = 10,
                          **kwargs: Any) -> List[Document]:
        """
        Return docs most similar to query.
        """
        print(f"Performing similarity search for query: '{query}' with top {k} results")
        query_embedding = self.embedding.embed_query(query)
        print("Query embedded successfully for similarity search")
        if self.engine:
            try:
                search_sql = text("""
                    SELECT TOP :k text, metadata, VECTOR_DOT_PRODUCT(text_vector, TO_VECTOR(:search_vector)) as score
                    FROM {table_name}
                    WHERE VECTOR_DOT_PRODUCT(text_vector, TO_VECTOR(:search_vector)) >= {minimum_match_score}
                    ORDER BY score DESC
                """.format(table_name=CONSTANTS.IRIS_TABLE_NAME,
                           minimum_match_score=CONSTANTS.MINIMUM_MATCH_SCORE))
                with self.engine.connect() as conn:
                    print("Database connection established successfully for similarity search")
                    with conn.begin():
                        results = conn.execute(
                            search_sql, {
                                'k': k,
                                'search_vector': str(query_embedding)
                            }).fetchall()
                        documents = [
                            Document(page_content=result[0],
                                     metadata=eval(result[1]))
                            for result in results
                        ]
                        print(f"Similarity search returned {len(documents)} documents")
                        scores = [result[2] for result in results]
                        print(f"Similarity search scores: {scores}")
                        return documents
            except SQLAlchemyError as e:
                print(f"Vector search failed: {e}")
                return []
        print("Database engine is not available for similarity search")
        return []

    @classmethod
    def from_texts(cls,
                   texts: List[str],
                   **kwargs: Any) -> "InterSystemsVectorStore":
        """
        Return VectorStore initialized from texts and embeddings.
        """
        print(f"Creating InterSystemsVectorStore from {len(texts)} texts")
        store = cls()
        if store:
            print("InterSystemsVectorStore instance created successfully")
            store.add_texts(texts, **kwargs)
            print("InterSystemsVectorStore created and initialized from texts successfully")
        else:
            print("Failed to create InterSystemsVectorStore instance")
        return store
