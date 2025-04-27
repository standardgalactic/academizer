#!/bin/bash

summary_file="detailed-overview.txt"
progress_file="progress.log"
main_dir=$(pwd)

# Function to check if a file is already processed
is_processed() {
    grep -Fxq "$1" "$main_dir/$progress_file"
}

# Create progress file if it doesn't exist
touch "$main_dir/$progress_file"

# Process text files in the current directory
process_files() {
    for file in *.txt; do
        if [ -f "$file" ]; then
            file_path=$(pwd)/"$file"
            if ! is_processed "$file_path"; then
                echo "Processing $file"
                echo "Processing $file" >> "$main_dir/$summary_file"

                ollama run wizardlm2 "The speaker is Darin Stevenson. Summarize:" < "$file" | tee -a "$main_dir/$summary_file"
                echo "$file_path" >> "$main_dir/$progress_file"
            fi
        fi
    done
}

# Check for subdirectories and recursively process them
process_subdirectories() {
    for dir in */; do
        if [ -d "$dir" ]; then
            echo "Entering directory $dir"
            echo "Directory: $dir" >> "$main_dir/$summary_file"
            
            # Change into the subdirectory
            cd "$dir" || continue

            # Process files in the subdirectory
            process_files

            # Recursively process any subdirectories within
            process_subdirectories

            # Return to the parent directory
            cd "$main_dir"
        fi
    done
}

# Main execution
echo "Processing directory: $main_dir"

# Remove the call to process_files here
# process_files

# Start processing subdirectories
process_subdirectories

