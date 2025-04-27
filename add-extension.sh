#!/bin/bash

# Loop through all files in the current directory
for file in *; do
# Check if it's a file and doesn't already have an extension
if [ -f "$file" ] && [[ "$file" != *.* ]]; then
mv "$file" "$file.mhtml"
echo "Renamed $file to $file.mhtml"
fi
done
