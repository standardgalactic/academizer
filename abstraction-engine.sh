#!/bin/bash

INPUT_FILE="$1"
TMP_DIR=$(mktemp -d)
CHUNK_SIZE=500  # characters per chunk

split -b $CHUNK_SIZE -d "$INPUT_FILE" "$TMP_DIR/chunk_"

prev_speed=""

for chunk in "$TMP_DIR"/chunk_*; do
    [ -f "$chunk" ] || continue

    TYPE=$(python3 classify-chunk.py "$chunk")

    if [ "$TYPE" == "code" ]; then
        SPEED=275  # or 550 if you want max speed
    else
        SPEED=44
    fi

    # Avoid flickering: only change speed if different from last
    if [ "$SPEED" != "$prev_speed" ]; then
        echo -e "\n--- Switching to $SPEED wpm ---\n"
        prev_speed=$SPEED
    fi

    pv -q -L $((SPEED * 6)) < "$chunk"
done

rm -rf "$TMP_DIR"

