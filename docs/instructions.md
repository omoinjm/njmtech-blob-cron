I have now updated the code to use the modern Vercel Blob SDK as you requested.

**Please run `poetry install`** to:
1.  Upgrade the `vercel-blob` library to the new version.
2.  Install the necessary testing libraries (`pytest-mock`).

After the installation is complete, please run `poetry run pytest tests/` again. This should resolve the `ImportError` and other test failures.