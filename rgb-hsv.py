from PIL import Image 
import numpy as np

def gerar_matriz_aux ( M ):
    matriz_zero = np.zeros( [ M.shape[0] , M.shape[1] , 3 ] )

    return matriz_zero

def hsvPixel(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0

    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn

    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

img = Image.open('pikachu.png')

imgArray = np.asarray(img)

imgHSV = gerar_matriz_aux(imgArray)
print(imgHSV)

#Reescreve os pixels em HSV
for x in range(img.width):
        for y in range(img.height):
            r, g, b = img.getpixel((y, x))
            imgHSV[x, y, :] = hsvPixel(r, g, b)

print(imgHSV)


imgHSV = Image.fromarray( imgHSV.astype( np.uint8 ), "HSV" )

print(imgHSV.mode)

print(hsvPixel(0, 215, 0))

imgHSV.show()