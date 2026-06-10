import urllib.request, ssl, re, os
ssl._create_default_https_context = ssl._create_unverified_context
outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

recipes = [
    'https://eda.ru/recepty/vypechka-deserty/hleb-s-semechkami-43481',
    'https://eda.ru/recepty/vypechka-deserty/zavarnoj-hleb-181783',
    'https://eda.ru/recepty/vypechka-deserty/hleb-borodinskij-51187',
    'https://eda.ru/recepty/vypechka-deserty/hleb-s-otrubjami-186776',
]

for url in recipes:
    name = url.rstrip('/').split('-')[-2] if '-' in url else url
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
        images = re.findall(r'<img[^>]+src="([^"]+\.(?:jpg|jpeg|png))"', html)
        print(f'{name}: {len(images)} images')
        for img in images[:5]:
            if img.startswith('//'):
                img = 'https:' + img
            elif img.startswith('/'):
                img = 'https://eda.ru' + img
            if any(x in img.lower() for x in ['logo', 'avatar', 'icon', 'vk.', 'fb.']):
                continue
            try:
                ireq = urllib.request.Request(img, headers=headers)
                data = urllib.request.urlopen(ireq, timeout=10).read()
                print(f'  {len(data)} bytes: {img[:90]}')
                if len(data) > 50000:
                    path = os.path.join(outdir, 'bread.jpg')
                    with open(path, 'wb') as f:
                        f.write(data)
                    print(f'  *** SAVED as bread.jpg ***')
                    exit()
            except Exception as e:
                print(f'  error: {str(e)[:40]}')
    except Exception as e:
        print(f'{name}: FAILED - {str(e)[:40]}')
