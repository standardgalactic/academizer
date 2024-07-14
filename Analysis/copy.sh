mkdir -p files

while IFS= read -r file; do
	echo "Coping $file to 'files' folder"
	if [[ -f "$file" ]]; then
		cp "$file" files/
	else
		echo "Skipping $file: File not found or not accessible."
	fi
done < file_list.txt

