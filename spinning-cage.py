import bpy
import math

# --- World Setup: Set background to black ---
if bpy.context.scene.world:
    bpy.context.scene.world.use_nodes = True
    bg = bpy.context.scene.world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs[0].default_value = (0, 0, 0, 1)  # Pure black

# --- Create Nested Spheres with Wireframe Modifiers and Rotation ---
num_spheres = 10
base_radius = 2.0
radius_step = 0.15  # Each sphere gets slightly smaller
base_speed = 1      # Base rotation speed multiplier

for i in range(num_spheres):
    # Calculate sphere radius
    radius = base_radius - i * radius_step
    
    # Add a UV sphere at the origin
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
    sphere = bpy.context.active_object
    sphere.name = f"Sphere_{i}"
    
    # Add a Wireframe modifier for a web-like filament appearance
    wire_mod = sphere.modifiers.new(name="Wireframe", type='WIREFRAME')
    wire_mod.thickness = 0.02  # Tweak thickness as desired
    
    # Create a material with a slight transparency (adjust Transmission if needed)
    mat = bpy.data.materials.new(name=f"Material_{i}")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)  # White
        bsdf.inputs["Transmission"].default_value = 0.8         # Slight transparency
        bsdf.inputs["Roughness"].default_value = 0.1
    sphere.data.materials.append(mat)
    
    # Set up rotation animation (keyframes at frame 1 and 250)
    sphere.rotation_mode = 'XYZ'
    sphere.rotation_euler = (0, 0, 0)
    sphere.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # Rotate around Z-axis by an amount proportional to the sphere index
    rotation_amount = (i + 1) * 2 * math.pi  # Full rotations
    sphere.rotation_euler = (0, 0, rotation_amount)
    sphere.keyframe_insert(data_path="rotation_euler", frame=250)
    
    # Set keyframe interpolation to linear for constant rotation speed
    action = sphere.animation_data.action
    for fcurve in action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = 'LINEAR'

# --- Create a Starfield Background using a Large Enclosing Sphere ---
bpy.ops.mesh.primitive_uv_sphere_add(radius=100, location=(0, 0, 0))
star_sphere = bpy.context.active_object
star_sphere.name = "Starfield"

# Flip the sphere normals so that the texture is visible from the inside
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.flip_normals()
bpy.ops.object.mode_set(mode='OBJECT')

# Create a new material for the starfield
star_mat = bpy.data.materials.new(name="StarfieldMaterial")
star_mat.use_nodes = True
nodes = star_mat.node_tree.nodes
links = star_mat.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

# Create an Emission node (for a self-lit starfield)
emission = nodes.new(type="ShaderNodeEmission")
emission.inputs["Strength"].default_value = 1.5

# Create a Noise Texture to generate a random star pattern
noise = nodes.new(type="ShaderNodeTexNoise")
noise.inputs["Scale"].default_value = 500.0

# Use a ColorRamp to threshold the noise into star-like white specks against black
color_ramp = nodes.new(type="ShaderNodeValToRGB")
color_ramp.color_ramp.elements[0].position = 0.98
color_ramp.color_ramp.elements[1].position = 1.0
color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

# Material output node
material_output = nodes.new(type="ShaderNodeOutputMaterial")

# Connect the nodes: noise -> color ramp -> emission color, then to material output
links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
links.new(color_ramp.outputs["Color"], emission.inputs["Color"])
links.new(emission.outputs["Emission"], material_output.inputs["Surface"])

# Assign the starfield material to the starfield sphere
star_sphere.data.materials.append(star_mat)

# Optionally, prevent the starfield sphere from casting shadows
star_sphere.cycles_visibility.shadow = False
