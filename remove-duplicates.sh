#!/bin/bash

# Directory to search for duplicate files
directory="./"

# Find and remove all files that end with "(1).txt"
find "$directory" -type f -name "* (1).pdf" -exec rm -f {} \;

echo "All duplicate files with (1).pdf ending have been removed."

