import pytest

def test_imports():
    try:
        import prettymol
        from prettymol import Repltools
        from prettymol import StructureSelector
        from prettymol import draw, load_pdb
        from prettymol import Material
        from prettymol import CartoonStyle
        assert True
    except ImportError as e:
        pytest.fail(f"Import test failed: {e}")
