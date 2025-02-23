#!/usr/bin/bash

base_directory="$PWD"  # Replace with the path to your 'Github' directory

# List of directories to process
directories("abraxas" "agora" "alphabet" "arcanum" "backward-compatibility" "brain" "Centerfuge" "cogniscium" "eclectric-oil" "example"          "experiments" "Haplopraxis/IFM" "human" "hyperspace" "keen-unicoder" "library" "logical-connectives" "mindgame" "mirror"              "negentropy" "phonograph" "prototypes" "psychohistory" "quadrivium" "quantum-soup" "umbilicus" "secret-message" "sitemap"             "standardgalactic.github.io" "substrate" "supercube" "systada" "technobabble" "theory" "transcript" "unscannable-interfaces"          "vectorspace" "xanadu" "xylomancy" "zygomindfulness")


for dir in "${directories[@]}"; do
  cd "$base_directory/$dir" && git push
done

