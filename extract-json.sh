#!/bin/bash

# Create archive file if it doesn't exist
touch archive.txt

# Log the start of the process
echo "Fetching video IDs from playlist..."

# Fetch video IDs from the playlist
video_ids=$(yt-dlp --cookies cookies.txt --skip-download --get-id "https://www.youtube.com/playlist?list=PLcKyTzEkOa-jf5kKmmBkf5JZPXyrz63i7")

# Check if we received any video IDs
if [ -z "$video_ids" ]; then
  echo "No video IDs found. Check if the playlist URL is correct and cookies are valid."
  exit 1
fi

# Process each video ID
for video_id in $video_ids; do
  echo "Processing video ID: $video_id"
  
  # Check if video is already in the archive
  if grep -q "$video_id" archive.txt; then
    echo "Skipping $video_id (already archived)"
  else
    # Log the metadata download attempt
    echo "Attempting to download metadata for video ID: $video_id"
    
    # Download metadata and check if it was successful
    yt-dlp --cookies cookies.txt --skip-download --write-info-json "https://www.youtube.com/watch?v=$video_id"
    if [ $? -eq 0 ]; then
      echo "$video_id" >> archive.txt
      echo "Metadata for $video_id downloaded and archived."
    else
      echo "Failed to download metadata for $video_id. Skipping..."
    fi
  fi
done

# Log the completion of the script
echo "All video IDs processed."
