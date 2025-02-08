import rdkit.Chem as Chem
from rdkit.Chem import AllChem
from moltite import rdkit_to_biotite

def test_rdkit_to_biotite():
    """Test conversion from RDKit mol to Biotite AtomArray"""
    # Create test molecule
    mol = Chem.MolFromSmiles('CCO')
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)

    # Convert to biotite
    biotite_struct = rdkit_to_biotite(mol)

    # Check structure matches
    assert biotite_struct.array_length() == mol.GetNumAtoms()

    # Check coordinates exist
    assert biotite_struct.coord.shape == (mol.GetNumAtoms(), 3)

    # Check elements are preserved
    mol_elements = [atom.GetSymbol() for atom in mol.GetAtoms()]
    assert list(biotite_struct.element) == mol_elements
