# -*- coding: utf-8 -*-
"""
pysheetson: Tiny Python client for the Sheetson API (Google Sheets as a REST API)

Features:
- Create / Read / Update / Delete rows
- Filtering with `where` (operators: $gte, $lte, $in, ...)
- Ordering (ascending / descending)
- Pagination (skip / limit)
- Field selection with `keys`
- Clear docstrings and examples

Requirements:
    pip install requests
"""
from __future__ import annotations

import json
import requests
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Union

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

__all__ = [
    "SheetsonClient",
    "create_row",
    "get_row",
    "update_row",
    "delete_row",
    "search_rows",
    "list_rows",
    "batch_operations",
    "create_rows_from_dataframe",
]

JSONMapping = Mapping[str, Any]
JSONDict = Dict[str, Any]


class SheetsonError(RuntimeError):
    """Generic error raised when the Sheetson API returns a non-2xx response."""


class SheetsonClient:
    """Minimal client for the Sheetson API.

    Parameters
    ----------
    api_key : str
        Your Sheetson API key (Bearer token).
    spreadsheet_id : str
        The Google Spreadsheet ID you want to interact with.
    base_url : str, optional
        Base URL for the Sheetson API. Defaults to "https://api.sheetson.com/v2".

    Examples
    --------
    >>> from pysheetson import SheetsonClient
    >>> client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
    >>> client.list_rows("Cities", limit=2)
    """

    def __init__(self, api_key: str, spreadsheet_id: str, *, base_url: str = "https://api.sheetson.com/v2") -> None:
        self.api_key = api_key
        self.spreadsheet_id = spreadsheet_id
        self.base_url = base_url.rstrip("/")

    @property
    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-Spreadsheet-Id": self.spreadsheet_id,
            "Content-Type": "application/json",
        }

    def _raise_for_status(self, resp: requests.Response) -> None:
        if 200 <= resp.status_code < 300:
            return
        try:
            payload = resp.json()
        except Exception:
            payload = {"error": resp.text}
        raise SheetsonError(f"{resp.status_code} {resp.reason}: {payload}")

    @staticmethod
    def _serialize_where(where: Optional[Union[str, JSONMapping]]) -> Optional[str]:
        if where is None:
            return None
        if isinstance(where, str):
            where = where.strip()
            return where
        return json.dumps(dict(where))

    @staticmethod
    def _serialize_keys(keys: Optional[Iterable[str]]) -> Optional[str]:
        if keys is None:
            return None
        keys_list = list(keys)
        return ",".join(keys_list) if keys_list else None

    # ---------------- Core CRUD ----------------
    def create_row(self, sheet: str, data: JSONMapping) -> JSONDict:
        """Create (POST) a new row in the given sheet.

        Examples
        --------
        >>> client.create_row("Cities", {"name": "San Francisco", "country": "USA"})
        """
        url = f"{self.base_url}/sheets/{sheet}"
        resp = requests.post(url, headers=self._headers, json=dict(data))
        self._raise_for_status(resp)
        return resp.json()

    def get_row(self, sheet: str, row_number: int, *, extra_params: Optional[JSONMapping] = None) -> JSONDict:
        """Retrieve (GET) a specific row by row number.

        Examples
        --------
        >>> client.get_row("Cities", 3)
        """
        url = f"{self.base_url}/sheets/{sheet}/{row_number}"
        resp = requests.get(url, headers=self._headers, params=dict(extra_params or {}))
        self._raise_for_status(resp)
        return resp.json()

    def update_row(self, sheet: str, row_number: int, data: JSONMapping) -> JSONDict:
        """Update (PUT) a specific row.

        Examples
        --------
        >>> client.update_row("Cities", 2, {"population": 3314000})
        """
        url = f"{self.base_url}/sheets/{sheet}/{row_number}"
        resp = requests.put(url, headers=self._headers, json=dict(data))
        self._raise_for_status(resp)
        return resp.json()

    def delete_row(self, sheet: str, row_number: int) -> JSONDict:
        """Delete (DELETE) a specific row.

        Examples
        --------
        >>> client.delete_row("Cities", 3)
        """
        url = f"{self.base_url}/sheets/{sheet}/{row_number}"
        resp = requests.delete(url, headers=self._headers)
        self._raise_for_status(resp)
        return resp.json()

    # -------------- Listing & Searching --------------
    def list_rows(self, sheet: str, *, skip: Optional[int] = None, limit: Optional[int] = None,
                  order_by: Optional[str] = None, desc: bool = False, keys: Optional[Iterable[str]] = None) -> JSONDict:
        """List (GET) rows with optional pagination, ordering and field selection.

        Examples
        --------
        >>> client.list_rows("Cities", limit=5)
        >>> client.list_rows("Cities", order_by="population", desc=True, keys=["name", "country'])
        """
        url = f"{self.base_url}/sheets/{sheet}"
        params: MutableMapping[str, Any] = {}
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        if order_by:
            params["order"] = f"-{order_by}" if desc else order_by
        keys_str = self._serialize_keys(keys)
        if keys_str:
            params["keys"] = keys_str
        resp = requests.get(url, headers=self._headers, params=params)
        self._raise_for_status(resp)
        return resp.json()

    def search_rows(self, sheet: str, *, where: Optional[Union[str, JSONMapping]] = None,
                    order_by: Optional[str] = None, desc: bool = False,
                    skip: Optional[int] = None, limit: Optional[int] = None,
                    keys: Optional[Iterable[str]] = None) -> JSONDict:
        """Search/filter rows using the `where` parameter.

        Examples
        --------
        >>> client.search_rows("Cities", where={"country": "USA"})
        >>> client.search_rows("Cities", where={"population": {"$gte": 10_000_000, "$lte": 30_000_000}})
        """
        url = f"{self.base_url}/sheets/{sheet}"
        params: MutableMapping[str, Any] = {}
        where_str = self._serialize_where(where)
        if where_str:
            params["where"] = where_str
        if order_by:
            params["order"] = f"-{order_by}" if desc else order_by
        if skip is not None:
            params["skip"] = skip
        if limit is not None:
            params["limit"] = limit
        keys_str = self._serialize_keys(keys)
        if keys_str:
            params["keys"] = keys_str
        resp = requests.get(url, headers=self._headers, params=params)
        self._raise_for_status(resp)
        return resp.json()

    # -------------- Batch Operations & DataFrame Support --------------
    def create_rows_from_dataframe(self, sheet: str, dataframe, *, chunk_size: int = 100) -> List[JSONDict]:
        """Create multiple rows from a pandas DataFrame.

        Parameters
        ----------
        sheet : str
            The sheet name to insert rows into.
        dataframe : pandas.DataFrame
            The DataFrame containing the data to insert.
        chunk_size : int, optional
            Number of rows to process in each batch. Defaults to 100.

        Returns
        -------
        List[JSONDict]
            List of responses from each batch operation.

        Examples
        --------
        >>> import pandas as pd
        >>> df = pd.DataFrame([
        ...     {"name": "Paris", "country": "France", "population": 2161000},
        ...     {"name": "London", "country": "UK", "population": 8982000}
        ... ])
        >>> client.create_rows_from_dataframe("Cities", df)

        Raises
        ------
        ImportError
            If pandas is not installed.
        """
        if not PANDAS_AVAILABLE:
            raise ImportError("pandas is required for DataFrame operations. Install it with: pip install pandas")
        
        # Convert DataFrame to list of dictionaries
        records = dataframe.to_dict('records')
        
        # Process in chunks
        results = []
        for i in range(0, len(records), chunk_size):
            chunk = records[i:i + chunk_size]
            batch_result = self.batch_operations(sheet, [
                {"operation": "create", "data": record} for record in chunk
            ])
            results.append(batch_result)
        
        return results

    def batch_operations(self, sheet: str, operations: List[Dict[str, Any]]) -> JSONDict:
        """Perform multiple operations in a single batch request.

        Parameters
        ----------
        sheet : str
            The sheet name to perform operations on.
        operations : List[Dict[str, Any]]
            List of operations to perform. Each operation should have:
            - "operation": str ("create", "update", "delete")
            - "data": dict (for create/update operations)
            - "row_number": int (for update/delete operations)

        Returns
        -------
        JSONDict
            Response from the batch operation.

        Examples
        --------
        >>> operations = [
        ...     {"operation": "create", "data": {"name": "Tokyo", "country": "Japan"}},
        ...     {"operation": "update", "row_number": 2, "data": {"population": 14000000}},
        ...     {"operation": "delete", "row_number": 5}
        ... ]
        >>> client.batch_operations("Cities", operations)

        Notes
        -----
        This method performs operations sequentially. For true batch API support,
        the Sheetson API would need to support batch endpoints.
        """
        results = []
        
        for operation in operations:
            op_type = operation.get("operation")
            
            try:
                if op_type == "create":
                    data = operation.get("data", {})
                    result = self.create_row(sheet, data)
                    results.append({"operation": "create", "success": True, "result": result})
                    
                elif op_type == "update":
                    row_number = operation.get("row_number")
                    data = operation.get("data", {})
                    if row_number is None:
                        raise ValueError("row_number is required for update operations")
                    result = self.update_row(sheet, row_number, data)
                    results.append({"operation": "update", "row_number": row_number, "success": True, "result": result})
                    
                elif op_type == "delete":
                    row_number = operation.get("row_number")
                    if row_number is None:
                        raise ValueError("row_number is required for delete operations")
                    result = self.delete_row(sheet, row_number)
                    results.append({"operation": "delete", "row_number": row_number, "success": True, "result": result})
                    
                else:
                    results.append({
                        "operation": op_type,
                        "success": False,
                        "error": f"Unknown operation type: {op_type}"
                    })
                    
            except Exception as e:
                results.append({
                    "operation": op_type,
                    "success": False,
                    "error": str(e),
                    "row_number": operation.get("row_number")
                })
        
        return {
            "batch_results": results,
            "total_operations": len(operations),
            "successful_operations": sum(1 for r in results if r.get("success", False)),
            "failed_operations": sum(1 for r in results if not r.get("success", False))
        }


# Functional aliases
def _client(api_key: str, spreadsheet_id: str) -> SheetsonClient:
    return SheetsonClient(api_key=api_key, spreadsheet_id=spreadsheet_id)


def create_row(api_key: str, spreadsheet_id: str, sheet: str, data: JSONMapping) -> JSONDict:
    return _client(api_key, spreadsheet_id).create_row(sheet, data)


def get_row(api_key: str, spreadsheet_id: str, sheet: str, row_number: int) -> JSONDict:
    return _client(api_key, spreadsheet_id).get_row(sheet, row_number)


def update_row(api_key: str, spreadsheet_id: str, sheet: str, row_number: int, data: JSONMapping) -> JSONDict:
    return _client(api_key, spreadsheet_id).update_row(sheet, row_number, data)


def delete_row(api_key: str, spreadsheet_id: str, sheet: str, row_number: int) -> JSONDict:
    return _client(api_key, spreadsheet_id).delete_row(sheet, row_number)


def list_rows(api_key: str, spreadsheet_id: str, sheet: str, *, skip: Optional[int] = None,
              limit: Optional[int] = None, order_by: Optional[str] = None,
              desc: bool = False, keys: Optional[Iterable[str]] = None) -> JSONDict:
    return _client(api_key, spreadsheet_id).list_rows(sheet, skip=skip, limit=limit,
                                                     order_by=order_by, desc=desc, keys=keys)


def search_rows(api_key: str, spreadsheet_id: str, sheet: str, *, where: Optional[Union[str, JSONMapping]] = None,
                order_by: Optional[str] = None, desc: bool = False, skip: Optional[int] = None,
                limit: Optional[int] = None, keys: Optional[Iterable[str]] = None) -> JSONDict:
    return _client(api_key, spreadsheet_id).search_rows(sheet, where=where,
                                                       order_by=order_by, desc=desc,
                                                       skip=skip, limit=limit, keys=keys)


def batch_operations(api_key: str, spreadsheet_id: str, sheet: str, operations: List[Dict[str, Any]]) -> JSONDict:
    return _client(api_key, spreadsheet_id).batch_operations(sheet, operations)


def create_rows_from_dataframe(api_key: str, spreadsheet_id: str, sheet: str, dataframe, *, chunk_size: int = 100) -> List[JSONDict]:
    return _client(api_key, spreadsheet_id).create_rows_from_dataframe(sheet, dataframe, chunk_size=chunk_size)
