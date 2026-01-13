import asyncio
from typing import List, Dict, Any
from vercel_blob import list as vercel_list, download as vercel_download, put as vercel_put
import os

from njm_blob_cron.blob_storage.base import BlobStorage
from njm_blob_cron.config import VERCEL_BLOB_TOKEN

class VercelBlobStorage(BlobStorage):
    """
    Concrete implementation of the BlobStorage interface for Vercel Blob Storage.
    """

    def __init__(self):
        if not VERCEL_BLOB_TOKEN:
            raise ValueError("VERCEL_BLOB_TOKEN is not set.")
        os.environ["BLOB_TOKEN"] = VERCEL_BLOB_TOKEN

    async def list(self, folder: str) -> List[Dict[str, Any]]:
        """
        Lists all blobs in a specified folder in Vercel Blob Storage.
        """
        try:
            response = await asyncio.to_thread(vercel_list, prefix=folder, limit=1000)
            return response.get('blobs', [])
        except Exception as e:
            print(f"Error listing blobs in folder '{folder}': {e}")
            return []

    async def download(self, pathname: str) -> bytes:
        """
        Downloads a blob's content from Vercel Blob Storage.
        """
        try:
            content = await asyncio.to_thread(vercel_download, pathname)
            return content
        except Exception as e:
            print(f"Error downloading blob '{pathname}': {e}")
            raise

    async def upload(self, pathname: str, content: bytes) -> Dict[str, Any]:
        """
        Uploads content to a blob in Vercel Blob Storage.
        """
        try:
            response = await asyncio.to_thread(vercel_put, pathname, content)
            return response
        except Exception as e:
            print(f"Error uploading blob '{pathname}': {e}")
            raise
