from PIL import Image, ImageDraw, ImageFont, ImageFilter

# configuration ===

grid_size = 5  # 5x5 to match "IRON GOLD STONE GATE HEAD HOME"
cell_size = 64
text = "TYSO NTYS ONTYS ONTY SONTY SONT".replace(" ", "")
font_path = "fonts/NovaMonoStandardGalactic.ttf"  # Make sure this path is correct
output_path = "tyson-grid.png"
image_size = grid_size * cell_size

# === Create base images ===
base_image = Image.new("RGB", (image_size, image_size), "black")
padded_size = image_size + 8  # Add padding for glow
glow_layer = Image.new("RGB", (padded_size, padded_size), "black")
draw_base = ImageDraw.Draw(base_image)
draw_glow = ImageDraw.Draw(glow_layer)

# === Load font ===
try:
    font = ImageFont.truetype(font_path, size=32)  # Slightly smaller font size
except IOError:
    print("Font not found, using default.")
    font = ImageFont.load_default()

# === Generate spiral coordinates ===
def classic_inward_spiral(n):
    top, left = 0, 0
    bottom, right = n - 1, n - 1
    coords = []
    while top <= bottom and left <= right:
        for i in range(left, right + 1):  # Left to Right
            coords.append((top, i))
        top += 1
        for i in range(top, bottom + 1):  # Top to Bottom
            coords.append((i, right))
        right -= 1
        for i in range(right, left - 1, -1):  # Right to Left
            coords.append((bottom, i))
        bottom -= 1
        for i in range(bottom, top - 1, -1):  # Bottom to Top
            coords.append((i, left))
        left += 1
    return coords

# === Fill text into grid ===
grid = [["" for _ in range(grid_size)] for _ in range(grid_size)]
spiral_coords = classic_inward_spiral(grid_size)
for idx, (y, x) in enumerate(spiral_coords):
    if idx < len(text):
        grid[y][x] = text[idx]

# === Draw characters with glow ===
for row in range(grid_size):
    for col in range(grid_size):
        char = grid[row][col]
        pos_x = col * cell_size + cell_size // 2 + 4  # Adjust for padding
        pos_y = row * cell_size + cell_size // 2 + 4
        # Glow layer (multiple passes to intensify)
        for offset in [-2, 0, 2]:
            draw_glow.text((pos_x + offset, pos_y), char, font=font, fill=(0, 255, 0), anchor="mm")
            draw_glow.text((pos_x, pos_y + offset), char, font=font, fill=(0, 255, 0), anchor="mm")
        # Base text
        draw_base.text((pos_x - 4, pos_y - 4), char, font=font, fill=(0, 255, 0), anchor="mm")

# === Grid lines ===
grid_draw = ImageDraw.Draw(base_image)
line_color = (0, 120, 0)

# Draw all vertical and horizontal grid lines
for i in range(grid_size + 1):
    x = i * cell_size
    y = i * cell_size
    # Vertical lines
    grid_draw.line([(x, 0), (x, image_size - 1)], fill=line_color, width=1)
    # Horizontal lines
    grid_draw.line([(0, y), (image_size - 1, y)], fill=line_color, width=1)

# Draw the rightmost and bottommost edges explicitly
grid_draw.line([(image_size - 1, 0), (image_size - 1, image_size - 1)], fill=line_color, width=1)  # Right edge
grid_draw.line([(0, image_size - 1), (image_size - 1, image_size - 1)], fill=line_color, width=1)  # Bottom edge

# === Apply glow effect and merge ===
glow_image = glow_layer.filter(ImageFilter.GaussianBlur(4))
glow_image = glow_image.crop((4, 4, image_size + 4, image_size + 4))  # Crop back to original size
final_image = Image.blend(glow_image, base_image, alpha=0.8)

# === Save the image ===
final_image.save(output_path)
print(f"Saved to {output_path}")
