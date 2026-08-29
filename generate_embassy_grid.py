import os
import json
import urllib.request
from datetime import datetime

def get_latest_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            for event in data:
                if event['type'] == 'PushEvent':
                    repo = event['repo']['name']
                    commits = event['payload']['commits']
                    msg = commits[0]['message'] if commits else "Made some updates"
                    return repo, msg
    except Exception as e:
        print("Error fetching activity:", e)
    return "prajwal918/prajwal918", "Squashed bugs and improved performance."

def escape_xml(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\"', '&quot;')

def create_svg(username, repo, msg):
    repo = escape_xml(repo)
    msg = escape_xml(msg)
    
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="300">
    <style>
        .title {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 20px; fill: #A8C0D8; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; }}
        .subtitle {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; fill: #8b949e; }}
        .text {{ font-family: sans-serif; font-size: 16px; fill: #c9d1d9; }}
        .highlight {{ fill: #f59e0b; font-weight: bold; }}
        .box {{ fill: #0d1117; stroke: #30363d; stroke-width: 2px; rx: 8px; }}
        .box:hover {{ stroke: #A8C0D8; }}
        a {{ cursor: pointer; }}
    </style>
    <rect width="100%" height="100%" fill="#010409" />
    
    <!-- Central Command / Embassy Grid -->
    <a href="https://github.com/{username}" target="_blank">
        <rect x="15" y="15" width="375" height="120" class="box" />
        <text x="35" y="55" class="title">🏛 THE EMBASSY</text>
        <text x="35" y="80" class="subtitle">STATUS: ONLINE | SECTOR 6</text>
        <text x="35" y="110" class="text">COMMANDER: <tspan class="highlight">@{username}</tspan></text>
    </a>
    
    <!-- Latest Intel / Activity -->
    <a href="https://github.com/{repo}" target="_blank">
        <rect x="410" y="15" width="375" height="120" class="box" />
        <text x="430" y="55" class="title">📡 LATEST INTEL</text>
        <text x="430" y="80" class="subtitle">TARGET: {repo}</text>
        <text x="430" y="110" class="text">COMM: "{msg[:30]}{'...' if len(msg)>30 else ''}"</text>
    </a>
    
    <!-- Core Modules -->
    <a href="https://github.com/{username}/keylogger-monitor" target="_blank">
        <rect x="15" y="150" width="243" height="135" class="box" />
        <text x="35" y="195" class="title">MODULE 01</text>
        <text x="35" y="225" class="subtitle">KEYLOGGER MONITOR</text>
        <text x="35" y="255" class="text" style="font-size:13px; fill:#8b949e;">SYSTEM SURVEILLANCE</text>
    </a>
    
    <a href="https://github.com/{username}/resource-hub" target="_blank">
        <rect x="278" y="150" width="244" height="135" class="box" />
        <text x="298" y="195" class="title">MODULE 02</text>
        <text x="298" y="225" class="subtitle">RESOURCE HUB</text>
        <text x="298" y="255" class="text" style="font-size:13px; fill:#8b949e;">DATA VAULT</text>
    </a>
    
    <a href="https://github.com/{username}/mcq-platform" target="_blank">
        <rect x="542" y="150" width="243" height="135" class="box" />
        <text x="562" y="195" class="title">MODULE 03</text>
        <text x="562" y="225" class="subtitle">MCQ PLATFORM</text>
        <text x="562" y="255" class="text" style="font-size:13px; fill:#8b949e;">TESTING CHAMBER</text>
    </a>
</svg>"""
    os.makedirs('dist', exist_ok=True)
    with open('dist/embassy-grid.svg', 'w', encoding='utf-8') as f:
        f.write(svg)

if __name__ == "__main__":
    repo, msg = get_latest_activity("prajwal918")
    create_svg("prajwal918", repo, msg)
    print("Embassy Grid SVG generated.")
