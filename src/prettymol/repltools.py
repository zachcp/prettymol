#
# repltools is the class for all repl-related utlity functions
#
import bpy
import math
import mathutils
from .lighting import LightingCreator, BlenderLight

class Repltools():
    def __init__(self):
        self.setup_compositing()
        self.scene_clear()
        self.view_set_axis()


    def lighting_set_light(self, light: BlenderLight):
        # Clear existing lights
        for obj in bpy.data.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj, do_unlink=True)

        light_data = bpy.data.lights.new(name="Light", type = light.type)
        for property_name, value in vars(light).items():
            if hasattr(light_data, property_name):
                 setattr(light_data, property_name, value)

        light_object = bpy.data.objects.new(name="Light", object_data=light_data)
        default_collection = bpy.data.collections['Collection']
        default_collection.objects.link(light_object)

        return self


    def lighting_adjust_light_intensity(self, multiplier=1.0):
        """Adjust all light intensities by a multiplier"""
        for obj in bpy.data.objects:
            if obj.type == 'LIGHT':
                obj.data.energy *= multiplier


    def scene_clear(self):
        mol_collection = bpy.data.collections.get("Molecular Nodes")
        if mol_collection:
            for obj in mol_collection.objects:
                bpy.data.objects.remove(obj, do_unlink=True)
        for obj in bpy.data.objects:
            if obj.type == "MESH" and obj.name != "Camera":
                bpy.data.objects.remove(obj, do_unlink=True)
        return self

    def scene_clear_cache(self):
        bpy.context.view_layer.update()
        bpy.ops.outliner.orphans_purge(do_recursive=True)

        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        # for obj in bpy.data.objects:
        #     bpy.data.objects.remove(obj)

            bpy.context.view_layer.update()

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


    # def view_auto(self):
    #     area_type = 'VIEW_3D'
    #     areas = [area for area in bpy.context.window.screen.areas if area.type == area_type]
    #     if len(areas) <= 0:
    #         raise Exception(f"Make sure an Area of type {area_type} is open or visible in your screen!")

    #     # Select only MolecularNodes collection
    #     for col in bpy.data.collections:
    #         col.hide_viewport = True
    #     if "MolecularNodes" in bpy.data.collections:
    #         bpy.data.collections["MolecularNodes"].hide_viewport = False

    #     with bpy.context.temp_override(
    #         window=bpy.context.window,
    #         area=areas[0],
    #         region=[region for region in areas[0].regions if region.type == 'WINDOW'][0],
    #         screen=bpy.context.window.screen
    #     ):
    #         bpy.ops.view3d.view_all()

    #     # Restore visibility
    #     for col in bpy.data.collections:
    #         col.hide_viewport = False

    #     self._view = self.get_view()
    #     return self


    def view_auto(self):
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


    def view_get(self):
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


    def view_render(self):
        print("in the repl render_view")
        try:
            from IPython.display import Image, display
            use_ipython = True
        except NameError:
            use_ipython = False

        # Render and save the image
        bpy.context.scene.render.filepath = '/tmp/output.png'
        bpy.ops.render.render(use_viewport=True, write_still=True)

        if use_ipython:
            return display(Image('/tmp/output.png'))
        else:
            # Fallback behavior for non-IPython environments
            print("Image saved to /tmp/output.png")
            return '/tmp/output.png'

    def view_set(self, view_matrix):
        mmat = mathutils.Matrix(list(view_matrix))
        camera = bpy.context.scene.camera
        area3d = next((area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None)
        region3d = area3d.spaces.active.region_3d
        if area3d and region3d and camera:
            bpy.context.scene.camera.matrix_world = mmat
            region3d.view_matrix = mmat.inverted()


    def view_selected(self):
        # todo
        # bpy.ops.view3d.camera_to_view_selected()
        pass



    def view_set_axis(self, axis="x", distance=5):
        camera = bpy.context.scene.camera
        if camera is not None:
            match axis:
                case 'x':
                    camera.location = mathutils.Vector((distance, 0, 0))  # Move along X-axis
                case 'y':
                    camera.location = mathutils.Vector((0, distance, 0))  # Move along Y-axis
                case 'z':
                    camera.location = mathutils.Vector((0, 0, distance))  # Move along Z-axis
                case _:
                    print(f"Invalid axis: {axis}. Choose from 'x', 'y', or 'z'.")

            # Point the camera to look at the origin (0, 0, 0)
            direction = camera.location - mathutils.Vector((0, 0, 0))
            rot_quat = direction.to_track_quat('Z', 'Y')
            camera.rotation_euler = rot_quat.to_euler()
            area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
            region = next(region for region in area.regions if region.type == 'WINDOW')

            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    area.spaces[0].region_3d.view_perspective = 'CAMERA'

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



    # def lighting_set_light_color(color=(1, 1, 1, 1)):
    #     """Set color for all lights"""
    #     for obj in bpy.data.objects:
    #         if obj.type == 'LIGHT':
    #             obj.data.color = color[:3]
    #
    # def setup_ambient_occlusion():
        # """Setup ambient occlusion for better detail"""
        # bpy.context.scene.eevee.use_gtao = True
        # bpy.context.scene.eevee.gtao_distance = 0.2
        # bpy.context.scene.eevee.gtao_factor = 1.0
