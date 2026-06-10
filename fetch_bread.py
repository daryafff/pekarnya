import urllib.request, ssl, re, os
ssl._create_default_https_context = ssl._create_unverified_context
outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def get_page(url):
    req = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')

def find_img(html, base_url):
    for m in re.finditer(r'src="([^"]+\.(?:jpg|jpeg|png))"', html, re.I):
        u = m.group(1)
        if u.startswith('//'):
            u = 'https:' + u
        elif u.startswith('/'):
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            u = f'{parsed.scheme}://{parsed.netloc}{u}'
        if 'logo' not in u.lower() and 'icon' not in u.lower() and 'avatar' not in u.lower():
            try:
                req2 = urllib.request.Request(u, headers=headers)
                data = urllib.request.urlopen(req2, timeout=10).read()
                if len(data) > 10000:
                    path = os.path.join(outdir, 'bread.jpg')
                    with open(path, 'wb') as f:
                        f.write(data)
                    print(f'OK bread.jpg: {len(data)} bytes')
                    return True
            except:
                pass
    return False

# Try these bread recipe pages
pages = [
    'https://eda.ru/recepty/vypechka-deserty/hleb-borodinskij-51187',
    'https://eda.ru/recepty/vypechka-deserty/hleb-s-semechkami-43481',
    'https://eda.ru/recepty/vypechka-deserty/zavarnoj-hleb-181783',
    'https://russianfood.com/recipes/recipe.php?rid=169663',
    'https://russianfood.com/recipes/recipe.php?rid=137228',
]

for url in pages:
    try:
        html = get_page(url)
        if find_img(html, url):
            break
    except:
        continue
