# pysheetson

A tiny Python client for the Sheetson API (Google Sheets as a REST API).

## Installation

```bash
pip install -r requirements.txt
# or (editable install)
pip install -e .
```

## Quick Start

```python
from pysheetson import SheetsonClient

client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
print(client.list_rows("Cities", limit=5))
```
