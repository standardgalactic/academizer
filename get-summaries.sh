#!/usr/bin/env bash
set -Eeuo pipefail

CHUNK_LINES=100

MODEL_COMMAND=("ollama" "run" "vanilj/phi-4")
PROGRESS_FILE="progress.log"
SUMMARY_OVERVIEW_FILE="overview.txt"

main_dir="$(pwd)"
touch "$main_dir/$PROGRESS_FILE"
touch "$main_dir/$SUMMARY_OVERVIEW_FILE"

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
trap cleanup_tempdirs EXIT

log "Script started."

process_files_in_directory() {
  local dir="$1"
  log "Processing directory: $dir"

  shopt -s nullglob
  local all_files=("$dir"/*.txt)
  shopt -u nullglob

  [[ ${#all_files[@]} -eq 0 ]] && {
    log "No .txt files found in $dir"
    return
  }

  for file in "${all_files[@]}"; do
    [[ -f "$file" && ! -L "$file" ]] || continue

    local file_name="$(basename "$file")"

    if is_processed "$file"; then
      log "Skipping (already processed): $file"
      continue
    fi

    log "Processing file: $file"

    local sanitized_name
    sanitized_name="$(echo "$file_name" | tr -d '[:space:]')"
    local temp_dir
    temp_dir="$(mktemp -d "$dir/tmp_${sanitized_name}_XXXXXX")"
    TEMP_DIRS_CREATED="${TEMP_DIRS_CREATED:-} $temp_dir"
    log "Created temporary directory: $temp_dir"

    local preprocessed_file="$temp_dir/preprocessed.txt"
    cp "$file" "$preprocessed_file"

    split -l "$CHUNK_LINES" -- "$preprocessed_file" "$temp_dir/chunk_"
    log "Split $file into chunks of $CHUNK_LINES lines each."

    {
      echo "============================================="
      echo "Summary for file: $file_name"
      echo "============================================="
    } >> "$SUMMARY_OVERVIEW_FILE"

    for chunk_file in "$temp_dir"/chunk_*; do
      [[ -f "$chunk_file" ]] || continue
      local chunk_name
      chunk_name="$(basename "$chunk_file")"
      log "Summarizing chunk: $chunk_name"

      {
        echo "Summarize the following text from \"$file_name\"."
        echo "Focus on main ideas, ignoring extraneous details."
        echo "---------------"
        cat "$chunk_file"
      } | "${MODEL_COMMAND[@]}" 2>>"$main_dir/$PROGRESS_FILE" \
        >> "$SUMMARY_OVERVIEW_FILE"

      echo "" >> "$SUMMARY_OVERVIEW_FILE"
    done

    mark_processed "$file"
    log "Marked $file as processed."
  done
}

process_files_in_directory "$main_dir"

log "Script completed."
