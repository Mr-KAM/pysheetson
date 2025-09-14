def test_import():
    import pysheetson
    assert hasattr(pysheetson, "SheetsonClient")
