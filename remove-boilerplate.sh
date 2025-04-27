#!/bin/bash

# This script renames all .txt files in the current directory,
# removing the substring " ( PDFDrive )" using sed for pattern
# replacement.

for file in *.pdf; do
# Use sed to remove the substring " ( PDFDrive )"
newfile=$(echo "$file" | sed 's/ ( PDFDrive )//g')
# Only rename if the name has changed.
if [[ "$file" != "$newfile" ]]; then
  echo "Renaming: '$file' -> '$newfile'"
  mv "$file" "$newfile"
fi
done

