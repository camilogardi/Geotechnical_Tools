"""
Test suite for the Geotechnical Tools Streamlit app
"""

import pytest
import pandas as pd
from io import StringIO


def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit  # noqa: F401
        import pandas  # noqa: F401
        import matplotlib  # noqa: F401
        import plotly  # noqa: F401
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_sample_csv_processing():
    """Test basic CSV processing functionality"""
    # Create sample CSV data
    csv_data = """depth,pressure,density
10,100,1.5
20,200,1.6
30,300,1.7
40,400,1.8"""

    # Read CSV
    df = pd.read_csv(StringIO(csv_data))

    # Verify data structure
    assert df.shape == (4, 3)
    assert list(df.columns) == ['depth', 'pressure', 'density']

    # Verify numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    assert len(numeric_cols) == 3


def test_app_module_exists():
    """Test that app.py module can be imported"""
    try:
        import app
        assert hasattr(app, 'main')
    except ImportError as e:
        pytest.fail(f"Failed to import app module: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
