# Quick Start Guide - pysheetson

This guide will help you get started with pysheetson in minutes.

## Step 1: Prepare Your Google Sheet

1. **Create a Google Sheet** with a header row (mandatory)
2. **Use descriptive column names** (alphanumeric characters recommended)

Example:
```text
| name          | country | population | founded |
|---------------|---------|------------|---------|
| San Francisco | USA     | 3314000    | 1776    |
| Tokyo         | Japan   | 37400068   | 1603    |
| Paris         | France  | 10901000   | 300     |
```

## Step 2: Share Your Sheet

Share your Google Sheet with `google@sheetson.com` as an **Editor**:

1. Click **Share** button in your Google Sheet
2. Add `google@sheetson.com` 
3. Set permission to **Editor**
4. Click **Send**

## Step 3: Get Your Credentials

1. **API Key**: Sign up at [Sheetson](https://sheetson.com) and get your API key from the [Dashboard](https://sheetson.com/dashboard)
2. **Spreadsheet ID**: Copy from your Google Sheet URL
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
   ```
3. **Sheet Name**: The tab name in your spreadsheet (case-sensitive)

## Step 4: Install pysheetson

```bash
pip install requests
# Optional: for DataFrame support
pip install pandas
```

## Step 5: Start Coding

### Basic Usage

```python
from pysheetson import SheetsonClient

# Initialize client
client = SheetsonClient(
    api_key="your_api_key_here",
    spreadsheet_id="your_spreadsheet_id_here"
)

# Create a new row
new_city = client.create_row("Cities", {
    "name": "London",
    "country": "UK", 
    "population": "8982000",
    "founded": "43"
})
print(f"Created row: {new_city}")

# Read all rows
cities = client.list_rows("Cities", limit=10)
print(f"Found {len(cities['results'])} cities")

# Search for specific rows
usa_cities = client.search_rows("Cities", where={"country": "USA"})
print(f"USA cities: {usa_cities}")

# Update a row
updated = client.update_row("Cities", 2, {"population": "3400000"})
print(f"Updated row: {updated}")

# Delete a row
deleted = client.delete_row("Cities", 3)
print(f"Deleted row: {deleted}")
```

### Batch Operations

```python
# Multiple operations at once
operations = [
    {"operation": "create", "data": {"name": "Berlin", "country": "Germany"}},
    {"operation": "update", "row_number": 2, "data": {"population": "3700000"}},
    {"operation": "delete", "row_number": 5}
]

result = client.batch_operations("Cities", operations)
print(f"Batch result: {result['successful_operations']} successful")
```

### DataFrame Integration

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame([
    {"name": "Madrid", "country": "Spain", "population": "3223000"},
    {"name": "Rome", "country": "Italy", "population": "2873000"}
])

# Bulk insert from DataFrame
results = client.create_rows_from_dataframe("Cities", df)
print(f"Inserted {len(results)} batches")
```

## Common Patterns

### Pagination
```python
# Get data in chunks
all_data = []
skip = 0
limit = 100

while True:
    batch = client.list_rows("Cities", skip=skip, limit=limit)
    if not batch['results']:
        break
    all_data.extend(batch['results'])
    skip += limit
```

### Filtering & Sorting
```python
# Complex queries
large_cities = client.search_rows("Cities", 
    where={"population": {"$gte": "1000000"}},
    order_by="population", 
    desc=True,
    limit=5
)
```

### Error Handling
```python
from pysheetson import SheetsonError

try:
    result = client.create_row("Cities", {"name": "Test"})
except SheetsonError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"General Error: {e}")
```

## Next Steps

- Check out the [full API documentation](index.md)
- Browse [example scripts](../examples/)
- Read the [Sheetson API docs](https://docs.sheetson.com/) for advanced features

## Troubleshooting

**Common Issues:**

1. **403 Forbidden**: Check your API key
2. **404 Not Found**: Verify spreadsheet ID and sheet name
3. **422 Unprocessable**: Check your data format
4. **No data returned**: Ensure you shared the sheet with `google@sheetson.com`

**Data Format Notes:**
- All values are returned as strings
- Use consistent column headers
- Empty cells return `null`
- Row numbers start from 2 (row 1 is headers)
