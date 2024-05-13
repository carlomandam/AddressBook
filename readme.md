# Address Book API

A simple address book api created using fast api

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv ./env
   ```

2. Activate the virtual environment:

    * On Windows:
    ```bash
    ./env/Scripts/activate
    ```
    * On Unix or MacOS:
    ```bash
    source ./env/bin/activate
    ```
3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
4. Generate the SQLite database:

    ```bash
    python create_db.py
    ```

5. Run the FastAPI application in dev mode:

    ```bash
    fastapi dev main.py
    ```