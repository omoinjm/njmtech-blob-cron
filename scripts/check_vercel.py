import asyncio
import sys
import os

try:
    import vercel
    from vercel.blob import AsyncBlobClient
    print(f"Vercel Package Version: {getattr(vercel, '__version__', 'unknown')}")
    print(f"AsyncBlobClient attributes: {dir(AsyncBlobClient)}")
    
    # Try to instantiate and check attributes of an instance
    client = AsyncBlobClient()
    print(f"AsyncBlobClient instance attributes: {dir(client)}")
    
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Exception: {e}")
