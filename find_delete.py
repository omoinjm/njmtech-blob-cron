import asyncio
import httpx
from njm_blob_cron.config import VERCEL_BLOB_TOKEN, BLOB_API_URL

async def test_endpoints():
    base_url = BLOB_API_URL.rstrip('/')
    headers = {"Authorization": f"Bearer {VERCEL_BLOB_TOKEN}"}
    path = "njmtech-blob-api/tests/2026-01-11_07:24:06/transcript.md.txt"
    
    endpoints = [
        ("/api/v1/blob/delete", "blob_path"),
        ("/api/v1/blob/delete", "path"),
        ("/api/v1/blob/remove", "blob_path"),
        ("/api/v1/blob/remove", "path"),
    ]
    
    async with httpx.AsyncClient() as client:
        for ep, param in endpoints:
            url = f"{base_url}{ep}"
            print(f"Trying DELETE {url} with {param}={path}")
            try:
                resp = await client.delete(url, params={param: path}, headers=headers)
                print(f"Response: {resp.status_code} - {resp.text}")
                if resp.status_code < 300:
                    print("SUCCESS!")
                    return
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_endpoints())
