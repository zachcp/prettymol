#
# repltools is the class for all repl-related utlity functions
#
import bpy
import mathutils

class repltools():
    def __init__(self):
        self.setup_compositing()
        self._orientation = None
        self._view = self.get_view()


    def auto_view(self):
        area_type = 'VIEW_3D'
        areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        if len(areas) <= 0:
            raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

        # Select only MolecularNodes collection
        for col in bpy.data.collections:
            col.hide_viewport = True
        if "MolecularNodes" in bpy.data.collections:
            bpy.data.collections["MolecularNodes"].hide_viewport = False

        with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen
        ):
            bpy.ops.view3d.view_all()

        # Restore visibility
        for col in bpy.data.collections:
            col.hide_viewport = False

        self._view = self.get_view()
        return self

    def rotate_view(self, degrees):
        area_type = 'VIEW_3D'
        areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        if len(areas) <= 0:
            raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

        with bpy.context.temp_override(
            window=bpy.context.window,
            area=areas[0],
            region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
            screen=bpy.context.window.screen
        ):
            import math
            rads = math.radians(degrees)
            bpy.ops.view3d.rotate(angle=rads, type="ORBIT")

        self._view = self.get_view()
        return self


    def rotate_view2(self, degrees):
        import math
        area_type = 'VIEW_3D'
        areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
        if len(areas) <= 0:
            raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

        space_data = areas[0].spaces.active

        rads = math.radians(degrees)
        space_data.region_3d.view_rotation.rotate(mathutils.Euler((0.0, 0.0, rads)))

        self._view = self.get_view()
        return self

    def view_selected(self):
        # todo
        # bpy.ops.view3d.camera_to_view_selected()
        pass

    # todo allow adding other bloom types
    def setup_compositing(self):
        scene = bpy.context.scene
        if not scene.use_nodes:
            scene.use_nodes = True

        node_tree = scene.node_tree
        glare_node = node_tree.nodes.new('CompositorNodeGlare')
        render_layers = node_tree.nodes['Render Layers']
        composite = node_tree.nodes['Composite']
        glare_node.location = (render_layers.location.x + 300, render_layers.location.y)

        # bloom_types =  ['BLOOM', 'GHOSTS', 'STREAKS', 'FOG_GLOW', 'SIMPLE_STAR']
        glare_node.glare_type = "BLOOM"

        node_tree.links.new(render_layers.outputs['Image'], glare_node.inputs['Image'])
        node_tree.links.new(glare_node.outputs['Image'], composite.inputs['Image'])
        return self

    def clear(self):
        mol_collection = bpy.data.collections.get("Molecular Nodes")
        if mol_collection:
            for obj in mol_collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
        for obj in bpy.data.objects:
            if obj.type == "MESH" and obj.name != "Camera":
                bpy.data.objects.remove(obj, do_unlink=True)
        return self

    def get_view(self):
        window = bpy.context.window
        camera = bpy.context.scene.camera
        areas3d = next((area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None)
        region3d = areas3d.spaces.active.region_3d
        if areas3d:
            region = next((reg for reg in areas3d.regions if reg.type == "WINDOW"), None)
        else:
            return None

        if areas3d and region3d and camera:
            view_matrix = region3d.view_matrix
            camera_matrix = view_matrix.inverted()
            camera.matrix_world = camera_matrix
            return [list(row) for row in camera.matrix_world]
        return None


    def set_view(self, view_matrix):
        mmat = mathutils.Matrix(list(view_matrix))
        camera = bpy.context.scene.camera
        area3d = next((area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None)
        region3d = area3d.spaces.active.region_3d
        if area3d and region3d and camera:
            bpy.context.scene.camera.matrix_world = mmat
            region3d.view_matrix = mmat.inverted()
