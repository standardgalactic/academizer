#!/usr/bin/bash
set -e
set -x

# Base directory where the repositories are located
base_directory="$PWD"

# Directory to copy files into (the 'academizer' repository)
academizer_directory="$base_directory/academizer"

# List of directories to process
directories=("abraxas" "agora" "alphabet" "brain" "audiobooks" "Centerfuge" "eclectric-oil" "library" "example" "Haplopraxis/IFM" "keen-unicoder" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "prototypes" "psychohistory" "quantum-soup" "standardgalactic.github.io" "technobabble" "unfinished-thoughts" "unscannable-interfaces" "substrate" "systada" "xanadu" "zygomindfulness")

# Loop through each specified directory
for dir in "${directories[@]}"; do
    echo "Processing $dir"

    # Full path to the source directory
    full_path="$base_directory/$dir"

    # Check if directory exists
    if [ -d "$full_path" ]; then
        echo "Checking for files in $full_path"
        
        # Check if there are files to copy
        if compgen -G "$full_path/*.mhtml" > /dev/null || compgen -G "$full_path/*.html" > /dev/null || compgen -G "$full_path/*.txt" > /dev/null; then
            echo "Copying files from $dir to academizer"
            
            # Copy .mhtml, .html, and .txt files to academizer only if they don't exist or are newer
            cp -vu "$full_path"/*.mhtml "$full_path"/*.html "$full_path"/*.txt "$academizer_directory"

            # Change directory to academizer
            cd "$academizer_directory" || exit

            # Add all changes to git
            git add .

            # Commit the changes with a message indicating which directory the files came from
            git commit -m "Imported files from $dir"

            echo "Acknowledging $dir"
            sleep 2 

            # Push the changes to the remote repository
            git push

            # Return to the base directory
            cd "$base_directory" || exit
        else
            echo "No files to copy in $dir"
        fi
    else
        echo "Directory $full_path does not exist"
    fi
done

