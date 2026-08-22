# Interview Coach – Project README

**Important:**

- **Always activate the virtual environment** before running any Python code in this project. The virtual environment lives in the `.venv` directory.
- To start the Flask application, run:
  ```
  .venv\Scripts\activate   # Windows PowerShell or CMD
  python app.py
  ```
- To run the test suite (and any debug scripts) reliably, use the provided wrapper script:
  ```
  run_tests.bat
  ```
  This script automatically invokes the Python interpreter from the `.venv` (`.venv\Scripts\python.exe -m pytest -vv`).

Running code without activating `.venv` may load a system‑wide installation of `sentence-transformers` that uses a different model (e.g., `all-MiniLM-L12-v2` with 768‑dim embeddings) which can cause inconsistent behavior.

---

*The rest of the project documentation can be added here.*
