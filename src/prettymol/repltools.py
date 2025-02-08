#
# repltools is the class for all repl-related utlity functions
#
import bpy
import mathutils

class repltools():
    def __init__(self):
        self.setup_compositing()
        self._orientation = None
        self._view = None

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

        # print("\n=== INPUT SOCKETS ===")
        # for input in glare_node.inputs:
        #     print(f"Name: {input.name}")
        #     print(f"Type: {input.type}")
        #     print(f"Default Value: {input.default_value}")
        #     print("---")
        #
        # # Print Output Sockets
        # print("\n=== OUTPUT SOCKETS ===")
        # for output in glare_node.outputs:
        #     print(f"Name: {output.name}")
        #     print(f"Type: {output.type}")
        #     print("---")
        #
        # bloom_types =  ['BLOOM', 'GHOSTS', 'STREAKS', 'FOG_GLOW', 'SIMPLE_STAR']
        # for bt in bloom_types:
        #     glare_node.glare_type = bt
        #
        #     print("\n=== Glare Type  ===")
        #     print(f"{glare_node.glare_type}")
        #
        #     print(f"\n=== Settable Properties for Glare Type: {glare_node.glare_type} ===")
        #     for prop in glare_node.bl_rna.properties:
        #         if not prop.is_readonly:
        #             try:
        #                 value = getattr(glare_node, prop.identifier)
        #                 print(f"Property: {prop.identifier}")
        #                 print(f"Current Value: {value}")
        #                 print(f"Type: {prop.type}")
        #                 print("---")
        #             except AttributeError:
        #                 pass

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

            # Convert matrix to list of vectors
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
