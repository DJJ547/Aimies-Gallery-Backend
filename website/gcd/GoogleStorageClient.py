from google.cloud import storage
from dotenv import dotenv_values
import os

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/jdai1/OneDrive/Desktop/PythonWorkSpace/AimiesGallery.flask/website/static/aimiefung-art-db-395704-97e3664dac9e.json'
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = dotenv_values(".env")


# authenticate to Cloud Storage
def get_google_authentication():
    storage_client = storage.Client(project='aimiefung-art-db-395704')
    return storage_client
