"""
Test imports for Tools module
"""

import pytest


def test_import_tools_module():
    """Test that Tools module can be imported"""
    try:
        import Tools
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import Tools module: {e}")


def test_import_tools_functions():
    """Test that Tools functions exist and can be imported"""
    try:
        from Tools.Tools import compute_rectangular_boussinesq, save_cache, load_cache
        
        # Verify functions exist
        assert callable(compute_rectangular_boussinesq), \
            "compute_rectangular_boussinesq should be callable"
        assert callable(save_cache), "save_cache should be callable"
        assert callable(load_cache), "load_cache should be callable"
        
    except ImportError as e:
        pytest.fail(f"Failed to import Tools functions: {e}")


def test_import_from_package():
    """Test importing from Tools package"""
    try:
        from Tools import compute_rectangular_boussinesq, save_cache, load_cache
        
        assert callable(compute_rectangular_boussinesq)
        assert callable(save_cache)
        assert callable(load_cache)
        
    except ImportError as e:
        pytest.fail(f"Failed to import from Tools package: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
