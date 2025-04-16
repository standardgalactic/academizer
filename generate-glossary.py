#!/c/Users/Mechachleopteryx/AppData/Local/Microsoft/WindowsApps/python3

from pathlib import Path

# Paths
fonts_folder = "fonts"
word_list_file = "common-words.txt"
output_file = "logico-philosophicus-glossary.html"

# Read the word list
words = []
with open(word_list_file, encoding="utf-8") as f:
    for line in f:
        word = line.strip()
        if word:
            words.append(word)

# HTML template
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Logico-Philosophico to SGA Viewer</title>
    <style>
        @font-face {{
            font-family: 'Logico';
            src: url('{fonts_folder}/Logico_philosophicus-Regular.ttf') format('truetype');
        }}
        @font-face {{
            font-family: 'SGA';
            src: url('{fonts_folder}/Sga-Regular.ttf') format('truetype');
        }}
        body {{
            font-family: sans-serif;
            padding: 2rem;
            background: white;
            color: black;
            transition: background 0.3s, color 0.3s;
        }}
        body.dark {{
            background: #111;
            color: #f0f0f0;
        }}
        .row {{
            display: flex;
            margin-bottom: 1rem;
        }}
        .logico {{
            font-family: 'Logico';
            font-size: 42pt;
            width: 30%;
        }}
        .sga {{
            font-family: 'SGA';
            font-size: 36pt;
            width: 30%;
        }}
        .toggle {{
            margin-bottom: 2rem;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            cursor: pointer;
            background-color: black;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background 0.3s, color 0.3s;
        }}
        body.dark .toggle {{
            background-color: white;
            color: black;
        }}
    </style>
</head>
<body>
    <button class="toggle" onclick="toggleMode()">Switch to Dark Mode</button>
    <h1>Logico-Philosophico → SGA Viewer</h1>

    <script>
        function toggleMode() {{
            const body = document.body;
            const btn = document.querySelector('.toggle');
            body.classList.toggle('dark');
            if (body.classList.contains('dark')) {{
                btn.textContent = "Switch to Light Mode";
            }} else {{
                btn.textContent = "Switch to Dark Mode";
            }}
        }}
    </script>
"""

# Add word pairs
for word in words:
    html += f"""    <div class="row">
        <div class="logico">{word}</div>
        <div class="sga">{word}</div>
    </div>\n"""

html += """</body>\n</html>"""

# Write the output HTML file
Path(output_file).write_text(html, encoding="utf-8")
print(f"HTML file generated: {output_file}")
