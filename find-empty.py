import json

# Load playlist JSON
playlist_file = 'Protosociology [PLcKyTzEkOa-jf5kKmmBkf5JZPXyrz63i7].info.json'
with open(playlist_file, 'r') as f:
    playlist_data = json.load(f)

# Load empty directory names
with open('empty_dirs.txt', 'r') as f:
    empty_dirs = {line.strip() for line in f}

# Find missing videos
for entry in playlist_data['entries']:
    if entry['title'] in empty_dirs:
        print(f"Missing Video: {entry['title']} by {entry['uploader']}")
