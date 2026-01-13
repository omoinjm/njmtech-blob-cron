import pytest
from njm_blob_cron import config
import os
import importlib
from unittest import mock

@mock.patch('dotenv.load_dotenv')
def test_validate_config_missing_vars(mock_load_dotenv, monkeypatch):
    """
    Tests that validate_config raises a ValueError if required
    environment variables are missing.
    """
    monkeypatch.delenv("BLOB_READ_WRITE_TOKEN", raising=False)
    importlib.reload(config)
    with pytest.raises(ValueError, match="Missing required environment variables: BLOB_READ_WRITE_TOKEN"):
        config.validate_config()

@mock.patch('dotenv.load_dotenv')
def test_validate_config_all_vars_present(mock_load_dotenv, monkeypatch):
    """
    Tests that validate_config runs without error if all required
    environment variables are present.
    """
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "test_token")
    importlib.reload(config)
    try:
        config.validate_config()
    except ValueError:
        pytest.fail("validate_config() raised ValueError unexpectedly!")
