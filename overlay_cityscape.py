import os
import urllib.request
from PIL import Image

def fetch_and_composite_skyline():
    cn_tower_url = "https://img.icons8.com/ios-filled/500/cn-tower.png"
    buildings_url = "https://img.icons8.com/ios-filled/500/city-buildings.png"
    
    urllib.request.urlretrieve(cn_tower_url, "cn_tower.png")
    urllib.request.urlretrieve(buildings_url, "buildings.png")
    
    cn_tower = Image.open("cn_tower.png").convert("RGBA")
    buildings = Image.open("buildings.png").convert("RGBA")
    
    width, height = 800, 300
    skyline = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    
    cn_tower = cn_tower.resize((int(cn_tower.width * 0.4), int(cn_tower.height * 0.4)))
    buildings = buildings.resize((int(buildings.width * 0.5), int(buildings.height * 0.5)))
    
    # White overlay to make it visible on dark mode
    for x in range(0, width, buildings.width - 20):
        skyline.paste(buildings, (x, height - buildings.height), buildings)
    skyline.paste(cn_tower, (150, height - cn_tower.height), cn_tower)
    
    # Create white version
    data = skyline.getdata()
    newData = []
    for item in data:
        if item[3] > 0:
            newData.append((255, 255, 255, 180)) # White with opacity
        else:
            newData.append(item)
    skyline.putdata(newData)
    
    skyline.save("toronto_skyline_white.png")
    return "toronto_skyline_white.png"

def overlay_on_svg(svg_path, img_path):
    if not os.path.exists(svg_path):
        return
        
    import base64
    with open(img_path, 'rb') as f:
        b64_img = base64.b64encode(f.read()).decode('utf-8')
        
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        
    img_tag = f'\n  <image href="data:image/png;base64,{b64_img}" x="0" y="0" width="100%" height="100%" preserveAspectRatio="none" style="opacity: 0.3;" />\n</svg>'
    svg_content = svg_content.replace('</svg>', img_tag)
    
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

if __name__ == '__main__':
    img_path = fetch_and_composite_skyline()
    overlay_on_svg('dist/github-contribution-grid-snake-dark.svg', img_path)
    print("Overlay with Toronto skyline completed.")
