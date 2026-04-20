import asyncio
import httpx
import os
import vercel_blob

os.environ["BLOB_READ_WRITE_TOKEN"] = "vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"

async def purge():
    delete_url = "https://blob.vercel-storage.com/delete"
    delete_headers = {"Authorization": f"Bearer {os.environ['BLOB_READ_WRITE_TOKEN']}"}
    
    print("Listing all blobs for absolute purge...")
    res = vercel_blob.list()
    blobs = res.get('blobs', [])
    
    urls_to_delete = []
    for b in blobs:
        if b['pathname'].endswith(".md"):
            print(f"Queuing for deletion: {b['pathname']}")
            urls_to_delete.append(b['url'])
            
    if not urls_to_delete:
        print("No files to purge.")
        return
        
    print(f"Deleting {len(urls_to_delete)} files...")
    async with httpx.AsyncClient() as client:
        for i in range(0, len(urls_to_delete), 100):
            chunk = urls_to_delete[i:i+100]
            resp = await client.post(delete_url, json={"urls": chunk}, headers=delete_headers)
            print(f"Batch {i//100 + 1} response: {resp.status_code}")

if __name__ == "__main__":
    asyncio.run(purge())
