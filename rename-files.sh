#!/bin/bash

# Set the prefix for renamed files
prefix="capstone-"

# Counter for numbering files
count=1

# Find and sort image files while handling spaces and parentheses
for file in image\ \(*\).webp; do
    # Check if file exists to avoid glob issues
    [ -e "$file" ] || continue
    
    # Generate new filename with padded number
    new_name=$(printf "%s%02d.webp" "$prefix" "$count")
    
    # Rename the file
    mv -- "$file" "$new_name"
    
    # Increment counter
    ((count++))
done

# Rename 'image.webp' separately if it exists
if [[ -f "image.webp" ]]; then
    new_name=$(printf "%s%02d.webp" "$prefix" "$count")
    mv -- "image.webp" "$new_name"
fi

echo "Renaming complete."

