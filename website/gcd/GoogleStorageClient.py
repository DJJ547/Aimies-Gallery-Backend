from google.cloud import storage
import os

currentPath = os.path.dirname(__file__)
# PATH = '/website/static/aimiefung-art-db-4b88d7b0f766.json'


# authenticate to Cloud Storage
def get_google_authentication():
    storage_client = storage.Client()
    return storage_client
