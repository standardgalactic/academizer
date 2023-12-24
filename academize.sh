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
directories=("alphabet" "audiobooks" "Centerfuge" "eclectric-oil" "example" "Haplopraxis/IFM" "keen-unicoder" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "psychohistory" "quantum-soup" "standardgalactic.github.io" "technobabble" "unfinished-thoughts" "substrate" "xanadu" "zygomindfulness")

# Loop through each specified directory
for dir in "${directories[@]}"; do
    echo "-----------------------------------------"
    echo "Starting processing for directory: $dir"
    sleep 5 # 5-second delay

    # Full path to the directory
    full_path="$base_directory/$dir"

    # Check if directory exists
    if [ -d "$full_path" ]; then
        echo "Directory exists: $full_path"
        sleep 5

        cd "$full_path" || exit
        echo "Changed directory to $full_path"
        sleep 5

        primary_branch=$(git symbolic-ref refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
        echo "Primary branch for $dir is $primary_branch"
        sleep 5

        git pull origin "$primary_branch"
        echo "Git pull completed on $primary_branch"
        sleep 5

        git add .
        echo "Git add completed"
        sleep 5

        git commit -m "Imported from $dir"
        echo "Git commit completed"
        sleep 5

        # Uncomment the next line to enable git push
        # git push origin "$primary_branch"
        # echo "Git push completed on $primary_branch"
        # sleep 5
    else
        echo "Directory $full_path does not exist"
        sleep 5
    fi

    echo "Finished processing for directory: $dir"
    sleep 5
done

echo "Script completed."
