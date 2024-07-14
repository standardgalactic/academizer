while IFS= read -r file; do
    echo "Checking $file"
    if [[ -f "$PWD/$file" ]]; then
        echo "File: $file"
        ollama run mistral "Summarize:" < "$PWD/$file"
    else
        echo "Skipping $file: File not found or not accessible."
    fi
done < file_list.txt


: '
while IFS= read -r file; do
    echo "Checking $file"
    if [[ -f "$file" ]]; then
        echo "File: $file"
        ollama run mistral "Summarize:" < "$file"
    else
        echo "Skipping $file: File not found or not accessible."
    fi
done < file_list.txt

while IFS= read -r file; do
    echo "Checking $file"
    if [[ -f "./$file" ]]; then
        echo "File: $file"
        ollama run mistral "Summarize:" < "./$file"
    else
        echo "Skipping $file: File not found or not accessible."
    fi
done < file_list.txt
'
