import streamlit_app.config.constants as CONSTANTS
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, text

class CheckIntersystemsDB:
    
    @staticmethod
    def create_database_engine():
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

    @staticmethod
    def count_table_records(engine):
        """
        Returns the count of records in the specified table.
        """
        try:
            if engine:
                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {CONSTANTS.IRIS_TABLE_NAME}"))
                    count = result.fetchone()[0]
                    print(f"Record count for table {CONSTANTS.IRIS_TABLE_NAME}: {count}")
                    return count
        except SQLAlchemyError as e:
            print(f"Unable to count records in the table: {e}")
        return 0

    @staticmethod
    def ensure_table_exists(engine):
        """
        Ensures that the table exists in the database.
        """
        print("Ensuring the table exists in the database")
        CheckIntersystemsDB.delete_existing_table(engine)
        if not CheckIntersystemsDB.verify_table_existence(engine):
            CheckIntersystemsDB.create_data_table(engine)

    @staticmethod
    def verify_table_existence(engine):
        """
        Checks if the specified table exists in the database.
        """
        if engine:
            try:
                with engine.connect() as conn:
                    with conn.begin():
                        check_sql = f"SELECT 1 FROM {CONSTANTS.IRIS_TABLE_NAME} WHERE 1=0"
                        conn.execute(text(check_sql))
                print(f"Table {CONSTANTS.IRIS_TABLE_NAME} exists in the database")
                return True
            except SQLAlchemyError:
                print(f"Table {CONSTANTS.IRIS_TABLE_NAME} does not exist in the database")
                return False
        print("No engine available to verify table existence")
        return False
    
    @staticmethod
    def delete_existing_table(engine):
        """
        Deletes the specified table if it exists in the database.
        """
        print(f"Drop table man: {CONSTANTS.IRIS_TABLE_NAME}")
        print(engine)
        if engine:
            try:
                with engine.connect() as conn:
                    with conn.begin():
                        drop_sql = f"DROP TABLE IF EXISTS {CONSTANTS.IRIS_TABLE_NAME}"
                        conn.execute(text(drop_sql))
                print(f"Existing table {CONSTANTS.IRIS_TABLE_NAME} deleted successfully")
                return True
            except SQLAlchemyError as e:
                print(f"Failed to drop table {CONSTANTS.IRIS_TABLE_NAME}: {e}")
                return False
        print("No engine available to delete table")
        return True

    @staticmethod
    def create_data_table(engine):
        """
        Creates a new table with specified schema.
        """
        if engine:
            try:
                with engine.connect() as conn:
                    with conn.begin():
                        create_sql = f"""
                        CREATE TABLE {CONSTANTS.IRIS_TABLE_NAME} (
                            text TEXT,
                            text_vector VECTOR(DOUBLE, 384),
                            metadata TEXT
                        )
                        """
                        conn.execute(text(create_sql))
                print(f"Data table {CONSTANTS.IRIS_TABLE_NAME} created successfully")
                return True
            except SQLAlchemyError as e:
                print(f"Failed to create table {CONSTANTS.IRIS_TABLE_NAME}: {e}")
                return False
        print("No engine available to create table")
        return False
