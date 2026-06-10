import urllib.request
import ssl
import re
import os

ssl._create_default_https_context = ssl._create_unverified_context
outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get_page(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')

def find_images(html, base_url):
    urls = []
    for m in re.finditer(r'src="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
        u = m.group(1)
        if u.startswith('//'):
            u = 'https:' + u
        elif u.startswith('/'):
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            u = f'{parsed.scheme}://{parsed.netloc}{u}'
        urls.append(u)
    return urls

def download(url, name):
    try:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req, timeout=15).read()
        if len(data) > 10000:
            path = os.path.join(outdir, name)
            with open(path, 'wb') as f:
                f.write(data)
            print(f'OK {name}: {len(data)} bytes')
            return True
        else:
            print(f'TOO SMALL {name}: {len(data)} bytes')
            return False
    except Exception as e:
        print(f'FAIL {name}: {str(e)[:60]}')
        return False

# Recipe pages from eda.ru - find and download images
recipes = [
    ('croissant.jpg', 'https://eda.ru/recepty/vypechka-deserty/kruassany-klassicheskie-18757'),
    ('bread.jpg', 'https://eda.ru/recepty/vypechka-deserty/hleb-pshenichnyj-domashnij-193506'),
    ('tart.jpg', 'https://eda.ru/recepty/vypechka-deserty/tart-s-yablokami-35434'),
]

for name, url in recipes:
    print(f'\n--- {name} ---')
    try:
        html = get_page(url)
        images = find_images(html, url)
        print(f'Found {len(images)} images')
        for img_url in images[:5]:
            if download(img_url, name):
                break
    except Exception as e:
        print(f'Page error: {str(e)[:60]}')
