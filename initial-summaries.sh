#!/usr/bin/env bash
set -Eeuo pipefail

# Number of lines per chunk
CHUNK_LINES=100

MODEL_COMMAND=("ollama" "run" "vanilj/phi-4")
PROGRESS_FILE="progress.log"
OVERVIEW_FILE="overview.txt"

main_dir="$(pwd)"
touch "$main_dir/$PROGRESS_FILE"
touch "$main_dir/$OVERVIEW_FILE"

log() {
  local message="[${USER:-$(whoami)}@$(hostname)] [$(date '+%Y-%m-%d %H:%M:%S')] $*"
  echo "$message"
  echo "$message" >> "$main_dir/$PROGRESS_FILE"
}

is_processed() {
  local file_path="$1"
  grep -Fxq "$file_path" "$main_dir/$PROGRESS_FILE"
}

mark_processed() {
  local file_path="$1"
  echo "$file_path" >> "$main_dir/$PROGRESS_FILE"
}

cleanup_tempdirs() {
  if [[ -n "${TEMP_DIRS_CREATED:-}" ]]; then
    for tmpd in $TEMP_DIRS_CREATED; do
      [[ -d "$tmpd" ]] && rm -rf "$tmpd"
      log "Cleaned up temporary directory: $tmpd"
    done
  fi
}

log "Script started."

process_files_in_directory() {
  local dir="$1"
  log "Processing directory: $dir"

  shopt -s nullglob
  local all_files=("$dir"/*.txt)
  shopt -u nullglob

  [[ ${#all_files[@]} -eq 0 ]] && {
    log "No files found in $dir"
    return
  }

  for file in "${all_files[@]}"; do
    # 1) Skip if not a regular file or if it's a symlink
    [[ -f "$file" && ! -L "$file" ]] || continue

    # 2) Also skip if we’ve already processed it
    if is_processed "$file"; then
      log "Skipping (already processed): $file"
      continue
    fi

    # 3) Now process the .txt file
    log "Processing file: $file"

    # Create a temporary directory for chunking
    local file_name="$(basename "$file")"
    local sanitized_name
    sanitized_name="$(echo "$file_name" | tr -d '[:space:]')"
    local temp_dir
    temp_dir="$(mktemp -d "$dir/tmp_${sanitized_name}_XXXXXX")"
    TEMP_DIRS_CREATED="${TEMP_DIRS_CREATED:-} $temp_dir"
    log "Created temporary directory: $temp_dir"

    # Copy it as-is (or do any special processing if needed)
    local preprocessed_file="$temp_dir/preprocessed.txt"
    cp "$file" "$preprocessed_file"

    # Truncate the file to the first 100 lines
    head -n 100 "$preprocessed_file" > "$preprocessed_file.truncated"
    mv "$preprocessed_file.truncated" "$preprocessed_file"
    log "Truncated $file to the first 100 lines."

    # Summarize the truncated file and append to the overview file
    log "Summarizing file: $file"

    {
      echo "Summarizing the file: $file_name"
      echo "==============================="
      echo "Summarize the following text from \"$file_name\"."
      echo "Focus on main ideas, ignoring extraneous details."
      echo "---------------"
      cat "$preprocessed_file"
    } | "${MODEL_COMMAND[@]}" 2>>"$main_dir/$PROGRESS_FILE" | tee -a "$main_dir/$OVERVIEW_FILE"

    mark_processed "$file"
    log "Marked $file as processed."

    # Clean up the temporary directory
    rm -rf "$temp_dir"
    log "Removed temporary directory: $temp_dir"
  done
}

# Process the current directory
process_files_in_directory "$main_dir"

# Uncomment if you want to recurse into subdirectories
# for subdir in "$main_dir"/*/; do
#   [[ -d "$subdir" ]] && process_files_in_directory "$subdir"
# done

log "Script completed."