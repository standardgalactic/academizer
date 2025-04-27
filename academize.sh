#!/usr/bin/bash

# Handle Control-C (SIGINT)
trap 'echo "Script interrupted"; exit' SIGINT

# Check if current directory is 'Github'
current_directory=$(basename "$PWD")
if [ "$current_directory" != "GitHub" ]; then
    echo "This script must be run from the 'Github' directory. Aborting."
    exit 1
fi

# Base directory is the current directory
base_directory="$PWD"

# List of directories to process
directories=(
"abraxas" "agora" "arcanum" "alphabet" "antivenom" "backward-compatibility" "brain" "bubble-city" "capstone" "Centerfuge" "circle-of-fifths" "codex" "cogniscium" "eclectric-oil" "example" "experiments" "ensign" "Haplopraxis/IFM" "hepastitium"  "human" "hyperspace" "keen-unicoder" "keyboard" "kitbash" "library" "logical-connectives" "lorax" "mindgame" "mirror" "negentropy" "phonograph" "pacer" "prototypes" "psychohistory" "quadrivium"
"quantum-soup" "umbilicus" "secret-message"  "sitemap" "spherepop" "standardgalactic.github.io" "substrate" "supercube" "systada" "technobabble" "teleosemantics" "terminal-simulator" "theory" "transcript" "unscannable-interfaces" "vectorspace" "xanadu" "zetetics" "zygomindfulness" "xylomancy"
)

# Loop through each specified directory
for dir in "${directories[@]}"; do
    echo "-----------------------------------------"
    echo "Starting processing for directory: $dir"
    sleep 1 # 2-second delay

    # Full path to the directory
    full_path="$base_directory/$dir"

    # Check if directory exists
    if [ -d "$full_path" ]; then
        echo "Directory exists: $full_path"
        sleep 1

        cd "$full_path" || exit
        echo "Changed directory to $full_path"
        sleep 1

        primary_branch=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
        echo "Primary branch for $dir is $primary_branch"
        sleep 1

        git pull origin "$primary_branch"
        echo "Git pull completed on $primary_branch"
        sleep 1

#        git add .
#        echo "Git add completed"
#        sleep 1

#        git commit -m "Imported from $dir"
#        echo "Git commit completed"
#        sleep 1

        # Uncomment the next line to enable git push
        # git push origin "$primary_branch"
        # echo "Git push completed on $primary_branch"
        # sleep 1
    else
        echo "Directory $full_path does not exist"
        sleep 1
    fi

    echo "Finished processing for directory: $dir"
    sleep 1
done

echo "Script completed."
