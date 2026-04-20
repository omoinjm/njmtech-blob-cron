import os
import vercel_blob

os.environ["BLOB_READ_WRITE_TOKEN"] = "vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"

def check():
    res = vercel_blob.list()
    blobs = res.get('blobs', [])
    print(f"Total blobs: {len(blobs)}")
    for b in blobs:
        if "transcript" in b['pathname'] or "yt-transcribe" in b['pathname']:
            # Look for recent uploads (today)
            print(f"PATH: {b['pathname']}")

if __name__ == "__main__":
    check()
