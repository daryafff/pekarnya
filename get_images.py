import re, urllib.request, ssl, os, random
ssl._create_default_https_context = ssl._create_unverified_context

outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'

# Try to get images from Russian food sites
urls_to_try = [
    # Known recipe image URLs from gastronom.ru
    "https://www.gastronom.ru/sites/default/files/recipes/croissant.jpg",
    "https://www.gastronom.ru/sites/default/files/recipes/bread.jpg",
    "https://www.gastronom.ru/sites/default/files/recipes/tart.jpg",
]

# Fetch from eda.ru recipes for croissant, bread, tart
recipes = [
    ("croissant", "https://eda.ru/recepty/vypechka-deserty/kruassany-klassicheskie-18757"),
    ("bread", "https://eda.ru/recepty/vypechka-deserty/hleb-pshenichnyj-domashnij-193506"),
    ("tart", "https://eda.ru/recepty/vypechka-deserty/tart-s-yablokami-35434"),
]

for name, url in recipes:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        # Find image URLs - simple pattern matching
        for match in re.finditer(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
            img_url = match.group(1)
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            elif img_url.startswith('/'):
                img_url = 'https://eda.ru' + img_url
            if img_url:
                print(f"{name}: trying {img_url}")
                try:
                    ireq = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    data = urllib.request.urlopen(ireq, timeout=10).read()
                    if len(data) > 5000:  # more than 5KB = real image
                        ext = 'jpg' if 'jpeg' in img_url or 'jpg' in img_url else 'png'
                        fname = f"{name}.{ext}"
                        path = os.path.join(outdir, fname)
                        with open(path, 'wb') as f:
                            f.write(data)
                        print(f"  DOWNLOADED: {fname} ({len(data)} bytes)")
                        break
                    else:
                        print(f"  too small: {len(data)} bytes")
                except Exception as e:
                    print(f"  failed: {str(e)[:50]}")
    except Exception as e:
        print(f"{name}: page fetch failed - {str(e)[:50]}")
