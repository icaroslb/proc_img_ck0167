from PIL import Image
import numpy as np

def gerar_matriz_aux ( M ):
    matriz_zero = np.zeros( [ M.shape[0] , M.shape[1] , 3 ] )

    return matriz_zero

def rgbPixel(h, s, v):

    sf = float(s/100)
    vf = float(v/100)
    
    c = vf * sf
    x = c * (1 - abs((h/60)%2 - 1))
    m = vf - c

    r1, g1, b1 = 0, 0, 0
    if(0 <= h < 60):
        r1, g1, b1 = c, x, 0
    elif(60 <= h < 120):
        r1, g1, b1 = x, c, 0
    elif(180 <= h < 240):
        r1, g1, b1 = 0, x, c
    elif(240 <= h < 300):
        r1, g1, b1 = x, 0, c
    elif(300 <= h < 360):
        r1, g1, b1 = c, 0, x

    r, g ,b = ((r1+m)*255, (g1+m)*255, (b1+m)*255)
    return round(r), round(g), round(b)

def hsvPixel(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0

    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn

    if df == 0:
        h = 0
    elif mx == r:   
        h = (60 * (((g-b)/df) % 6))
    elif mx == g:
        h = (60 * (((b-r)/df) +  2))
    elif mx == b:
        h = (60 * (((r-g)/df) + 4))
    if mx == 0:
        s = 0
    else:
        s = (df/mx)
    v = mx


    return round(h), int(s*100), int(v*100)

def hsvArray(imgArray):
    imgHSV = gerar_matriz_aux(imgArray)
    img = Image.fromarray(imgArray)


    #Reescreve os pixels em HSV
    for x in range(img.width):
        for y in range(img.height):
                r, g, b = img.getpixel((x, y))
                #print(img.getpixel((y, x)))
                #print(hsvPixel(r, g, b))
                imgHSV[x, y, :] = hsvPixel(r, g, b)

    return imgHSV

def rgbArray(imgHsvArray):
    rgbArray = gerar_matriz_aux(imgHsvArray)

    #Reescreve os pixels em RGB, convertendo pixel a pixel
    for x in range(imgHsvArray.shape[0]):
        for y in range(imgHsvArray.shape[1]):
                h, s, v = imgHsvArray[y, x, :]
                rgbArray[x, y, :] = rgbPixel(h, s, v)
    return rgbArray

def ajustarSat(imgHSV, newSat):

    #Cálculos em hsv
    for x in range(imgHSV.shape[0]):
        for y in range(imgHSV.shape[1]):
            h, s, v = imgHSV[x, y, :]
            #Checa se o pixel está em tom puro de cinza
            if(s == 0):
                s = s
            #Normaliza os valores e aplica a alteração de saturação
            elif(s + newSat > 100):
                s = 100
            elif(s + newSat <= 0):
                s = 1
            else:
                s = s + newSat
            imgHSV[x, y, :] = h, s, v

    #Converte de volta para rgb
    rgb = rgbArray(imgHSV)
    img = Image.fromarray(rgb.astype( np.uint8 ), 'RGB')
    return img            

def ajustarMatiz(imgHSV, newHue):

    #Cálculos em hsv
    for x in range(imgHSV.shape[0]):
        for y in range(imgHSV.shape[1]):
            h, s, v = imgHSV[x, y, :]
            #Aplica a alteração de matiz
            h = (h + newHue)%360
            imgHSV[x, y, :] = h, s, v

    #Converte de volta para rgb
    rgb = rgbArray(imgHSV)
    img = Image.fromarray(rgb.astype( np.uint8 ), 'RGB')
    return img