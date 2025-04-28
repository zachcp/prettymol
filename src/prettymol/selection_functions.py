import numpy as np
from biotite.structure import filter

"""
selectors.py - Functional selection helpers for molecular structures

This module provides curried versions of selection functions that return lambdas
which can be composed and combined for flexible molecular structure selection.

Example usage:
    from selectors import amino_acids, chain, resid

    # Create selections
    my_selection = [
        amino_acids(),
        chain("A"),
        resid(10)
    ]

    # Apply selections to structure
    selection_mask = all(sel(structure) for sel in my_selection)
"""

import numpy as np
from biotite.structure import filter


# ====== CURRIED 1-ARGUMENT FUNCTIONS ======
# These take no arguments (other than the structure which is applied later)

def amino_acids():
    """Select amino acids."""
    return lambda arr: filter.filter_amino_acids(arr)

def canonical_amino_acids():
    """Select canonical amino acids."""
    return lambda arr: filter.filter_canonical_amino_acids(arr)

def canonical_nucleotides():
    """Select canonical nucleotides."""
    return lambda arr: filter.filter_canonical_nucleotides(arr)

def carbohydrates():
    """Select carbohydrates."""
    return lambda arr: filter.filter_carbohydrates(arr)

def first_altloc():
    """Select first alternative location."""
    return lambda arr: filter.filter_first_altloc(arr)

def hetero():
    """Select hetero atoms."""
    return lambda arr: True == arr.get_annotation("hetero")

def highest_occupancy_altloc():
    """Select alternative location with highest occupancy."""
    return lambda arr: filter.filter_highest_occupancy_altloc(arr)

def intersection():
    """Select intersection of atoms."""
    return lambda arr: filter.filter_intersection(arr)

def ligand():
    """Select ligand molecules (hetero compounds that are not solvent or ions)."""
    return lambda arr: (
        hetero()(arr) & ~solvent()(arr) & ~monoatomic_ions()(arr)
    )

def linear_bond_continuity():
    """Select atoms with linear bond continuity."""
    return lambda arr: filter.filter_linear_bond_continuity(arr)

def monoatomic_ions():
    """Select monoatomic ions."""
    return lambda arr: filter.filter_monoatomic_ions(arr)

def nucleotides():
    """Select nucleotides."""
    return lambda arr: filter.filter_nucleotides(arr)

def peptide_backbone():
    """Select peptide backbone atoms."""
    return lambda arr: filter.filter_peptide_backbone(arr)

def phosphate_backbone():
    """Select phosphate backbone atoms."""
    return lambda arr: filter.filter_phosphate_backbone(arr)

def polymer():
    """Select polymer atoms."""
    return lambda arr: filter.filter_polymer(arr)

def solvent():
    """Select solvent molecules."""
    return lambda arr: filter.filter_solvent(arr)


# ====== CURRIED 2-ARGUMENT FUNCTIONS ======
# These take one argument plus the structure (which is applied later)

def atomname(atomname):
    """Select atoms by atom name."""
    return lambda arr: atomname == arr.get_annotation("atom_name")

def chain(chain_id):
    """Select atoms by chain ID."""
    return lambda arr: chain_id == arr.get_annotation("chain_id")

def element(element_symbol):
    """Select atoms by element symbol."""
    return lambda arr: element_symbol == arr.get_annotation("element")

def inscode(inscode):
    """Select atoms by insertion code."""
    return lambda arr: inscode == arr.get_annotation("ins_code")

def resid(num):
    """Select atoms by residue ID."""
    return lambda arr: num == arr.get_annotation("res_id")

def resids(nums):
    """Select atoms by multiple residue IDs."""
    return lambda arr: np.isin(arr.get_annotation("res_id"), nums)

def resname(res_name):
    """Select atoms by residue name."""
    return lambda arr: res_name == arr.get_annotation("res_name")


# ====== NEGATED VERSIONS OF ALL FUNCTIONS ======

def not_amino_acids():
    """Select non-amino acids."""
    return lambda arr: ~amino_acids()(arr)

def not_atomname(atomname):
    """Select atoms not having the specified atom name."""
    return lambda arr: ~atomname(atomname)(arr)

def not_canonical_amino_acids():
    """Select non-canonical amino acids."""
    return lambda arr: ~canonical_amino_acids()(arr)

def not_canonical_nucleotides():
    """Select non-canonical nucleotides."""
    return lambda arr: ~canonical_nucleotides()(arr)

def not_carbohydrates():
    """Select non-carbohydrates."""
    return lambda arr: ~carbohydrates()(arr)

def not_chain(chain_id):
    """Select atoms not in the specified chain."""
    return lambda arr: ~chain(chain_id)(arr)

def not_element(element_symbol):
    """Select atoms not of the specified element."""
    return lambda arr: ~element(element_symbol)(arr)

def not_hetero():
    """Select non-hetero atoms."""
    return lambda arr: ~hetero()(arr)

def not_inscode(inscode):
    """Select atoms not having the specified insertion code."""
    return lambda arr: ~inscode(inscode)(arr)

def not_monoatomic_ions():
    """Select non-monoatomic ions."""
    return lambda arr: ~monoatomic_ions()(arr)

def not_nucleotides():
    """Select non-nucleotides."""
    return lambda arr: ~nucleotides()(arr)

def not_peptide_backbone():
    """Select non-peptide backbone atoms."""
    return lambda arr: ~peptide_backbone()(arr)

def not_phosphate_backbone():
    """Select non-phosphate backbone atoms."""
    return lambda arr: ~phosphate_backbone()(arr)

def not_polymer():
    """Select non-polymer atoms."""
    return lambda arr: ~polymer()(arr)

def not_resid(num):
    """Select atoms not in the specified residue ID."""
    return lambda arr: ~resid(num)(arr)

def not_resids(nums):
    """Select atoms not in any of the specified residue IDs."""
    return lambda arr: ~resids(nums)(arr)

def not_resname(res_name):
    """Select atoms not in residues with the specified name."""
    return lambda arr: ~resname(res_name)(arr)

def not_solvent():
    """Select non-solvent molecules."""
    return lambda arr: ~solvent()(arr)


# ====== COMBINATORS ======
# Functions to combine selections

def combine_and(*selectors):
    """Combine multiple selectors with logical AND."""
    return lambda arr: all(selector(arr) for selector in selectors)

def combine_or(*selectors):
    """Combine multiple selectors with logical OR."""
    return lambda arr: any(selector(arr) for selector in selectors)

def all_of(selectors):
    """Combine a list of selectors with logical AND."""
    return lambda arr: np.all([selector(arr) for selector in selectors], axis=0)

def any_of(selectors):
    """Combine a list of selectors with logical OR."""
    return lambda arr: np.any([selector(arr) for selector in selectors], axis=0)

def none_of(selectors):
    """Exclude atoms selected by any of the selectors."""
    return lambda arr: ~any_of(selectors)(arr)
```

Now let's update your `Prettymol` class to use these functions:

```python
class Prettymol:
    def __init__(self, array):
        self.array = array
        self.transformations = None
        self.selections = []

    def add_selection(self, selection=None, color=None, style=None, material=None):
        """
        Add selection(s) to the molecule.

        Parameters:
        - selection: A single selection function or a list of selection functions to be combined.
                     Each function should be a curried function that takes a structure and returns a mask.
        - color: Color to apply to the selection
        - style: Style to apply
        - material: Material to apply

        Returns:
        - self (for method chaining)
        """
        if selection is None:
            # No selection means select all atoms
            mask = np.ones(len(self.array), dtype=bool)
        elif isinstance(selection, list):
            # Process a list of selection functions
            if not selection:  # Empty list
                mask = np.ones(len(self.array), dtype=bool)
            else:
                # Start with all atoms selected
                mask = np.ones(len(self.array), dtype=bool)
                # Apply each selection function and combine with AND
                for sel_func in selection:
                    if callable(sel_func):
                        result = sel_func(self.array)
                        mask = mask & result
                    else:
                        raise TypeError(f"Selection must be callable, got {type(sel_func)}")
        elif callable(selection):
            # Single selection function
            mask = selection(self.array)
        else:
            raise TypeError("Selection must be a callable, a list of callables, or None")

        self.selections.append({
            'mask': mask,
            'color': color,
            'style': style,
            'material': material
        })

        return self  # Return self for method chaining

    def draw(self):
        # Apply transformations

        # Iterate through each selection
        for selection_data in self.selections:
            mask = selection_data['mask']
            color = selection_data['color']
            style = selection_data['style']
            material = selection_data['material']

            # Create a new AtomArray with the selection
            selected_atoms = self.array[mask]

            # Apply style, color, material to selected atoms
            # ... (your drawing code here)

        return self
