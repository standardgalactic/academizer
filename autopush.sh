#!/usr/bin/bash

base_directory="$PWD"  # Replace with the path to your 'Github' directory

# List of directories to process
directories=("abraxas" "alphabet" "audiobooks" "Centerfuge" "eclectric-oil" "example" "Haplopraxis/IFM" "keen-unicoder" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "psychohistory" "quantum-soup" "standardgalactic.github.io" "technobabble" "unfinished-thoughts" "xanadu" "zygomindfulness")


for dir in "${directories[@]}"; do
  cd "$base_directory/$dir" && git push
done

