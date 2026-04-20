import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

# Add src to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock external dependencies before importing project modules
import ollama
ollama.AsyncClient = MagicMock()

from njm_blob_cron.scanner.directory_scanner import DirectoryScanner
from njm_blob_cron.processing.markdown_transformer import MarkdownTransformer
from njm_blob_cron.blob_storage.base import BlobStorage

class MockBlobStorage(BlobStorage):
    def __init__(self):
        self.files = {
            'recordings/meeting_1/transcript.txt': b"John: Hello everyone. Um, we should talk about the, like, budget. Jane: I agree, John. Let's, ah, set a deadline for Friday."
        }
        self.uploaded = {}

    async def list(self, folder: str):
        return [{'pathname': k} for k in self.files.keys()]

    async def download(self, pathname: str):
        return self.files[pathname]

    async def upload(self, pathname: str, content: bytes):
        self.uploaded[pathname] = content.decode('utf-8')
        print(f"--- MOCK UPLOAD: {pathname} ---\n{self.uploaded[pathname]}\n--- END MOCK ---")

async def test_run():
    print("Starting Mock Test Run...")
    
    # 1. Mock Ollama Response
    mock_ollama = MagicMock()
    mock_ollama.chat = AsyncMock(return_value={
        'message': {
            'content': "# Meeting Summary\n\n- **Topic:** Budget discussion\n- **Deadline:** Friday\n\n### Action Items\n- Set budget by Friday."
        }
    })
    
    # Inject mock into MarkdownTransformer
    blob_storage = MockBlobStorage()
    transformer = MarkdownTransformer(blob_storage=blob_storage)
    transformer.client = mock_ollama
    
    # 2. Run Scanner
    scanner = DirectoryScanner(blob_storage=blob_storage, file_processor=transformer)
    
    await scanner.scan_and_process()
    
    print("\nTest Run Completed Successfully!")
    if 'recordings/meeting_1/transcript.md' in blob_storage.uploaded:
        print("Verified: Markdown file was generated and 'uploaded'.")
    else:
        print("Error: Markdown file was NOT generated.")

if __name__ == "__main__":
    asyncio.run(test_run())
