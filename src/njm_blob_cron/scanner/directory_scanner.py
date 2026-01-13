import asyncio
from njm_blob_cron.blob_storage.base import BlobStorage
from njm_blob_cron.processing.base import FileProcessor
from njm_blob_cron.config import ROOT_SCAN_FOLDER
from collections import defaultdict
from typing import List, Dict, Any

class DirectoryScanner:
    """
    Scans a blob storage container, identifies directories that meet
    specific criteria, and triggers a file processor for them concurrently.
    This class encapsulates the core business logic of the application.
    """

    def __init__(self, blob_storage: BlobStorage, file_processor: FileProcessor):
        """
        Initializes the DirectoryScanner.

        Args:
            blob_storage: An object that conforms to the BlobStorage interface.
            file_processor: An object that conforms to the FileProcessor interface.
        """
        self.blob_storage = blob_storage
        self.file_processor = file_processor

    async def scan_and_process(self):
        """
        Starts the scanning and processing workflow.
        1. Lists all files from the root folder.
        2. Groups files by their parent directory.
        3. Identifies all qualifying files from those directories.
        4. Creates concurrent tasks to process each qualifying file.
        """
        print(f"Starting scan in root folder: '{ROOT_SCAN_FOLDER}'")
        all_blobs = await self.blob_storage.list(folder=ROOT_SCAN_FOLDER)

        directories = defaultdict(list)
        for blob in all_blobs:
            pathname = blob.get('pathname', '')
            directory = '/'.join(pathname.split('/')[:-1])
            if directory:
                directories[directory].append(blob)

        print(f"Found {len(directories)} directories to evaluate.")

        # Identify all files that need processing
        files_to_process = []
        for directory, files in directories.items():
            qualifying_file = self._get_qualifying_file(directory, files)
            if qualifying_file:
                files_to_process.append(qualifying_file)

        # Create concurrent tasks for processing
        if not files_to_process:
            print("No files to process.")
        else:
            print(f"Found {len(files_to_process)} files to process concurrently.")
            tasks = [self._process_file(file) for file in files_to_process]
            await asyncio.gather(*tasks)
        
        print("Scan finished.")

    def _get_qualifying_file(self, directory: str, files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Applies file evaluation rules. Returns the file to be processed if the
        directory qualifies, otherwise returns None.
        """
        print(f"Evaluating directory: '{directory}'")
        
        file_count = len(files)
        txt_files = [f for f in files if f['pathname'].lower().endswith('.txt')]
        md_files = [f for f in files if f['pathname'].lower().endswith('.md')]

        if md_files:
            print(f"  [SKIP] Directory contains a .md file: {md_files[0]['pathname']}")
            return None

        if file_count > 1:
            print(f"  [SKIP] Directory contains more than one file ({file_count} files).")
            return None

        if file_count == 1 and len(txt_files) == 1:
            file_to_process = txt_files[0]
            print(f"  [QUALIFIES] Found single .txt file: {file_to_process['pathname']}")
            return file_to_process
        
        print(f"  [SKIP] Directory does not meet processing criteria.")
        return None

    async def _process_file(self, file_to_process: Dict[str, Any]):
        """
        Downloads, processes, and handles errors for a single file.
        """
        pathname = file_to_process['pathname']
        try:
            print(f"  [PROCESS] Starting processing for: {pathname}")
            file_content_bytes = await self.blob_storage.download(pathname)
            file_content = file_content_bytes.decode('utf-8')
            
            await self.file_processor.process(file_content, pathname)
        except Exception as e:
            print(f"  [ERROR] Failed to process file {pathname}: {e}")


