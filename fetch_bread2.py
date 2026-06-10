import urllib.request, ssl, re, os
ssl._create_default_https_context = ssl._create_unverified_context
outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=20).read()

def get_img(url):
    data = get(url)
    return data

# Try to get a bread image from known working sources
# Let's try 1000.menu with a specific bread recipe
urls = [
    ('https://1000.menu/cooking/20254-domashnii-xleb-v-duxovke', 'bread1'),
    ('https://1000.menu/cooking/49028-xleb-pshenichnyi-domashnii', 'bread2'),
    ('https://1000.menu/cooking/1627-domashnii-xleb', 'bread3'),
]

# Also try iamcook.ru
iam_urls = [
    'https://www.iamcook.ru/showrecipe/1190',  # homemade bread
]

for url, name in urls:
    try:
        print(f'Trying: {url}')
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        # Find image with "bread" related keywords
        for m in re.finditer(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"[^>]*>', html, re.I):
            u = m.group(0)
            src = re.search(r'src="([^"]+)"', u).group(1)
            alt = re.search(r'alt="([^"]*)"', u)
            alt_text = alt.group(1).lower() if alt else ''
            if src.startswith('//'): src = 'https:' + src
            elif src.startswith('/'): src = 'https://1000.menu' + src
            # Check alt text for bread keywords
            if any(k in alt_text for k in ['хлеб', 'хлеба', 'хлебный', 'выпечка', 'хлебушек']):
                try:
                    data = get_img(src)
                    if len(data) > 20000:
                        path = os.path.join(outdir, 'bread.jpg')
                        with open(path, 'wb') as f:
                            f.write(data)
                        print(f'  SAVED bread.jpg: {len(data)} bytes (alt: {alt_text})')
                        exit()
                except:
                    pass
        # Fallback: try largest image
        candidates = []
        for m in re.finditer(r'src="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
            u = m.group(1)
            if u.startswith('//'): u = 'https:' + u
            elif u.startswith('/'): u = 'https://1000.menu' + u
            if any(x in u.lower() for x in ['logo', 'avatar', 'icon', 'vk.', 'fb.']):
                continue
            try:
                data = get_img(u)
                if len(data) > 20000:
                    candidates.append((len(data), u, data))
            except:
                pass
        candidates.sort(key=lambda x: -x[0])
        if candidates:
            size, u, data = candidates[0]
            path = os.path.join(outdir, 'bread.jpg')
            with open(path, 'wb') as f:
                f.write(data)
            print(f'  SAVED bread.jpg (fallback): {size} bytes from {u[:80]}')
            exit()
    except Exception as e:
        print(f'  Error: {str(e)[:60]}')

# Try russianfood.com as last resort
try:
    print('Trying russianfood.com...')
    req = urllib.request.Request('https://russianfood.com/recipes/recipe.php?rid=169663', headers=headers)
    html = urllib.request.urlopen(req, timeout=15).read().decode('cp1251', errors='ignore')
    for m in re.finditer(r'src="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
        u = m.group(1)
        if u.startswith('//'): u = 'https:' + u
        elif u.startswith('/'): u = 'https://russianfood.com' + u
        try:
            data = get_img(u)
            if len(data) > 20000:
                path = os.path.join(outdir, 'bread.jpg')
                with open(path, 'wb') as f:
                    f.write(data)
                print(f'  SAVED bread.jpg: {len(data)} bytes')
                exit()
        except:
            pass
except Exception as e:
    print(f'Error: {str(e)[:60]}')
