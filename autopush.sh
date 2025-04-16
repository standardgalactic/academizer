#!/usr/bin/bash

base_directory="$PWD"  # Replace with the path to your 'Github' directory

# List of directories to process
directories(
"abraxas" "agora" "arcanum" "alphabet" "antivenom" "backward-compatibility" "brain" "bubble-city" "capstone" "Centerfuge" "circle-of-fifths" "cogniscium" "eclectric-oil" "example" "experiments" "ensign" "Haplopraxis/IFM" "hepastitium"  "human" "hyperspace" "keen-unicoder" "keyboard" "library" "logical-connectives" "lorax" "mindgame" "mirror" "negentropy" "phonograph" "pacer" "prototypes" "psychohistory" "quadrivium" "quantum-soup" "umbilicus" "secret-message"  "sitemap" "spherepop" "standardgalactic.github.io" "substrate" "supercube" "systada" "technobabble" "teleosemantics" "terminal-simulator" "theory" "transcript" "unscannable-interfaces" "vectorspace" "xanadu" "zetetics" "zygomindfulness" "xylomancy" 
)

for dir in "${directories[@]}"; do
  cd "$base_directory/$dir" && git push
done

