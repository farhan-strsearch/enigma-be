#!/usr/bin/env bash

PATH_ARG="$1"
OUTPUT_FILE="$2"

if [ -z "$PATH_ARG" ]; then
    echo "Usage: $0 <path> [output_file]"
    exit 1
fi

if [ ! -d "$PATH_ARG" ]; then
    echo "Error: The path '$PATH_ARG' does not exist."
    exit 1
fi

TREE_LINES=()

show_tree () {
    local folder="$1"
    local indent="$2"

    items=()
    for f in "$folder"/*; do
        name=$(basename "$f")

        if [[ "$name" == "venv" || "$name" == "__pycache__" || "$name" == "node_modules" ]]; then
            continue
        fi

        items+=("$name")
    done

    count=${#items[@]}
    i=0

    for item in "${items[@]}"; do
        ((i++))

        if [ "$i" -eq "$count" ]; then
            symbol="\\--"
        else
            symbol="|--"
        fi

        line="${indent}${symbol} ${item}"
        echo "$line"
        TREE_LINES+=("$line")

        if [ -d "$folder/$item" ]; then
            if [ "$i" -eq "$count" ]; then
                new_indent="${indent}   "
            else
                new_indent="${indent}|   "
            fi

            show_tree "$folder/$item" "$new_indent"
        fi
    done
}

echo "$PATH_ARG"
TREE_LINES+=("$PATH_ARG")

show_tree "$PATH_ARG" ""

if [ -n "$OUTPUT_FILE" ]; then
    printf "%s\n" "${TREE_LINES[@]}" > "$OUTPUT_FILE"
    echo ""
    echo "Folder structure saved to: $OUTPUT_FILE"
fi