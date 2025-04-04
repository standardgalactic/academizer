#!/usr/bin/env bash
set -Eeuo pipefail

SUMMARY_COMMAND=("ollama" "run" "vanilj/phi-4")

main_dir="$(pwd)"
output_file="$main_dir/stranded.text"
echo "" > "$output_file" # Initialize the output file

log() {
    local message="[${USER:-$(whoami)}@$(hostname)] [$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$message"
}

is_processed() {
    return 1
}

mark_processed() {
    return 0
}

log "Script started."

shopt -s nullglob
files=("$main_dir"/*.txt)
shopt -u nullglob

IFS=$'\n' sorted_files=($(printf "%s\n" "${files[@]}" | sort))
day=1

for file in "${sorted_files[@]}"; do
    [[ -f "$file" && ! -L "$file" ]] || continue

    if ! is_processed "$file"; then
        file_name="$(basename "$file")"

        log "Processing $file as Day $day"

        {
            echo "It is day number $day."
            echo "Summarize the following text as if it were a letter from Robinson Crusoe, written in Daniel Defoe-like King James English."
            echo "---------------"
            cat "$file"
        } | "${SUMMARY_COMMAND[@]}" | tee -a "$output_file"

        mark_processed "$file"
        log "Finished Day $day ($file_name)"
    else
        log "Skipping already processed file: $file"
    fi

    ((day++))
done

log "Script completed."
