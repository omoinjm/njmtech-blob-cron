import os
import vercel_blob
from njm_blob_cron.config import VERCEL_BLOB_TOKEN

# Note: vercel_blob usually uses an environment variable
os.environ["BLOB_READ_WRITE_TOKEN"] = "vercel_blob_rw_fxw7x7LUyCsSVOGX_72mj1Mp7AFFN33zxDKgcpOFfaZiV3k"

def test_delete():
    url = "https://fxw7x7luycssvogx.public.blob.vercel-storage.com/njmtech-blob-api/tests/2026-01-11_07%3A24%3A06/transcript.md.txt"
    print(f"Attempting to delete URL: {url}")
    try:
        res = vercel_blob.delete(url)
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_delete()
