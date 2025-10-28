# pysheetson

A tiny Python client for the Sheetson API - Transform any Google Sheet into a REST API.

## What is Sheetson?

Sheetson allows you to use Google Sheets as a database for your applications. Every Google Sheet becomes a database, and each tab becomes a table. No complex setup required!

## Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete rows
- ✅ **Advanced Filtering**: Use `where` clauses with operators ($gte, $lte, $in, etc.)
- ✅ **Sorting & Pagination**: Order results and paginate through large datasets
- ✅ **Batch Operations**: Perform multiple operations efficiently
- ✅ **DataFrame Support**: Direct integration with pandas DataFrames
- ✅ **Type Hints**: Full typing support for better development experience
- ✅ **Error Handling**: Comprehensive error handling with custom exceptions

## Quick Start

### 1. Setup Your Google Sheet

1. Create a Google Sheet with headers in the first row
2. Share it with `google@sheetson.com` as an Editor
3. Get your API key from [Sheetson Dashboard](https://sheetson.com/dashboard)

### 2. Install pysheetson

```bash
pip install requests
# Optional: for DataFrame support  
pip install pandas
```

### 3. Start Coding

```python
from pysheetson import SheetsonClient

# Initialize client
client = SheetsonClient(
    api_key="your_api_key_here",
    spreadsheet_id="your_spreadsheet_id_here"
)

# Basic operations
cities = client.list_rows("Cities", limit=10)
new_city = client.create_row("Cities", {"name": "Paris", "country": "France"})
client.update_row("Cities", 2, {"population": "2161000"})
client.delete_row("Cities", 3)

# Advanced filtering
large_cities = client.search_rows("Cities", 
    where={"population": {"$gte": "1000000"}},
    order_by="population", 
    desc=True
)

# Batch operations
operations = [
    {"operation": "create", "data": {"name": "Tokyo", "country": "Japan"}},
    {"operation": "update", "row_number": 2, "data": {"population": "37400068"}},
    {"operation": "delete", "row_number": 5}
]
result = client.batch_operations("Cities", operations)

# DataFrame integration (requires pandas)
import pandas as pd
df = pd.DataFrame([
    {"name": "London", "country": "UK"},
    {"name": "Berlin", "country": "Germany"}
])
client.create_rows_from_dataframe("Cities", df)
```

## Documentation

- 📖 [Full Documentation](https://mr-kam.github.io/pysheetson/)
- 🚀 [Github repo](https://github.com/Mr-KAM/pysheetson/)
- 💻 [Example Scripts](https://github.com/Mr-KAM/pysheetson/tree/master/examples)
- 🌐 [Sheetson API Docs](https://docs.sheetson.com/)

## Examples

Check out the [examples/](examples/) directory for more usage patterns:

- `quickstart.py` - Basic operations
- `batch_and_dataframe_example.py` - Advanced features

## Error Handling

```python
from pysheetson import SheetsonError

try:
    result = client.create_row("Cities", {"name": "Test"})
except SheetsonError as e:
    print(f"API Error: {e}")
```

## Development

```bash
# Clone the repository
git clone https://github.com/Mr-KAM/pysheetson.git
cd pysheetson

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Sheetson Official Website](https://sheetson.com/)
- [Sheetson API Documentation](https://docs.sheetson.com/)
- [GitHub Repository](https://github.com/Mr-KAM/pysheetson)
