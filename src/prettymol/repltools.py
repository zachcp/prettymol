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
        self.clear()
        self._orientation = None
        self.set_view_axis()


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

    def set_view_axis(self, axis="x", distance=5):
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

    def render_view(self):
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

    def lighting_setup_three_point_lighting(self):
        # Clear existing lights
        for obj in bpy.data.objects:
            if obj.type == 'LIGHT':
                bpy.data.objects.remove(obj)

        # Key Light (main light)
        key_light = bpy.data.lights.new(name="Key_Light", type='AREA')
        key_light.energy = 1000
        key_light.size = 5
        key_light_obj = bpy.data.objects.new(name="Key_Light", object_data=key_light)
        bpy.context.scene.collection.objects.link(key_light_obj)
        key_light_obj.location = (6, -4, 8)
        key_light_obj.rotation_euler = (0.5, 0.2, -0.3)

        # Fill Light
        fill_light = bpy.data.lights.new(name="Fill_Light", type='AREA')
        fill_light.energy = 500
        fill_light.size = 5
        fill_light_obj = bpy.data.objects.new(name="Fill_Light", object_data=fill_light)
        bpy.context.scene.collection.objects.link(fill_light_obj)
        fill_light_obj.location = (-6, 2, 3)
        fill_light_obj.rotation_euler = (0.3, -0.2, 0.5)

        # Back Light
        back_light = bpy.data.lights.new(name="Back_Light", type='AREA')
        back_light.energy = 750
        back_light.size = 5
        back_light_obj = bpy.data.objects.new(name="Back_Light", object_data=back_light)
        bpy.context.scene.collection.objects.link(back_light_obj)
        back_light_obj.location = (-2, -6, 5)
        back_light_obj.rotation_euler = (0.7, -0.2, -2.0)

    def lighting_setup_hdri_lighting(self):
        # Set up world node tree
        world = bpy.context.scene.world
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links

        # Clear existing nodes
        nodes.clear()

        # Add nodes
        node_background = nodes.new('ShaderNodeBackground')
        node_environment = nodes.new('ShaderNodeTexEnvironment')
        node_mapping = nodes.new('ShaderNodeMapping')
        node_tex_coord = nodes.new('ShaderNodeTexCoord')
        node_output = nodes.new('ShaderNodeOutputWorld')

        # Link nodes
        links.new(node_tex_coord.outputs['Generated'], node_mapping.inputs['Vector'])
        links.new(node_mapping.outputs['Vector'], node_environment.inputs['Vector'])
        links.new(node_environment.outputs['Color'], node_background.inputs['Color'])
        links.new(node_background.outputs['Background'], node_output.inputs['Surface'])

        # Adjust world strength
        node_background.inputs['Strength'].default_value = 1.0

    def lighting_setup_rim_lighting(self):
        # Create rim lights
        for i in range(8):
            angle = i * (360/8)
            x = 6 * math.cos(math.radians(angle))
            y = 6 * math.sin(math.radians(angle))

            rim_light = bpy.data.lights.new(name=f"Rim_Light_{i}", type='AREA')
            rim_light.energy = 200
            rim_light.size = 2
            rim_light_obj = bpy.data.objects.new(name=f"Rim_Light_{i}", object_data=rim_light)
            bpy.context.scene.collection.objects.link(rim_light_obj)
            rim_light_obj.location = (x, y, 3)
            rim_light_obj.rotation_euler = (0.5, 0, math.radians(angle + 180))

    def lighting_setup_volumetric_lighting(self):
        # Set up volumetric lighting
        bpy.context.scene.eevee.use_volumetric_lights = True
        bpy.context.scene.eevee.volumetric_samples = 64

        # Create a strong spot light
        spot = bpy.data.lights.new(name="Volumetric_Spot", type='SPOT')
        spot.energy = 5000
        spot.spot_size = math.radians(30)
        spot.spot_blend = 0.5
        spot_obj = bpy.data.objects.new(name="Volumetric_Spot", object_data=spot)
        bpy.context.scene.collection.objects.link(spot_obj)
        spot_obj.location = (5, -5, 8)
        spot_obj.rotation_euler = (0.9, 0.2, -0.6)


    def lighting_setup_scientific_lighting(self):
        # Main top light
        top_light = bpy.data.lights.new(name="Top_Light", type='SUN')
        top_light.energy = 5
        top_light_obj = bpy.data.objects.new(name="Top_Light", object_data=top_light)
        bpy.context.scene.collection.objects.link(top_light_obj)
        top_light_obj.rotation_euler = (0, 0, 0)

        # Ambient light spheres
        for i in range(6):
            for j in range(3):
                angle = i * (360/6)
                z = 3 * (j - 1)
                x = 8 * math.cos(math.radians(angle))
                y = 8 * math.sin(math.radians(angle))

                amb_light = bpy.data.lights.new(name=f"Ambient_{i}_{j}", type='POINT')
                amb_light.energy = 100
                amb_light_obj = bpy.data.objects.new(name=f"Ambient_{i}_{j}", object_data=amb_light)
                bpy.context.scene.collection.objects.link(amb_light_obj)
                amb_light_obj.location = (x, y, z)

    def lighting_adjust_light_intensity(self, multiplier=1.0):
        """Adjust all light intensities by a multiplier"""
        for obj in bpy.data.objects:
            if obj.type == 'LIGHT':
                obj.data.energy *= multiplier

    def clear_cache(self):
        bpy.context.view_layer.update()
        bpy.ops.outliner.orphans_purge(do_recursive=True)

        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        # for obj in bpy.data.objects:
        #     bpy.data.objects.remove(obj)

        bpy.context.view_layer.update()

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
