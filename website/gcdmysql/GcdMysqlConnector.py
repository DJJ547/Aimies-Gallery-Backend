from google.cloud.sql.connector import Connector
from website.gcdmysql.constant import DATABASE_NAME
from website.gcdmysql.constant import CONNECTION_NAME
from website.gcdmysql.constant import PATH
import sqlalchemy
import os

# initialize Connector object
connector = Connector()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH


class GcdMysqlConnector:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self.conn_name = CONNECTION_NAME

    # # Function to get CloudSQL instance password from Secret Manager
    # def access_secret_version(self, project_id, secret_id, version_id):
    #     """
    #     Access the payload for the given secret version if one exists. The version
    #     can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    #     """
    #
    #     # Import the Secret Manager client library.
    #     from google.cloud import secretmanager
    #
    #     # Create the Secret Manager client.
    #     client = secretmanager.SecretManagerServiceClient()
    #
    #     # Build the resource name of the secret version.
    #     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    #
    #     # Access the secret version.
    #     response = client.access_secret_version(request={"name": name})
    #     # Print the secret payload.
    #     # snippet is showing how to access the secret material.
    #     payload = response.payload.data.decode("UTF-8")
    #     return payload

    # function to return the database connection object
    def get_connection(self):
        conn = connector.connect(
            self.conn_name,
            "pymysql",
            user="root",
            password="Djj@19950420",
            db=self.db_name
        )
        return conn

    # create connection pool with 'creator' argument to our connection object function
    def create_pool(self):
        pool = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=self.get_connection,
        )
        return pool

    def perform_query(self, query):
        pool = self.create_pool()
        with pool.connect() as db_conn:
            result = db_conn.execute(sqlalchemy.text(query)).fetchall()
            # Do something with the results
        for row in result:
            print(row)
        return result
