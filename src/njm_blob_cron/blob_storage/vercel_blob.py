import asyncio
from typing import List, Dict, Any
import vercel_blob # Import the module directly

from njm_blob_cron.blob_storage.base import BlobStorage


class VercelBlobStorage(BlobStorage):
    """
    Concrete implementation of the BlobStorage interface for Vercel Blob Storage.
    This implementation uses the vercel-blob Python SDK directly.
    """

    def __init__(self):
        # The Vercel Blob SDK is expected to pick up the token from environment variables
        # (e.g., BLOB_READ_WRITE_TOKEN). We only check for its existence.
        pass

    async def list(self, folder: str) -> List[Dict[str, Any]]:
        """
        Lists all blobs in a specified folder in Vercel Blob Storage.
        """
        try:
            # Use vercel_blob.list directly
            response = await asyncio.to_thread(vercel_blob.list, prefix=folder, limit=1000)
            return response.get("blobs", [])
        except Exception as e:
            print(f"Error listing blobs in folder '{folder}': {e}")
            return []

    async def download(self, pathname: str) -> bytes:
        """
        Downloads a blob's content from Vercel Blob Storage.
        """
        try:
            # Use vercel_blob.download directly
            content = await asyncio.to_thread(vercel_blob.download, pathname)
            return content
        except Exception as e:
            print(f"Error downloading blob '{pathname}': {e}")
            raise

    async def upload(self, pathname: str, content: bytes) -> Dict[str, Any]:
        """
        Uploads content to a blob in Vercel Blob Storage.
        """
        try:
            # Use vercel_blob.put directly
            blob_result = await asyncio.to_thread(
                vercel_blob.put, pathname, content
            )
            return blob_result
        except Exception as e:
            print(f"Error uploading blob '{pathname}': {e}")
            raise
