import urllib.request, ssl, re, os, sys
ssl._create_default_https_context = ssl._create_unverified_context
outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=20).read()

def get_html(url):
    return get(url).decode('utf-8', errors='ignore')

def find_large_images(html, base_url, min_bytes=30000):
    from urllib.parse import urlparse
    parsed = urlparse(base_url)
    results = []
    for m in re.finditer(r'(?:src|content)="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
        u = m.group(1)
        if u.startswith('//'):
            u = 'https:' + u
        elif u.startswith('/'):
            u = f'{parsed.scheme}://{parsed.netloc}{u}'
        # Skip small icons, logos, avatars
        if any(x in u.lower() for x in ['logo', 'avatar', 'icon', 'favicon', 'banner', 'vk.', 'fb.']):
            continue
        if u not in results:
            results.append(u)
    # Try to download and check size
    valid = []
    for u in results[:10]:
        try:
            data = get(u)
            if len(data) >= min_bytes:
                valid.append((u, len(data)))
        except:
            pass
    valid.sort(key=lambda x: -x[1])
    return valid

# Specific recipe URLs with GOOD photos of what we need
targets = [
    ('croissant.jpg', [
        'https://eda.ru/recepty/vypechka-deserty/kruassany-klassicheskie-18757',
        'https://www.gastronom.ru/recipe/27515/kruassany-klassicheskie',
        'https://1000.menu/cooking/24610-kruassany-klassicheskie',
    ]),
    ('bread.jpg', [
        'https://eda.ru/recepty/vypechka-deserty/hleb-pshenichnyj-domashnij-193506',
        'https://www.gastronom.ru/recipe/10037/hleb-pshenichnyj-domashnij',
        'https://1000.menu/cooking/39491-domashnii-xleb-v-duxovke',
    ]),
    ('tart.jpg', [
        'https://eda.ru/recepty/vypechka-deserty/tart-s-yablokami-35434',
        'https://www.gastronom.ru/recipe/2543/tart-taten-s-yablokami',
        'https://1000.menu/cooking/16281-tart-s-yablokami',
    ]),
]

for fname, urls in targets:
    print(f'\n=== {fname} ===')
    found = False
    for url in urls:
        if found:
            break
        try:
            print(f'Trying: {url}')
            html = get_html(url)
            images = find_large_images(html, url)
            print(f'  Found {len(images)} large images')
            for img_url, size in images[:3]:
                print(f'  -> {size} bytes: {img_url[:80]}')
                ext = 'jpg' if 'jpg' in img_url or 'jpeg' in img_url else 'png'
                path = os.path.join(outdir, fname)
                data = get(img_url)
                with open(path, 'wb') as f:
                    f.write(data)
                print(f'  SAVED {fname} ({len(data)} bytes)')
                found = True
                break
        except Exception as e:
            print(f'  Error: {str(e)[:60]}')
