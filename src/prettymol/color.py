from biotite.structure import AtomArray
# from molecularnodes.color import color_from_atomic_number, color_from_element, colors_from_elements, color_chains, color_chains_equidistant
from molecularnodes.color import (
    color_from_atomic_number,
    color_from_element,
    colors_from_elements,
    color_chains_equidistant,
    color_chains,
    iupac_colors_rgb
)

import numpy as np


class ColorArray(AtomArray):
    def __init__(self, atom_array: AtomArray):
        """
        Initialize a ColorArray from an existing AtomArray.

        Parameters
        ----------
        atom_array : AtomArray
            The atom array to be converted into a ColorArray
        """
        super().__init__(len(atom_array))

        # Copy all annotations and coordinates from the input array
        for annot in atom_array.get_annotation_categories():
            self.set_annotation(annot, atom_array.get_annotation(annot))
        self.coord = atom_array.coord.copy()

        # Add color annotation
        self.add_annotation("color", dtype=object)

    def color_by_element(self):
        """
        Assigns colors to atoms based on their chemical elements using IUPAC colors.
        """
        atomic_numbers = np.array([atomic_number_map.get(elem, 0) for elem in self.element])
        element_colors = colors_from_elements(atomic_numbers)
        element_colors[:, 3] = 1.0
        self.set_annotation("Color", element_colors)

    def color_by_chain(self):
        """
        Assigns colors to atoms based on their chain IDs using equidistant colors.
        """
        chain_colors = color_chains_equidistant(self.chain_id)
        chain_colors[:, 3] = 1.0
        self.set_annotation("Color", chain_colors)

    def color_by_chain_and_element(self):
        """
        Assigns colors to atoms based on both chain IDs and elements.
        Carbon atoms are colored by chain, other elements by their element color.
        """
        atomic_numbers = np.array([atomic_number_map.get(elem, 0) for elem in self.element])
        colors = color_chains(atomic_numbers, self.chain_id)
        colors[:, 3] = 1.0
        self.set_annotation("Color", colors)

    def set_custom_colors(self, colors: np.ndarray):
        """
        Sets custom colors for the atoms.

        Parameters
        ----------
        colors : np.ndarray
            Array of RGBA colors with shape (n_atoms, 4)
        """
        if len(colors) != len(self):
            raise ValueError("Colors array must have the same length as the atom array")
        if colors.shape[1] != 4:
            raise ValueError("Colors must be RGBA values (shape: n_atoms x 4)")
        self.set_annotation("Color", colors)

    def get_colors(self) -> np.ndarray:
        """
        Returns the current color array.

        Returns
        -------
        np.ndarray
            Array of RGBA colors for each atom
        """
        return self.get_annotation("Color")

# Create atomic number mapping
atomic_number_map = {
    element: i+1 for i, element in enumerate(iupac_colors_rgb.keys())
}
