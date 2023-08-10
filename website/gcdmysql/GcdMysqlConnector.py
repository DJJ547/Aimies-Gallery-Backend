from google.cloud.sql.connector import Connector
from website.gcdmysql.constant import DATABASE_NAME
from website.gcdmysql.constant import CONNECTION_NAME
from website.gcdmysql.constant import PATH
from google.cloud import secretmanager
import sqlalchemy
import os

# initialize Connector object
connector = Connector()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = PATH


class GcdMysqlConnector:
    def __init__(self):
        self.db_name = DATABASE_NAME
        self.conn_name = CONNECTION_NAME

    # Function to get CloudSQL instance password from Secret Manager
    def access_secret_version(self, project_id, secret_id, version_id):
        # Import the Secret Manager client library.
        # GCP project in which to store secrets in Secret Manager.
        project_id = "aimiefung-art-db"

        # ID of the secret to create.
        secret_id = "aimiefung-art-secret"

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the parent name from the project.
        parent = f"projects/{project_id}"

        # Create the parent secret.
        secret = client.create_secret(
            request={
                "parent": parent,
                "secret_id": secret_id,
                "secret": {"replication": {"automatic": {}}},
            }
        )

        # Add the secret version.
        version = client.add_secret_version(
            request={"parent": secret.name, "payload": {"data": b"hello world!"}}
        )

        # Access the secret version.
        response = client.access_secret_version(request={"name": version.name})

        # Print the secret payload.
        #
        # WARNING: Do not print the secret in a production environment - this
        # snippet is showing how to access the secret material.
        payload = response.payload.data.decode("UTF-8")
        print(f"Plaintext: {payload}")
        return payload

    # function to return the database connection object
    def get_connection(self):
        db_password = self.access_secret_version(self.conn_name, "aimiefung-art-secret", "1")
        print(db_password)
        conn = connector.connect(
            self.conn_name,
            "pymysql",
            user="root",
            password=db_password,
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
