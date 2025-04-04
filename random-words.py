import bpy
import os
import random
import math

# -----------------------
# SETTINGS & FONT LOADING
# -----------------------

# Specify the font file name (adjust capitalization as needed)
font_filename = "Sga-Regular.ttf"  # Ensure this file exists in your fonts folder
user_script_path = bpy.utils.script_path_user()
fonts_folder = os.path.join(user_script_path, "fonts")
font_path = os.path.join(fonts_folder, font_filename)

# Verify the font file exists
if not os.path.exists(font_path):
    raise Exception(f"Font file {font_filename} not found in {fonts_folder}.")

# Load the SGA‑Regular font (or reuse if already loaded)
try:
    sga_font = bpy.data.fonts.load(font_path, check_existing=True)
except Exception as e:
    raise Exception(f"Error loading font {font_filename}: {e}")

print(f"Loaded font: {font_filename}")

# Define a list of words to randomly choose from
words_list = ["Hello", "World", "Fly", "Around", "SGA", "Random", "Tunnel", "Explore", "3D", "Blender", "Design", "Art", "Python", "Code", "Font"]

# -----------------------
# HELPER: COLLECTION SETUP
# -----------------------

def get_or_create_collection(collection_name):
    if collection_name in bpy.data.collections:
        coll = bpy.data.collections[collection_name]
        # Clear existing objects in collection
        for obj in list(coll.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
    else:
        coll = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(coll)
    return coll

# Collection for random words
random_collection = get_or_create_collection("SGA_RandomWords")
# Collection for tunnel words
tunnel_collection = get_or_create_collection("SGA_TunnelWords")

# -----------------------
# CREATE RANDOMLY DISTRIBUTED WORDS
# -----------------------

random_count = 100  # Adjust the count if desired
for i in range(random_count):
    word = random.choice(words_list)
    # Create text curve data block
    text_data = bpy.data.curves.new(name=f"RandomText_{i}", type='FONT')
    text_data.body = word
    text_data.font = sga_font
    text_data.align_x = 'CENTER'
    
    # Create text object and assign random location and rotation
    text_obj = bpy.data.objects.new(name=f"RandomText_{i}", object_data=text_data)
    text_obj.location = (
        random.uniform(-50, 50),
        random.uniform(-50, 50),
        random.uniform(-50, 50)
    )
    text_obj.rotation_euler = (
        random.uniform(0, 2 * math.pi),
        random.uniform(0, 2 * math.pi),
        random.uniform(0, 2 * math.pi)
    )
    random_collection.objects.link(text_obj)

print(f"Created {random_count} random text objects in collection 'SGA_RandomWords'.")

# -----------------------
# CREATE A TUNNEL OF WORDS
# -----------------------

tunnel_count = 50    # Number of text objects along the tunnel
tunnel_radius = 30.0   # Radius of the tunnel circle
tunnel_rotations = 3   # Total rotations along the tunnel

for i in range(tunnel_count):
    word = random.choice(words_list)
    text_data = bpy.data.curves.new(name=f"TunnelText_{i}", type='FONT')
    text_data.body = word
    text_data.font = sga_font
    text_data.align_x = 'CENTER'
    
    text_obj = bpy.data.objects.new(name=f"TunnelText_{i}", object_data=text_data)
    
    # Parameter t goes from 0 to 1 along the tunnel
    t = i / (tunnel_count - 1)
    # z coordinate spans from -50 to 50
    z = -50 + 100 * t
    # Angle for the spiral: complete tunnel_rotations rotations
    angle = tunnel_rotations * 2 * math.pi * t
    x = tunnel_radius * math.cos(angle)
    y = tunnel_radius * math.sin(angle)
    text_obj.location = (x, y, z)
    
    # Orient the text so it faces the tunnel's center (0,0)
    # Compute the angle from the text position to the origin in the XY-plane
    face_angle = math.atan2(-y, -x)
    text_obj.rotation_euler = (0, 0, face_angle)
    
    tunnel_collection.objects.link(text_obj)

print(f"Created {tunnel_count} tunnel text objects in collection 'SGA_TunnelWords'.")

