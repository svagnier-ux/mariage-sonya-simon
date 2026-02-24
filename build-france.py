import base64, re, urllib.request, os

# Read the source HTML from the browser capture
src = """PLACEHOLDER"""

# We'll read it from the saved file instead
with open('france-source.html', 'r') as f:
    html = f.read()

# Remove tiiny.site ad banner div
html = re.sub(r'<div style="position: fixed.*?</div></div>', '', html, flags=re.DOTALL, count=1)
html = html.replace('<div style="height: 55px !important;"></div>', '')
html = re.sub(r'<script[^>]*tiiny[^>]*></script>', '', html)
html = re.sub(r'<meta[^>]*th-modified[^>]*>', '', html)

# Replace local image refs with base64
img_map = {
    'photo52.jpg': 'img/photo52.jpg',
    'photo19.jpg': 'img/photo19.jpg',
    'photo105.jpg': 'img/photo105.jpg',
}

for ref, path in img_map.items():
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    uri = f'data:image/jpeg;base64,{b64}'
    html = html.replace(f'src="{ref}"', f'src="{uri}"')

# Hero bg from Google Photos
hero_url = "https://lh3.googleusercontent.com/p/AF1QipM5W_FeyIyu1d16WityZOyuxXoQoanDEFmXLBRk=s1360-w1360-h1020-rw"
try:
    req = urllib.request.Request(hero_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        hero_data = resp.read()
    hero_b64 = base64.b64encode(hero_data).decode()
    hero_uri = f'data:image/jpeg;base64,{hero_b64}'
    html = html.replace(f"url('{hero_url}')", f"url('{hero_uri}')")
    print(f"Hero image: {len(hero_data)/1024:.0f} KB")
except Exception as e:
    print(f"Hero download failed: {e}")

with open('france-standalone.html', 'w') as f:
    f.write(html)

print(f"france-standalone.html: {os.path.getsize('france-standalone.html')/1024:.0f} KB")
