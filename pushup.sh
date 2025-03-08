#!/usr/bin/env bash

# Base directory where the repositories are located
base_directory="$PWD"

# Directory to copy files into (the 'academizer' repository)
academizer_directory="$base_directory/academizer"

# List of directories to process (full list restored)
directories=(
"abraxas" "agora" "arcanum" "alphabet" "antivenom" "backward-compatibility" "brain" "bubble-city" "capstone" "Centerfuge" "cogniscium" "eclectric-oil" "example" "experiments" "ensign" "Haplopraxis/IFM" "hepastitium"  "human" "hyperspace" "keen-unicoder" "library" "logical-connectives" "mindgame" "mirror" "negentropy" "phonograph" "pacer" "prototypes" "psychohistory" "quadrivium"
"quantum-soup" "umbilicus" "secret-message"  "sitemap" "spherepop" "standardgalactic.github.io" "substrate" "supercube" "systada" "technobabble" "terminal-simulator" "theory" "transcript" "unscannable-interfaces" "vectorspace" "xanadu" "xylomancy" "zygomindfulness"
)

# File extensions to process
extensions=("mhtml" "html" "txt" "py" "sh")

# Only these .txt filenames should get "(1)", "(2)" suffixes:
special_txt_files=("summaries" "file-list" "summary" "overview" "detailed-overview")

# ---------------------------------------------------
# COPY-WITH-SUFFIX FUNCTION
# ---------------------------------------------------
# Used ONLY for certain .txt files in "special_txt_files".
copy_with_suffix_if_exists() {
    local src_file="$1"
    local dest_dir="$2"

    local filename
    filename="$(basename "$src_file")"

    local base="${filename%.*}"     # e.g. "summary" if it's "summary.txt"
    local ext="${filename##*.}"     # e.g. "txt"
    
    if [ "$ext" = "$filename" ]; then
        # If there's no ".", $ext will be the entire filename
        ext=""
    fi

    local dest_file="$dest_dir/$filename"

    # If file already exists, append (1), (2), ...
    if [ -f "$dest_file" ]; then
        local count=1
        local new_filename
        if [ -n "$ext" ] && [ "$ext" != "$filename" ]; then
            new_filename="${base} (${count}).${ext}"
        else
            new_filename="${base} (${count})"
        fi

        while [ -f "$dest_dir/$new_filename" ]; do
            ((count++))
            if [ -n "$ext" ] && [ "$ext" != "$filename" ]; then
                new_filename="${base} (${count}).${ext}"
            else
                new_filename="${base} (${count})"
            fi
        done

        dest_file="$dest_dir/$new_filename"
    fi

    echo "Copying '$src_file' => '$dest_file'"
    cp -v "$src_file" "$dest_file"
}

# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
for dir in "${directories[@]}"; do
    echo "--------------------------------------------------"
    echo "Processing $dir"

    # Full path to the source directory
    full_path="$base_directory/$dir"

    # Check if directory exists
    if [ -d "$full_path" ]; then
        echo "Checking for files in $full_path"

        files_found=false

        for ext in "${extensions[@]}"; do
            shopt -s nullglob  # ignore if no files match
            for file in "$full_path"/*."$ext"; do
                [ -f "$file" ] || continue

                if [ "$ext" = "txt" ]; then
                    # Parse out the base (filename without extension)
                    base_name="$(basename "$file" .txt)"  
                    
                    # If base_name is in the special list, use suffix function
                    # Otherwise, overwrite
                    if [[ " ${special_txt_files[*]} " == *" $base_name "* ]]; then
                        copy_with_suffix_if_exists "$file" "$academizer_directory"
                    else
                        # Overwrite
                        filename="$(basename "$file")"
                        dest="$academizer_directory/$filename"
                        echo "Overwriting TXT file '$file' => '$dest'"
                        cp -v "$file" "$dest"
                    fi
                else
                    # For mhtml / html, always overwrite
                    filename="$(basename "$file")"
                    dest="$academizer_directory/$filename"
                    echo "Overwriting '$file' => '$dest'"
                    cp -v "$file" "$dest"
                fi

                files_found=true
            done
            shopt -u nullglob
        done

        # If at least one file was copied, run Git steps
        if $files_found; then
            echo "Files copied from $dir. Proceeding with Git operations."

            if cd "$academizer_directory"; then
                git add .
                if git commit -m "Imported files from $dir"; then
                    echo "Committed changes for $dir"
                    if git push; then
                        echo "Pushed changes for $dir"
                    else
                        echo "Git push failed for $dir"
                    fi
                else
                    echo "Git commit failed for $dir"
                fi
            else
                echo "Failed to change to academizer directory"
            fi

            # Return to the base directory
            if ! cd "$base_directory"; then
                echo "Failed to return to base directory. Exiting."
                exit 1
            fi
        else
            echo "No files to copy from $dir"
        fi
    else
        echo "Directory $full_path does not exist"
    fi
done
