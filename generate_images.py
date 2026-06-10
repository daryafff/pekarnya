from PIL import Image, ImageDraw, ImageFilter
import os, math

outdir = r'C:\Users\Nikita\Desktop\Darya\bakery\images'
os.makedirs(outdir, exist_ok=True)

W, H = 600, 400

def make_croissant():
    img = Image.new('RGB', (W, H), '#F5E6D3')
    d = ImageDraw.Draw(img)
    # Background panel
    d.rounded_rectangle([20, 20, 580, 380], radius=20, fill='#EDD9C0')
    # Shadow
    d.ellipse([140, 280, 460, 340], fill='#D4A574')
    d.ellipse([160, 285, 440, 330], fill='#C49A6C')
    # Body - outer
    pts = [(170,270),(190,190),(230,160),(300,180),(360,150),(420,190),(450,150),(460,120),(430,100),(380,120),(320,145),(280,150),(235,165),(195,145),(155,125),(135,145),(135,195),(155,255)]
    d.polygon(pts, fill='#D4A050')
    # Body - mid layer
    pts2 = [(185,258),(200,195),(235,168),(295,185),(353,158),(408,190),(435,155),(442,130),(418,112),(378,128),(320,150),(280,155),(238,168),(200,150),(168,136),(150,152),(148,198),(165,245)]
    d.polygon(pts2, fill='#E8C46A')
    # Body - inner highlight
    pts3 = [(195,248),(208,200),(240,175),(290,190),(345,165),(395,192),(420,160),(425,140),(405,125),(370,138),(318,155),(280,158),(240,170),(208,155),(182,142),(165,158),(162,198),(175,235)]
    d.polygon(pts3, fill='#F0D68A')
    # Layer lines
    d.line([(240,175),(290,190),(345,165)], fill='#C49A3C', width=3)
    d.line([(208,200),(240,175)], fill='#C49A3C', width=2)
    d.line([(345,165),(395,192)], fill='#C49A3C', width=2)
    d.line([(235,168),(200,150)], fill='#B8862D', width=2)
    d.line([(353,158),(408,190)], fill='#B8862D', width=2)
    d.line([(300,180),(320,145)], fill='#C49A3C', width=1)
    # Highlights
    d.line([(240,170),(300,185)], fill='#F5E6C0', width=2)
    d.line([(310,185),(355,165)], fill='#F5E6C0', width=2)
    # Top crust
    d.arc([225, 148, 375, 195], 180, 0, fill='#B8862D', width=4)
    return img

def make_bread():
    img = Image.new('RGB', (W, H), '#F5E6D3')
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([20, 20, 580, 380], radius=20, fill='#EDD9C0')
    # Shadow
    d.ellipse([130, 260, 470, 360], fill='#D4A574')
    d.ellipse([150, 270, 450, 350], fill='#C49A6C')
    # Main loaf
    d.ellipse([140, 140, 460, 340], fill='#C49A3C')
    d.ellipse([145, 145, 455, 335], fill='#D4A860')
    d.ellipse([150, 145, 450, 330], fill='#DDB870')
    # Top highlight
    d.ellipse([200, 130, 400, 240], fill='#E8C870')
    d.ellipse([230, 135, 370, 210], fill='#F0D890')
    # Crust texture - scoring
    d.line([(210,170),(255,205),(300,178),(345,210),(390,175)], fill='#A0761A', width=6, joint='curve')
    d.line([(230,195),(270,222),(310,198),(350,225)], fill='#A0761A', width=4, joint='curve')
    d.line([(250,210),(280,232),(310,215)], fill='#A0761A', width=3, joint='curve')
    # Flour dust
    for _ in range(40):
        x = 180 + int(ImageDraw.Draw(img).textlength(' ', font=None) * 0) + hash(str(_)) % 260
        y = 180 + hash(str(_+100)) % 120
        r = 1 + hash(str(_+200)) % 3
        d.ellipse([x, y, x+r*2, y+r*2], fill='#FFF8EE', outline=None)
    return img

def make_tart():
    img = Image.new('RGB', (W, H), '#F5E6D3')
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([20, 20, 580, 380], radius=20, fill='#EDD9C0')
    # Shadow
    d.ellipse([110, 240, 490, 370], fill='#D4A574')
    d.ellipse([130, 250, 470, 360], fill='#C49A6C')
    # Crust
    d.ellipse([120, 150, 480, 350], fill='#B8862D')
    d.ellipse([125, 155, 475, 345], fill='#C49A3C')
    d.ellipse([130, 158, 470, 340], fill='#D4A860')
    # Filling
    d.ellipse([145, 168, 455, 330], fill='#F4A940')
    d.ellipse([155, 175, 445, 320], fill='#E8A030')
    d.ellipse([165, 182, 435, 312], fill='#F0B050')
    # Apple slices
    apples = [(230,210,260,235),(320,195,350,220),(265,240,292,262),(345,228,372,250),(210,235,235,255),(295,230,322,252),(250,195,270,215),(305,215,328,235),(225,255,248,272),(335,215,355,235)]
    for x1,y1,x2,y2 in apples:
        d.ellipse([x1,y1,x2,y2], fill='#C0392B')
    # Apple slice highlights
    for x1,y1,x2,y2 in apples:
        d.ellipse([x1+2,y1+2,x2-2,y2-2], fill='#D45040')
    # Glaze
    d.ellipse([180, 195, 420, 290], fill='#F4C860', outline=None)
    # Crust edge pattern
    for i in range(16):
        x = 150 + i * 20
        d.arc([x-5, 150, x+20, 195], 0, 180, fill='#A0761A', width=3)
    # Serving slice
    d.polygon([(300,200),(340,190),(360,280),(300,310)], fill='#F4A940')
    d.polygon([(305,205),(338,196),(355,275),(305,300)], fill='#E8A030')
    d.ellipse([310,207,330,225], fill='#C0392B')
    # Glaze on slice
    d.polygon([(305,205),(335,195),(340,240),(305,260)], fill='#F4C860')
    return img

make_croissant().save(os.path.join(outdir, 'croissant.png'))
make_bread().save(os.path.join(outdir, 'bread.png'))
make_tart().save(os.path.join(outdir, 'tart.png'))

for f in ['croissant.png', 'bread.png', 'tart.png']:
    fp = os.path.join(outdir, f)
    sz = os.path.getsize(fp)
    print(f'  {f}: {sz} bytes')
print('Done!')
