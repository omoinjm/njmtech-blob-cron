import os
import vercel_blob

os.environ["BLOB_READ_WRITE_TOKEN"] = "vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"

def list_all():
    print("Listing all raw blobs...")
    res = vercel_blob.list()
    blobs = res.get('blobs', [])
    print(f"Found {len(blobs)} total blobs.")
    for b in blobs:
        print(f"PATH: {b['pathname']} | URL: {b['url']}")

if __name__ == "__main__":
    list_all()
