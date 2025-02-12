#!/usr/bin/bash

# Base directory where the repositories are located
base_directory="$PWD"

# Directory to copy files into (the 'academizer' repository)
academizer_directory="/mnt/c/Users/Mechachleopteryx/OneDrive/Documents/Github/academizer"

# List of directories to process
directories=("agora" "alphabet" "audiobooks" "Centerfuge" "eclectric-oil" "example" "Haplopraxis/IFM" "keen-unicoder" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "prototypes" "psychohistory" "quantum-soup" "standardgalactic.github.io" "technobabble" "unfinished-thoughts" "unscannable-interfaces" "substrate" "xanadu" "zygomindfulness")


# Loop through each specified directory
for dir in "${directories[@]}"; do
  echo "Processing $dir"

          # Full path to the source directory
          full_path="$base_directory/$dir"

                  # Check if directory exists
                  if [ -d "$full_path" ]; then
                    # Copy .mhtml, .html, and .txt files to
                    # academizer
                    cp "$full_path"/*.mhtml "$full_path"/*.html "$full_path"/*.txt "$academizer_directory"

                                                # Change directory to
                                                # academizer
                          cd "$academizer_directory" || exit

                                                                # Remove duplicate files with no extension 
                                                                for file in *.mhtml; do base=$(basename "$file" .mhtml); find . -maxdepth 1 -type f -name "$base*" ! -name "*.mhtml" -exec rm -f {} \;; done

                                                                # all
                                                                # changes
                                                                # to git
                                                                git add .

                                                                                # Commit the changes with a message
                                                                                git commit -m "Imported from $dir"

                                                                                echo "Acknowledging $dir" 
                                                                                sleep 2 

                                                                                                    # Uncomment the next line to enable
                                                                                                    # git push
                                                                                                    git push
                                                                                                  else
                                                                                                    echo "Directory $full_path does not exist"
                  fi
                done


