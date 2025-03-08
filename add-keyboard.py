# Read the contents of index.html
with open('index.html', 'r') as file:
        html_content = file.read()

        # Add the link to the CSS file in the <head> section
        html_content = html_content.replace('<head>', '<head>\n<link rel="stylesheet" type="text/css" href="styles.css">')

        # Add the image at the end of the HTML file
        html_content += '\n<img src="sobel-keyboard.jpg" alt="Sobel Keyboard Image" style="display:block; margin: 20px auto;">\n'

        # Write the updated content back to index.html
        with open('index.html', 'w') as file:
                file.write(html_content)
