#!/bin/bash

# Function to calculate chunk size to get approximately 25 or 26 chunks
calculate_chunk_size() {
    local total_lines=$1
    local chunk_size=$((total_lines / 25))

    # Ensure chunk size is at least 50 and at most 200
    if [ "$chunk_size" -lt 50 ]; then
        chunk_size=50
    elif [ "$chunk_size" -gt 200 ]; then
        chunk_size=200
    fi

    echo "$chunk_size"
}

# Function to process text files in a directory
process_files() {
    local dir=$1
    
    for file in "$dir"/*.txt; do
        # Skip if no .txt files are found
        [ -e "$file" ] || continue

        # Process the file if it's a regular file
        if [ -f "$file" ]; then
            local file_name=$(basename "$file")
            local total_lines=$(wc -l < "$file")
            local chunk_size=$(calculate_chunk_size "$total_lines")
            local num_chunks=$(( (total_lines + chunk_size - 1) / chunk_size ))  # Ceiling division

            echo "File: $file_name"
            echo "Total lines: $total_lines"
            echo "Chunk size: $chunk_size"
            echo "Number of chunks: $num_chunks"
            echo ""
        fi
    done
}

# Recursively process subdirectories
process_subdirectories() {
    local parent_dir=$1
    
    for dir in "$parent_dir"/*/; do
        if [ -d "$dir" ]; then
            process_files "$dir"  # Process files in the subdirectory
            process_subdirectories "$dir"  # Recursive call for nested subdirectories
        fi
    done
}

# Main execution
main_dir=$(pwd)
process_files "$main_dir"  # Process files in the main directory
process_subdirectories "$main_dir"  # Process files in subdirectories