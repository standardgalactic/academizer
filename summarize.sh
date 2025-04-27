#!/usr/bin/env bash
set -Eeuo pipefail

CHUNK_LINES=40
MODEL_COMMAND=("ollama" "run" "vanilj/phi-4")
SUMMARY_OVERVIEW_FILE="defense-strategies.txt"

main_dir="$(pwd)"
touch "$main_dir/$SUMMARY_OVERVIEW_FILE"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

cleanup_tempdir() {
  if [[ -n "${temp_dir:-}" ]] && [[ -d "$temp_dir" ]]; then
    rm -rf "$temp_dir"
    log "Cleaned up temporary directory: $temp_dir"
  fi
}
trap cleanup_tempdir EXIT

summarize_file() {
  local file_to_process="$1"

  file_name="$(basename "$file_to_process")"
  san_name="$(echo "$file_name" | tr -d '[:space:]')"
  temp_dir="$(mktemp -d "$main_dir/tmp_${san_name}_XXXXXX")"

  log "Created temporary directory: $temp_dir"

  cp "$file_to_process" "$temp_dir/preprocessed.txt"

  split -l "$CHUNK_LINES" -- "$temp_dir/preprocessed.txt" "$temp_dir/chunk_"
  log "Split $file_to_process into chunks of $CHUNK_LINES lines each."

  {
    echo "============================================="
    echo "Summary for file: $file_name"
    echo "============================================="
  } >> "$SUMMARY_OVERVIEW_FILE"

  for chunk_file in "$temp_dir"/chunk_*; do
    [[ -f "$chunk_file" ]] || continue
    chunk_name="$(basename "$chunk_file")"
    log "Summarizing chunk: $chunk_name"

    {
      echo "Summarize the following text from \"$file_name\"."
      echo "Focus on main ideas, ignoring extraneous details."
      echo "---------------"
      cat "$chunk_file"
    } | "${MODEL_COMMAND[@]}" >> "$SUMMARY_OVERVIEW_FILE"

    echo "" >> "$SUMMARY_OVERVIEW_FILE"
  done

  log "Summarization completed for: $file_to_process"
}

# Main script logic (corrected)
for f in *; do
  if [[ -f "$f" && "$f" != *.* && ! -e "$f.mhtml" && ! -e "$f.txt" ]]; then
    log "Temporarily renaming '$f' to '$f.mhtml'"
    mv "$f" "$f.mhtml"

    log "Extracting text from '$f.mhtml'"
    python3 extract-text.py "$f.mhtml"

    log "Restoring original file name '$f'"
    mv "$f.mhtml" "$f"

    txt_file="$f.txt"

    if [[ -f "$txt_file" ]]; then
      summarize_file "$txt_file"
    else
      log "Failed to extract text for '$f', skipping summarization."
    fi
  fi
done
