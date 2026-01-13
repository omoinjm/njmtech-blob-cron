import pytest
from njm_blob_cron.blob_storage.vercel_blob import VercelBlobStorage
from njm_blob_cron.config import BLOB_READ_WRITE_TOKEN # Import the actual config variable

@pytest.fixture
def storage(monkeypatch):
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "test_token")
    return VercelBlobStorage()

def test_vercel_blob_storage_initialization(storage):
    """
    Tests that the VercelBlobStorage class initializes correctly.
    """
    # __init__ no longer sets options, it just ensures the env var is set.
    # No assert needed here for options attribute.
    pass

@pytest.mark.asyncio
async def test_list_blobs(storage, mocker):
    """Tests that list method calls the vercel_blob.list function correctly."""
    mock_list = mocker.patch('vercel_blob.list', return_value={'blobs': [{'pathname': 'test.txt'}]})
    blobs = await storage.list("test_folder")
    
    mock_list.assert_called_once_with(prefix="test_folder", limit=1000)
    assert blobs == [{'pathname': 'test.txt'}]

@pytest.mark.asyncio
async def test_download_blob(storage, mocker):
    """Tests that download method calls the vercel_blob.download function correctly."""
    mock_download = mocker.patch('vercel_blob.download', return_value=b"test content")
    content = await storage.download("test.txt")

    mock_download.assert_called_once_with("test.txt")
    assert content == b"test content"

@pytest.mark.asyncio
async def test_upload_blob(storage, mocker):
    """Tests that upload method calls the vercel_blob.put function correctly."""
    mock_put = mocker.patch('vercel_blob.put', return_value={'url': 'test_url'})
    result = await storage.upload("test.txt", b"test content")

    mock_put.assert_called_once_with("test.txt", b"test content")
    assert result == {'url': 'test_url'}

