from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

class AzureBlobService(DefaultAzureCredential):
    """
    """

    def __init__(self, context, credential = None) :
        self._client = BlobServiceClient(context.blob.url, credential or DefaultAzureCredential())

    def close(self):
        self._client.close()

    def list_blobs(self, container_name: str):
        """List all blobs in the container."""
        container_client = self._client.get_container_client(container_name)
        return [blob.name for blob in container_client.list_blobs()]

    def find_blob(self, container_name: str, blob_name: str):
        """Find a blob in the container."""
        container_client = self._client.get_container_client(container_name)
        for blob in container_client.list_blobs():
            if blob.name == blob_name:
                return blob
        return None

