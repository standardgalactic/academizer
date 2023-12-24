#!/usr/bin/bash

# Base directory where the repositories are located
base_directory="$PWD"

# Directory to copy files into (the 'academizer' repository)
academizer_directory="/mnt/c/Users/Mechachleopteryx/OneDrive/Documents/Github/academizer"

# List of directories to process
directories=("abraxas" "alphabet" "audiobooks" "autodoxx" "Centerfuge" "eclectric-oil" "example" "Haplopraxis/IFM" "keen-unicoder" "library" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "psychohistory" "quantum-soup" "standardgalactic.github.io" "substrate" "technobabble" "unfinished-thoughts" "xanadu" "zygomindfulness")


# Loop through each specified directory
for dir in "${directories[@]}"; do
echo "Processing $dir"

# Full path to the source directory
full_path="$base_directory/$dir"

# Check if directory exists
if [ -d "$full_path" ]; then
# Copy .mhtml, .html, .pdf, and .txt files to academizer
cp "$full_path"/*.mhtml "$full_path"/*.html "$full_path"/*.pdf "$full_path"/*.txt "$academizer_directory"

# Change directory to academizer
cd "$academizer_directory" || exit

# Add all changes to git
git add .

# Commit the changes with a message
git commit -m "Imported from $dir"

echo "Acknowledging $dir" 
sleep 5

# Uncomment the next line to enable git push
git push
  else
    echo "Directory $full_path does not exist"
  fi
done



