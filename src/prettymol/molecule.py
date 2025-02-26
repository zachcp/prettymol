# shim for
import uuid
import bpy
from molecularnodes.session import MNSession
from molecularnodes.entities.molecule.base import Molecule
from molecularnodes.entities.molecule.pdb import _comp_secondary_structure
from molecularnodes.entities.base import EntityType
from biotite.structure import AtomArray

class Molecule2(Molecule):
    def __init__(self, *args, **kwargs):
        # super().__init__(file_path="UNUSED_TEST.pdb")
        self._entity_type = EntityType.MOLECULE
        self._uuid = str(uuid.uuid1())

    @classmethod
    def from_array(cls, array: AtomArray, name: str = "FromArray"):
        instance = cls()  # Create a new instance
        instance.file = "ARRAY_LOADED_DIRECTLY"
        instance._frames_collection = None
        instance._entity_type = EntityType.MOLECULE
        instance._assemblies = lambda : None #
        instance._uuid = str(uuid.uuid1())
        instance.array = instance._validate_structure_array(array)
        instance.n_atoms = instance.array.array_length()
        # from Molecular entity Init
        # bpy.context.scene.MNSession.register_entity(instance)
        #instance.create_object(name=name)
        return instance  # Return the new instance

    def _validate_structure_array(self, array: AtomArray):
        sec_struct = _comp_secondary_structure(array)
        array.set_annotation("sec_struct", sec_struct)
        return array
