import bpy
import os

# Get the user scripts directory path
user_script_path = bpy.utils.script_path_user()
print("User script path:", user_script_path)

# Define the path to your fonts folder (assuming it's in the user scripts directory)
fonts_folder = os.path.join(user_script_path, "fonts")
print("Fonts folder path:", fonts_folder)

# Check if the folder exists and list its contents
if os.path.isdir(fonts_folder):
    print("Fonts folder found. Contents:")
    for file in os.listdir(fonts_folder):
        print(" -", file)
else:
    print("Fonts folder not found.")

