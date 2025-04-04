#!/bin/bash

# Define progress and summary files
progress_file="progress.log"
summary_file="detailed-summary.txt"
main_dir=$(pwd)

# Function to check if a file is already processed
is_processed() {
    grep -Fxq "$1" "$main_dir/$progress_file"
}

# Create progress and summary files if they don't exist
touch "$main_dir/$progress_file"
touch "$main_dir/$summary_file"

# Start logging script progress
{
    echo "Script started at $(date)"
    echo "Summaries will be saved to $summary_file"
} >> "$main_dir/$progress_file"

# Function to calculate chunk size to get approximately 25 or 26 chunks
calculate_chunk_size() {
    local total_lines=$(wc -l < "$1")
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
    echo "Processing directory: $dir"
    
    for file in "$dir"/*.txt; do
        # Skip if no .txt files are found
        [ -e "$file" ] || continue

        # Process the file if it's a regular file
        if [ -f "$file" ]; then
            local file_name=$(basename "$file")
            
            # Process only if not processed before
            if ! is_processed "$file_name"; then
                echo "Processing $file_name" | tee -a "$main_dir/$progress_file"

                # Create a temporary directory for the file's chunks
                sanitized_name=$(basename "$file" | tr -d '[:space:]')
                temp_dir=$(mktemp -d "$dir/tmp_${sanitized_name}_XXXXXX")
                echo "Temporary directory created: $temp_dir" >> "$main_dir/$progress_file"

                # Calculate chunk size
                chunk_size=$(calculate_chunk_size "$file")

                # Split the file into chunks
                split -l "$chunk_size" "$file" "$temp_dir/chunk_"
                echo "File split into chunks of $chunk_size lines each: $(find "$temp_dir" -type f)" >> "$main_dir/$progress_file"

                # Summarize each chunk and append to the summary file
                for chunk_file in "$temp_dir"/chunk_*; do
                    [ -f "$chunk_file" ] || continue
                    echo "Summarizing chunk: $(basename "$chunk_file")"
                    ollama run vanilj/phi-4 "Summarize:" < "$chunk_file" | tee -a "$main_dir/$summary_file"
                    echo "" >> "$main_dir/$summary_file"
                done

                # Remove the temporary directory
                rm -rf "$temp_dir"
                echo "Temporary directory $temp_dir removed" >> "$main_dir/$progress_file"

                # Mark the file as processed
                echo "$file_name" >> "$main_dir/$progress_file"
            fi
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
process_files "$main_dir"  # Process files in the main directory
process_subdirectories "$main_dir"  # Process files in subdirectories

# Mark script completion
echo "Script completed at $(date)" >> "$main_dir/$progress_file"