import asyncio
import httpx

async def cleanup():
    list_url = "https://api.blob.njmtech.co.za/api/v1/blob/files"
    list_headers = {"Authorization": "Bearer 9kKAtYdMCgmGrMAVS818vnOkoHfDZkc9i"}
    
    delete_url = "https://blob.vercel-storage.com/delete"
    delete_headers = {"Authorization": "Bearer vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"}
    
    print("Listing all blobs for cleanup...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(list_url, headers=list_headers)
        if resp.status_code != 200:
            print(f"Error listing: {resp.text}")
            return
            
        data = resp.json().get('data', [])
        urls_to_delete = []
        
        for blob in data:
            pathname = blob['path']
            url = blob['url']
            
            # Identify mistakes
            is_mistake = False
            
            # 1. Duplicated root
            if pathname.count("njmtech-blob-api/") > 1:
                is_mistake = True
            
            # 2. Result files (to be re-processed correctly)
            elif pathname.endswith(".md.txt") or pathname.endswith(".md.md.txt"):
                is_mistake = True
                
            # 3. Orphaned or malformed nested
            elif "/transcript.md/" in pathname:
                is_mistake = True

            if is_mistake:
                print(f"Queuing for deletion: {pathname}")
                urls_to_delete.append(url)
        
        if not urls_to_delete:
            print("No mistakes found to clean up.")
            return
            
        print(f"Deleting {len(urls_to_delete)} files...")
        # Vercel delete takes up to 1000 URLs
        for i in range(0, len(urls_to_delete), 100):
            chunk = urls_to_delete[i:i+100]
            del_resp = await client.post(delete_url, json={"urls": chunk}, headers=delete_headers)
            print(f"Batch {i//100 + 1} response: {del_resp.status_code}")

if __name__ == "__main__":
    asyncio.run(cleanup())
