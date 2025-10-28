
# pysheetson Documentation

Tiny Python client for the Sheetson API (Google Sheets as a REST API)

## What is Sheetson?

Sheetson transforms any Google Sheet into a REST API. Every Google Sheet file is treated as a database, and each tab within that file becomes a table. This allows you to use Google Sheets as a backend for your applications without complex setup.

## Features

- Create / Read / Update / Delete rows
- Filtering with `where` (operators: $gte, $lte, $in, ...)
- Ordering (ascending / descending)
- Pagination (skip / limit)
- Field selection with `keys`
- **Batch operations** for multiple actions
- **DataFrame support** for pandas integration
- Clear docstrings and examples

## Prerequisites

### 1. Prepare your Google Sheet

**Important**: The first row of your sheet must always be the header row. Use alphanumeric characters for best compatibility.

Example sheet structure:

```text
| name          | state | country | population |
|---------------|-------|---------|------------|
| San Francisco | CA    | USA     | 3314000    |
| Los Angeles   | CA    | USA     | 12458000   |
| Tokyo         | null  | Japan   | 37400068   |
```

### 2. Share your spreadsheet

For security, Sheetson doesn't require your spreadsheet to be public. Instead:

1. Share your Google Sheet with `google@sheetson.com` as an **Editor**
2. Sheetson will handle the rest securely

### 3. Get your credentials

- **API Key**: Obtain from [Sheetson Dashboard](https://sheetson.com/dashboard)
- **Spreadsheet ID**: Found in your Google Sheet URL
- **Sheet Name**: The tab name (case-sensitive)

## Installation

```bash
pip install requests
# Optional: for DataFrame support
pip install pandas
```

## Usage Example

```python
from pysheetson import SheetsonClient
client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
client.list_rows("Cities", limit=2)
```

## Important Notes

### Authentication

- All API requests require a valid API key from [Sheetson Dashboard](https://sheetson.com/dashboard)
- For data-manipulating operations (create, update, delete), the API key is sent as Bearer token
- Read operations can use the API key as URL parameter

### Data Format

- **JSON Only**: All responses are in JSON format
- **String Values**: All cell values are returned as strings (except `rowIndex`)
- **Row Index**: Automatically added to each row result
- **Headers**: First row must contain column headers (alphanumeric recommended)

### API Endpoint

Base URL: `https://api.sheetson.com/v2`

### HTTP Status Codes

Sheetson API returns standard HTTP status codes:

**Successful requests:**

- `200 OK` - Resource retrieved (GET requests)
- `201 Created` - Resource created (POST requests)  
- `204 No Content` - Resource deleted (DELETE requests)

**Failed requests:**

- `403 Forbidden` - Invalid or missing API key
- `404 Not Found` - Spreadsheet or sheet not found
- `422 Unprocessable Entity` - Invalid data format

---

## API Reference

### SheetsonClient

Minimal client for the Sheetson API.

#### Parameters

- **api_key** (str): Your Sheetson API key (Bearer token).
- **spreadsheet_id** (str): The Google Spreadsheet ID you want to interact with.
- **base_url** (str, optional): Base URL for the Sheetson API. Defaults to `https://api.sheetson.com/v2`.

#### Methods

##### create_row(sheet, data)

Create (POST) a new row in the given sheet.

```python
client.create_row("Cities", {"name": "San Francisco", "country": "USA"})
```

##### get_row(sheet, row_number, extra_params=None)

Retrieve (GET) a specific row by row number.

```python
client.get_row("Cities", 3)
```

##### update_row(sheet, row_number, data)

Update (PUT) a specific row.

```python
client.update_row("Cities", 2, {"population": 3314000})
```

##### delete_row(sheet, row_number)

Delete (DELETE) a specific row.

```python
client.delete_row("Cities", 3)
```

##### list_rows(sheet, skip=None, limit=None, order_by=None, desc=False, keys=None)

List (GET) rows with optional pagination, ordering and field selection.

```python
client.list_rows("Cities", limit=5)
client.list_rows("Cities", order_by="population", desc=True, keys=["name", "country"])
```

##### search_rows(sheet, where=None, order_by=None, desc=False, skip=None, limit=None, keys=None)

Search/filter rows using the `where` parameter.

```python
client.search_rows("Cities", where={"country": "USA"})
client.search_rows("Cities", where={"population": {"$gte": 10000000, "$lte": 30000000}})
```

##### batch_operations(sheet, operations)

Perform multiple operations in a single batch request.

```python
operations = [
    {"operation": "create", "data": {"name": "Tokyo", "country": "Japan"}},
    {"operation": "update", "row_number": 2, "data": {"population": 14000000}},
    {"operation": "delete", "row_number": 5}
]
client.batch_operations("Cities", operations)
```

##### create_rows_from_dataframe(sheet, dataframe, chunk_size=100)

Create multiple rows from a pandas DataFrame.

```python
import pandas as pd
df = pd.DataFrame([
    {"name": "Paris", "country": "France", "population": 2161000},
    {"name": "London", "country": "UK", "population": 8982000}
])
client.create_rows_from_dataframe("Cities", df)
```

---

### Functional Aliases

These functions provide a functional interface to the API:

- `create_row(api_key, spreadsheet_id, sheet, data)`
- `get_row(api_key, spreadsheet_id, sheet, row_number)`
- `update_row(api_key, spreadsheet_id, sheet, row_number, data)`
- `delete_row(api_key, spreadsheet_id, sheet, row_number)`
- `list_rows(api_key, spreadsheet_id, sheet, ...)`
- `search_rows(api_key, spreadsheet_id, sheet, ...)`
- `batch_operations(api_key, spreadsheet_id, sheet, operations)`
- `create_rows_from_dataframe(api_key, spreadsheet_id, sheet, dataframe, ...)`

---

### Error Handling

- **SheetsonError**: Raised when the Sheetson API returns a non-2xx response.

---

## License

See [LICENSE](../LICENSE) for details.
