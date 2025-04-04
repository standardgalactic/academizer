import bpy
import os

# Get the user scripts path and define the fonts folder
user_script_path = bpy.utils.script_path_user()
fonts_folder = os.path.join(user_script_path, "fonts")

# List all .ttf files in the fonts folder, excluding ones with "dactyl" or "lingojam" in the filename
font_files = [f for f in os.listdir(fonts_folder) 
              if f.lower().endswith('.ttf') and 'dactyl' not in f.lower() and 'lingojam' not in f.lower()]

if not font_files:
    print("No .ttf font files found in", fonts_folder)
else:
    print("Found", len(font_files), "fonts (excluding Dactyl and Lingojam Cipher).")

# Settings for a single column layout
spacing_y = 10.0  # vertical spacing between samples

# Sample sentence to display with each font
sample_sentence = "The quick brown fox jumps over the lazy dog."

# Create a new collection for our font samples
collection_name = "FontSamples"
if collection_name in bpy.data.collections:
    collection = bpy.data.collections[collection_name]
else:
    collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(collection)

# Optional: Remove existing objects in the collection
for obj in list(collection.objects):
    bpy.data.objects.remove(obj, do_unlink=True)

# Loop through the font files and create text objects in one column
for idx, font_file in enumerate(font_files):
    # Construct the full path to the font file
    font_path = os.path.join(fonts_folder, font_file)
    
    # Load the font (or get it if already loaded)
    try:
        font_loaded = bpy.data.fonts.load(font_path, check_existing=True)
    except Exception as e:
        print(f"Could not load {font_file}: {e}")
        continue

    # Use the filename (without extension) as the font name
    font_name = os.path.splitext(font_file)[0]
    
    # Create a new text curve data block with two lines:
    # one with the font name and another with the sample sentence.
    text_data = bpy.data.curves.new(name=font_name, type='FONT')
    text_data.body = f"{font_name}\n{sample_sentence}"
    
    # Set the loaded font to the text data
    text_data.font = font_loaded
    text_data.align_x = 'CENTER'
    
    # Create a new text object using the text data
    text_obj = bpy.data.objects.new(name=font_name, object_data=text_data)
    
    # Position the text objects in one column along the Y axis
    text_obj.location = (0, idx * spacing_y, 0)
    
    # Optionally adjust the text size
    text_data.size = 1.0
    
    # Link the text object to our collection
    collection.objects.link(text_obj)

print("Created", len(font_files), "font sample objects in collection", collection_name)

