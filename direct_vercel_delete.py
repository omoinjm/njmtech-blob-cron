import asyncio
import httpx

async def test_delete():
    token = "vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"
    url = "https://fxw7x7luycssvogx.public.blob.vercel-storage.com/njmtech-blob-api/tests/2026-01-11_07%3A24%3A06/transcript.md.txt"
    
    # Official Vercel Blob delete endpoint
    api_url = f"https://blob.vercel-storage.com/delete"
    headers = {"Authorization": f"Bearer {token}"}
    body = {"urls": [url]}
    
    print(f"Attempting to delete URL via official API: {url}")
    async with httpx.AsyncClient() as client:
        resp = await client.post(api_url, json=body, headers=headers)
        print(f"Response: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_delete())
