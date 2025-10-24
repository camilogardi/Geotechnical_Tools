"""
Tests for Tools module imports
"""
import pytest


def test_tools_import():
    """Test that Tools module can be imported"""
    try:
        import Tools
        assert hasattr(Tools, 'compute_rectangular_boussinesq')
        assert hasattr(Tools, 'save_cache')
        assert hasattr(Tools, 'load_cache')
    except ImportError as e:
        pytest.fail(f"Failed to import Tools module: {e}")


def test_tools_submodule_import():
    """Test that Tools.Tools submodule can be imported"""
    try:
        from Tools import Tools as ToolsModule
        assert hasattr(ToolsModule, 'compute_rectangular_boussinesq')
        assert hasattr(ToolsModule, 'save_cache')
        assert hasattr(ToolsModule, 'load_cache')
    except ImportError as e:
        pytest.fail(f"Failed to import Tools.Tools module: {e}")


def test_function_imports():
    """Test that functions can be imported directly"""
    try:
        from Tools import compute_rectangular_boussinesq, save_cache, load_cache
        assert callable(compute_rectangular_boussinesq)
        assert callable(save_cache)
        assert callable(load_cache)
    except ImportError as e:
        pytest.fail(f"Failed to import functions from Tools: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
