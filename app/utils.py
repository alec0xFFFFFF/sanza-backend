# utils.py
import os
from google.cloud import storage
import voyageai

def get_gcs_client():
    client = storage.Client()
    # bucket = client.get_bucket('bucket-name')
    # blob = bucket.get_blob('path-to-file')
    # data = blob.download_as_string()
    return client.from_service_account_json('path/to/service_account.json')

def generate_embedding(text):
    vo = voyageai.Client(os.getenv("VOYAGE_API_KEY"))
    return vo.embed(
        text, model="voyage-large-2-instruct",
    ).embeddings
