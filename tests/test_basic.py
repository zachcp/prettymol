import pytest

def test_imports():
    try:
        import prettymol
        from prettymol import draw, load_pdb
        from prettymol import Repltools
        from prettymol import StructureSelector
        from prettymol import MaterialCreator
        from prettymol import StyleCreator
        from prettymol import LightingCreator
        assert True
    except ImportError as e:
        pytest.fail(f"Import test failed: {e}")
