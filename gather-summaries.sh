#!/bin/bash

# Base directory where your repos are
BASE_DIR="."  # change if needed
DEST_DIR="$BASE_DIR/summaries"

mkdir -p "$DEST_DIR"

counter=1

# Find all overview.txt files
find "$BASE_DIR" -type f -name "overview.txt" | while read -r file; do
    # Skip if already in summaries folder
    if [[ "$file" == "$DEST_DIR"* ]]; then
        continue
    fi

    # Compute file hash to check for duplicates
    hash=$(sha256sum "$file" | cut -d ' ' -f 1)
    duplicate=false

    for existing in "$DEST_DIR"/*.txt; do
        [[ -e "$existing" ]] || continue
        existing_hash=$(sha256sum "$existing" | cut -d ' ' -f 1)
        if [[ "$existing_hash" == "$hash" ]]; then
            echo "Duplicate found: $file"
            duplicate=true
            break
        fi
    done

    if ! $duplicate; then
        # Extract just the parent directory name
        parent_dir=$(basename "$(dirname "$file")")

        # Create destination filename
        dest_file="$DEST_DIR/summary_$counter.txt"

        # Write the folder name at the top, then append file content
        {
            echo "$parent_dir"
            echo
            cat "$file"
        } > "$dest_file"

        echo "Copied: $file -> $(basename "$dest_file")"
        ((counter++))
    fi
done

echo "✅ Done. Summaries are in: $DEST_DIR"

