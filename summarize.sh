#!/bin/bash

# Script to process text files (excluding overview.txt) and generate summaries
# Usage: Place in directory with .txt files and run

# Define constants
readonly PROGRESS_FILE="progress.log"
readonly SUMMARY_FILE="detailed-summary.txt"
readonly MAIN_DIR="$(pwd)"
readonly SKIP_FILE="overview.txt"

# Function to check if a file is already processed
is_processed() {
    local file="$1"
    grep -Fxq "$file" "$MAIN_DIR/$PROGRESS_FILE" 2>/dev/null
}

# Initialize log files
initialize_logs() {
    touch "$MAIN_DIR/$PROGRESS_FILE" "$MAIN_DIR/$SUMMARY_FILE" 2>/dev/null || {
        echo "Error: Cannot create log files in $MAIN_DIR" >&2
        exit 1
    }
    
    {
        echo "Script started at $(date)"
        echo "Summaries will be saved to $SUMMARY_FILE"
        echo "----------------------------------------"
    } >> "$MAIN_DIR/$PROGRESS_FILE"
}

# Function to process text files in a directory
process_files() {
    local dir="$1"
    echo "Processing directory: $dir" | tee -a "$MAIN_DIR/$PROGRESS_FILE"
    
    if [ ! -r "$dir" ]; then
        echo "Warning: Directory $dir is not readable" >&2
        return 1
    fi

    for file in "$dir"/*.txt; do
        [ -e "$file" ] || continue
        
        if [ -f "$file" ] && [ -r "$file" ]; then
            local file_name=$(basename "$file")
            
            # Skip overview.txt
            if [ "$file_name" = "$SKIP_FILE" ]; then
                echo "Skipping $file_name" >> "$MAIN_DIR/$PROGRESS_FILE"
                continue
            fi
            
            if ! is_processed "$file_name"; then
                echo "Processing $file_name" | tee -a "$MAIN_DIR/$PROGRESS_FILE"
                
                local sanitized_name=$(echo "$file_name" | tr -d '[:space:]')
                local temp_dir
                temp_dir=$(mktemp -d -t "tmp_${sanitized_name}_XXXXXX") || {
                    echo "Error: Failed to create temporary directory" >&2
                    continue
                }
                
                echo "Created temp directory: $temp_dir" >> "$MAIN_DIR/$PROGRESS_FILE"
                
                if ! split -l 100 "$file" "$temp_dir/chunk_" 2>/dev/null; then
                    echo "Error: Failed to split $file_name" >&2
                    rm -rf "$temp_dir"
                    continue
                fi
                
                echo "File split into chunks" >> "$MAIN_DIR/$PROGRESS_FILE"
                
                for chunk in "$temp_dir"/chunk_*; do
                    [ -f "$chunk" ] || continue
                    local chunk_name=$(basename "$chunk")
                    echo "Summarizing chunk: $chunk_name" >> "$MAIN_DIR/$PROGRESS_FILE"
                    
                    if ! ollama run vanilj/phi-4 "Summarize:" < "$chunk" >> "$MAIN_DIR/$SUMMARY_FILE" 2>/dev/null; then
                        echo "Warning: Failed to summarize $chunk_name" >&2
                    fi
                    echo "" >> "$MAIN_DIR/$SUMMARY_FILE"
                done
                
                rm -rf "$temp_dir" && echo "Removed temp directory: $temp_dir" >> "$MAIN_DIR/$PROGRESS_FILE"
                echo "$file_name" >> "$MAIN_DIR/$PROGRESS_FILE"
            fi
        fi
    done
}

# Function to process subdirectories recursively
process_subdirectories() {
    local parent_dir="$1"
    
    for dir in "$parent_dir"/*/ ; do
        [ -d "$dir" ] || continue
        process_files "$dir"
        process_subdirectories "$dir"
    done
}

# Main execution with error handling
main() {
    trap 'echo "Script interrupted at $(date)" >> "$MAIN_DIR/$PROGRESS_FILE"; exit 1' INT TERM
    
    initialize_logs
    process_files "$MAIN_DIR"
    process_subdirectories "$MAIN_DIR"
    
    echo "Script completed at $(date)" >> "$MAIN_DIR/$PROGRESS_FILE"
}

# Run main function
main
