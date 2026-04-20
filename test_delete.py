import asyncio
from njm_blob_cron.blob_storage.vercel_blob import VercelBlobStorage

async def test():
    s = VercelBlobStorage()
    path1 = "njmtech-blob-api/tests/2026-01-11_07:24:06/transcript.md.txt"
    path2 = "tests/2026-01-11_07:24:06/transcript.md.txt"
    print(f"Testing deletion for: {path1}")
    res1 = await s.delete(path1)
    print(f"Full path result: {res1}")
    
    print(f"Testing deletion for: {path2}")
    res2 = await s.delete(path2)
    print(f"Relative path result: {res2}")

if __name__ == "__main__":
    asyncio.run(test())
