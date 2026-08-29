import base64
import os
import random
from PIL import Image, ImageDraw

def generate_cityscape():
    # Create a transparent image
    width, height = 800, 300
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw skyline
    x = 0
    while x < width:
        building_width = random.randint(20, 60)
        building_height = random.randint(50, 200)
        draw.rectangle([x, height - building_height, x + building_width, height], fill=(120, 120, 120, 150))
        x += building_width + random.randint(2, 10)
        
    img.save('cityscape.png')

def overlay_on_svg(svg_path):
    if not os.path.exists(svg_path):
        return
        
    with open('cityscape.png', 'rb') as f:
        b64_img = base64.b64encode(f.read()).decode('utf-8')
        
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        
    # Insert image just before closing </svg>
    img_tag = f'\n  <image href="data:image/png;base64,{b64_img}" x="0" y="0" width="100%" height="100%" preserveAspectRatio="none" style="mix-blend-mode: multiply; opacity: 0.3;" />\n</svg>'
    svg_content = svg_content.replace('</svg>', img_tag)
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == '__main__':
    generate_cityscape()
    overlay_on_svg('dist/github-contribution-grid-snake.svg')
    overlay_on_svg('dist/github-contribution-grid-snake-dark.svg')
    print("Overlay completed.")
