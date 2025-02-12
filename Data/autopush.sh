#!/usr/bin/bash

base_directory="$PWD"  # Replace with the path to your 'Github' directory

# List of directories to process
directories=("agora" "abraxas" "alphabet" "audiobooks" "Centerfuge" "eclectric-oil" "example" "Haplopraxis/IFM" "keen-unicoder" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "prototypes" "psychohistory" "quantum-soup" "standardgalactic.github.io" "technobabble" "unfinished-thoughts" "unscannable-intefaces" "substrate" "xanadu" "zygomindfulness")


for dir in "${directories[@]}"; do
  cd "$base_directory/$dir" && git push
done

