#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example usage of the new batch operations and DataFrame features in pysheetson.
"""

from pysheetson import SheetsonClient

# Example 1: Batch operations
def example_batch_operations():
    client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
    
    # Define multiple operations
    operations = [
        {"operation": "create", "data": {"name": "Tokyo", "country": "Japan", "population": 14000000}},
        {"operation": "create", "data": {"name": "Seoul", "country": "South Korea", "population": 9720000}},
        {"operation": "update", "row_number": 2, "data": {"population": 14500000}},
        {"operation": "delete", "row_number": 5}
    ]
    
    # Execute batch operations
    result = client.batch_operations("Cities", operations)
    
    print(f"Total operations: {result['total_operations']}")
    print(f"Successful: {result['successful_operations']}")
    print(f"Failed: {result['failed_operations']}")
    
    # Print details of each operation
    for operation_result in result['batch_results']:
        if operation_result['success']:
            print(f"✓ {operation_result['operation']} succeeded")
        else:
            print(f"✗ {operation_result['operation']} failed: {operation_result['error']}")

# Example 2: DataFrame operations (requires pandas)
def example_dataframe_operations():
    try:
        import pandas as pd
        
        client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
        
        # Create a DataFrame with cities data
        df = pd.DataFrame([
            {"name": "Paris", "country": "France", "population": 2161000},
            {"name": "London", "country": "UK", "population": 8982000},
            {"name": "New York", "country": "USA", "population": 8336000},
            {"name": "Berlin", "country": "Germany", "population": 3669000},
            {"name": "Madrid", "country": "Spain", "population": 3223000}
        ])
        
        print(f"DataFrame shape: {df.shape}")
        print(df)
        
        # Insert all rows from DataFrame
        results = client.create_rows_from_dataframe("Cities", df, chunk_size=2)
        
        print(f"Processed {len(results)} batches")
        for i, batch_result in enumerate(results):
            print(f"Batch {i+1}: {batch_result['successful_operations']} successful operations")
            
    except ImportError:
        print("pandas is not installed. Install it with: pip install pandas")

# Example 3: Using functional aliases
def example_functional_aliases():
    # Using the new functional aliases
    from pysheetson import batch_operations, create_rows_from_dataframe
    
    api_key = "YOUR_API_KEY"
    spreadsheet_id = "YOUR_SPREADSHEET_ID"
    
    # Batch operations using functional interface
    operations = [
        {"operation": "create", "data": {"name": "Amsterdam", "country": "Netherlands"}},
        {"operation": "create", "data": {"name": "Rome", "country": "Italy"}}
    ]
    
    result = batch_operations(api_key, spreadsheet_id, "Cities", operations)
    print(f"Functional batch operations: {result['successful_operations']} successful")
    
    # DataFrame operations using functional interface
    try:
        import pandas as pd
        df = pd.DataFrame([
            {"name": "Vienna", "country": "Austria"},
            {"name": "Prague", "country": "Czech Republic"}
        ])
        
        results = create_rows_from_dataframe(api_key, spreadsheet_id, "Cities", df)
        print(f"Functional DataFrame operations: {len(results)} batches processed")
        
    except ImportError:
        print("pandas not available for functional DataFrame example")

if __name__ == "__main__":
    print("=== Batch Operations Example ===")
    example_batch_operations()
    
    print("\n=== DataFrame Operations Example ===")
    example_dataframe_operations()
    
    print("\n=== Functional Aliases Example ===")
    example_functional_aliases()
