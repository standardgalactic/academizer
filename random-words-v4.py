import bpy
import os
import random
import math
import mathutils

# -----------------------
# SETTINGS & FONT LOADING
# -----------------------

# Specify the font file name (ensure "Sga-Regular.ttf" is in your fonts folder)
font_filename = "Sga-Regular.ttf"
user_script_path = bpy.utils.script_path_user()
fonts_folder = os.path.join(user_script_path, "fonts")
font_path = os.path.join(fonts_folder, font_filename)

if not os.path.exists(font_path):
    raise Exception(f"Font file {font_filename} not found in {fonts_folder}.")

try:
    sga_font = bpy.data.fonts.load(font_path, check_existing=True)
except Exception as e:
    raise Exception(f"Error loading font {font_filename}: {e}")

print(f"Loaded font: {font_filename}")

# Define a list of words to choose from
words_list = ["Hello", "World", "Fly", "Around", "SGA", "Random", "Tunnel", "Explore", "3D", "Blender", "Design", "Art", "Python", "Code", "Font"]

# -----------------------
# ADJUSTED PARAMETERS: Scrunched Up Distribution
# -----------------------

# For random distribution, place objects within a cube (-20 to 20 units)
random_range = 20

# For the tunnel of words, use a smaller radius and Z range
tunnel_count = 50
tunnel_radius = 10.0
z_min, z_max = -20, 20
tunnel_rotations = 3

# -----------------------
# COLLECTION SETUP
# -----------------------

def get_or_create_collection(collection_name):
    if collection_name in bpy.data.collections:
        coll = bpy.data.collections[collection_name]
        # Clear existing objects in the collection
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        coll = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(coll)
    return coll

random_collection = get_or_create_collection("SGA_RandomWords")
tunnel_collection = get_or_create_collection("SGA_TunnelWords")

# -----------------------
# CREATE RANDOMLY DISTRIBUTED WORDS
# -----------------------

random_count = 100
for i in range(random_count):
    word = random.choice(words_list)
    text_data = bpy.data.curves.new(name=f"RandomText_{i}", type='FONT')
    text_data.body = word
    text_data.font = sga_font
    text_data.align_x = 'CENTER'
    
    text_obj = bpy.data.objects.new(name=f"RandomText_{i}", object_data=text_data)
    text_obj.location = (
        random.uniform(-random_range, random_range),
        random.uniform(-random_range, random_range),
        random.uniform(-random_range, random_range)
    )
    # We skip random rotations so we can use a constraint to face the camera.
    random_collection.objects.link(text_obj)

print(f"Created {random_count} random text objects in collection 'SGA_RandomWords'.")

# -----------------------
# CREATE A TUNNEL OF WORDS
# -----------------------

for i in range(tunnel_count):
    word = random.choice(words_list)
    text_data = bpy.data.curves.new(name=f"TunnelText_{i}", type='FONT')
    text_data.body = word
    text_data.font = sga_font
    text_data.align_x = 'CENTER'
    
    text_obj = bpy.data.objects.new(name=f"TunnelText_{i}", object_data=text_data)
    t = i / (tunnel_count - 1)
    z = z_min + (z_max - z_min) * t
    angle = tunnel_rotations * 2 * math.pi * t
    x = tunnel_radius * math.cos(angle)
    y = tunnel_radius * math.sin(angle)
    text_obj.location = (x, y, z)
    # Reset rotation; constraint will align it to face the camera.
    text_obj.rotation_euler = (0, 0, 0)
    
    tunnel_collection.objects.link(text_obj)

print(f"Created {tunnel_count} tunnel text objects in collection 'SGA_TunnelWords'.")

# -----------------------
# SET UP DARK BACKGROUND
# -----------------------

world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world

world.use_nodes = True
nodes = world.node_tree.nodes
bg = nodes.get("Background")
if bg:
    bg.inputs[0].default_value = (0.02, 0.02, 0.02, 1)  # Near black
    bg.inputs[1].default_value = 1.0

bpy.context.scene.render.engine = 'BLENDER_EEVEE'
print("World background set to dark.")

# -----------------------
# SET UP CAMERA
# -----------------------

# Look for an existing camera, else create one
cam = None
for obj in bpy.context.scene.objects:
    if obj.type == 'CAMERA':
        cam = obj
        break

if cam is None:
    cam_data = bpy.data.cameras.new("Camera")
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)

# A helper function to orient an object to look at a target
def look_at(obj, target):
    direction = target - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

# Initially position the camera (this will be overridden by animation keyframes)
cam.location = (0, -40, 10)
look_at(cam, mathutils.Vector((0, 0, 0)))
print("Camera set up.")

# -----------------------
# SET UP LIGHTING
# -----------------------

# Add a sun light for strong directional lighting
sun_data = bpy.data.lights.new(name="Sun", type='SUN')
sun_data.energy = 3.0
sun = bpy.data.objects.new("Sun", sun_data)
bpy.context.scene.collection.objects.link(sun)
sun.location = (0, 0, 50)

# Add a point light for fill
point_data = bpy.data.lights.new(name="Fill", type='POINT')
point_data.energy = 500
point = bpy.data.objects.new("Fill", point_data)
bpy.context.scene.collection.objects.link(point)
point.location = (20, -20, 20)
print("Lighting set up.")

# -----------------------
# ADD TRACK-TO CONSTRAINTS SO THAT ALL TEXT OBJECTS FACE THE CAMERA
# -----------------------

for coll in [random_collection, tunnel_collection]:
    for obj in coll.objects:
        # Remove existing TRACK_TO constraints if any
        for c in obj.constraints:
            if c.type == 'TRACK_TO':
                obj.constraints.remove(c)
        track = obj.constraints.new('TRACK_TO')
        track.target = cam
        # The text's local Z-axis will point toward the camera, and its local Y-axis remains up.
        track.track_axis = 'TRACK_Z'
        track.up_axis = 'UP_Y'

print("All text objects now face the camera.")

# -----------------------
# ANIMATE THE CAMERA: Fly Through the Scene
# -----------------------

# Set the timeline frame range
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 250

# Define keyframe positions for the camera.
# Adjust these positions as desired:
#   Frame 1: Far back and high above
#   Frame 125: Closer in, offset to the side
#   Frame 250: Near or even inside the wordscape
keyframes = {
    1: mathutils.Vector((0, -80, 30)),
    125: mathutils.Vector((20, -20, 10)),
    250: mathutils.Vector((0, 20, 5))
}

# Insert keyframes for camera location and rotation (oriented to always look at the scene center)
for frame, position in keyframes.items():
    bpy.context.scene.frame_set(frame)
    cam.location = position
    look_at(cam, mathutils.Vector((0, 0, 0)))
    cam.keyframe_insert(data_path="location", frame=frame)
    cam.keyframe_insert(data_path="rotation_euler", frame=frame)

print("Camera animation keyframes set.")

