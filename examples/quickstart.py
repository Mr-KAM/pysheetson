from pysheetson import SheetsonClient

def main():
    client = SheetsonClient(api_key="YOUR_API_KEY", spreadsheet_id="YOUR_SPREADSHEET_ID")
    print(client.list_rows("Cities", limit=5))

if __name__ == "__main__":
    main()
