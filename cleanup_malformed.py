import asyncio
from njm_blob_cron.blob_storage.vercel_blob import VercelBlobStorage
from njm_blob_cron.config import ROOT_SCAN_FOLDER

async def cleanup():
    storage = VercelBlobStorage()
    blobs = await storage.list(folder=ROOT_SCAN_FOLDER)
    
    print(f"Scanning {len(blobs)} blobs for cleanup...")
    
    for blob in blobs:
        pathname = blob['pathname']
        
        # 1. Malformed paths (duplicated root folder)
        if pathname.count(f"{ROOT_SCAN_FOLDER}/") > 1:
            print(f"Deleting malformed path: {pathname}")
            await storage.delete(pathname)
            continue
            
        # 2. Files ending in .md.txt (unless we decide to keep them)
        # But wait, let's only delete them if they are in a subfolder with same name
        if ".md/" in pathname and pathname.endswith(".txt"):
            print(f"Deleting nested malformed file: {pathname}")
            await storage.delete(pathname)
            continue

        # 3. Orphaned .md.txt files (optional: delete all and re-run)
        # For now, let's just delete the ones that have duplicated extensions
        if pathname.endswith(".md.md.txt") or pathname.endswith(".md.txt"):
             # Keep the ones we just created if we have to, but user wants .md
             # Let's delete ALL .md.txt to start clean
             print(f"Deleting .md.txt file: {pathname}")
             await storage.delete(pathname)

if __name__ == "__main__":
    asyncio.run(cleanup())
