import numpy as np
from biotite.structure import filter



class StructureSelector:
    """
    example = StructureSelector(structure)
            .resid(10)
            .resname("ALA")
            .chain("A")
            .get_selection())
    """
    def __init__(self, structure):
        self.structure = structure
        self.mask = None

    def _update_mask(self, new_mask):
        self.mask = new_mask if self.mask is None else (self.mask & new_mask)
        return self

    def amino_acids(self):
        return self._update_mask(select_amino_acids(self.structure))

    def atomname(self, atomname):
        return self._update_mask(select_atomname(self.structure, atomname))

    def canonical_amino_acids(self):
        return self._update_mask(select_canonical_amino_acids(self.structure))

    def canonical_nucleotides(self):
        return self._update_mask(select_canonical_nucleotides(self.structure))

    def carbohydrates(self):
        return self._update_mask(select_carbohydrates(self.structure))

    def chain(self, chain_id):
        return self._update_mask(select_chain(self.structure, chain_id))

    def element(self, element):
        return self._update_mask(select_element(self.structure, element))

    def first_altloc(self):
        return self._update_mask(select_first_altloc(self.structure))

    def get_mask(self):
        return self.mask

    def get_selection(self):
        """Returns the structure filtered by the current mask"""
        if self.mask is None:
            return self.structure
        return self.structure[self.mask]

    def hetero(self):
        return self._update_mask(select_hetero(self.structure))

    def highest_occupancy_altloc(self):
        return self._update_mask(select_highest_occupancy_altloc(self.structure))

    def inscode(self, inscode):
        return self._update_mask(select_inscode(self.structure, inscode))

    def intersection(self):
        return self._update_mask(select_intersection(self.structure))

    def linear_bond_continuity(self):
        return self._update_mask(select_linear_bond_continuity(self.structure))

    def monoatomic_ions(self):
        return self._update_mask(select_monoatomic_ions(self.structure))

    def nucleotides(self):
        return self._update_mask(select_nucleotides(self.structure))

    def peptide_backbone(self):
        return self._update_mask(select_peptide_backbone(self.structure))

    def phosphate_backbone(self):
        return self._update_mask(select_phosphate_backbone(self.structure))

    def polymer(self):
        return self._update_mask(select_polymer(self.structure))

    def resid(self, num):
        return self._update_mask(select_resid(self.structure, num))

    def resids(self, nums):
        return self._update_mask(select_resids(self.structure, nums))

    def resname(self, res_name):
        return self._update_mask(select_resname(self.structure, res_name))

    def solvent(self):
        return self._update_mask(select_solvent(self.structure))



def select_amino_acids(arr):
    return filter.filter_amino_acids(arr)

def select_atomname(arr, atomname):
    return atomname == arr.get_annotation("atom_name")

def select_canonical_amino_acids(arr):
    return filter.filter_canonical_amino_acids(arr)

def select_canonical_nucleotides(arr):
    return filter.filter_canonical_nucleotides(arr)

def select_carbohydrates(arr):
    return filter.filter_carbohydrates(arr)

def select_chain(arr, chain):
    return chain == arr.get_annotation("chain_id")

def select_element(arr, element):
    return element == arr.get_annotation("element")

def select_first_altloc(arr):
    return filter.filter_first_altloc(arr)

def select_hetero(arr):
    return True == arr.get_annotation("hetero")

def select_highest_occupancy_altloc(arr):
    return filter.filter_highest_occupancy_altloc(arr)

def select_inscode(arr, inscode):
    return inscode == arr.get_annotation("ins_code")

def select_intersection(arr):
    return filter.filter_intersection(arr)

def select_linear_bond_continuity(arr):
    return filter.filter_linear_bond_continuity(arr)

def select_monoatomic_ions(arr):
    return filter.filter_monoatomic_ions(arr)

def select_nucleotides(arr):
    return filter.filter_nucleotides(arr)

def select_peptide_backbone(arr):
    return filter.filter_peptide_backbone(arr)

def select_phosphate_backbone(arr):
    return filter.filter_phosphate_backbone(arr)

def select_polymer(arr):
    return filter.filter_polymer(arr)

def select_resid(arr, num):
    return num == arr.get_annotation("res_id")

def select_resids(arr, nums):
    return np.isin(arr.get_annotation("res_id"), nums)

def select_resname(arr, res_name):
    return res_name == arr.get_annotation("res_name")

def select_solvent(arr):
    return filter.filter_solvent(arr)
