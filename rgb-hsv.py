from PIL import Image 
import numpy as np
import cv2

def gerar_matriz_aux ( M ):
    matriz_zero = np.zeros( [ M.shape[0] , M.shape[1] , 3 ] )

    return matriz_zero

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

    return np.uint8(h), np.uint8(s*100), np.uint8(v*100)

def hsvArray(imgArray):
    imgHSV = gerar_matriz_aux(imgArray)
    img = Image.fromarray(imgArray)


    #Reescreve os pixels em HSV
    for x in range(img.width):
        for y in range(img.height):
                r, g, b = img.getpixel((y, x))
                #print(img.getpixel((y, x)))
                #print(hsvPixel(r, g, b))
                imgHSV[x, y, :] = hsvPixel(r, g, b)

    #imgHSV = Image.fromarray( imgHSV.astype(np.uint8), "HSV" )

    return imgHSV

def ajustarSat(imgHSV):
    newSat = 30
    for x in range(imgHSV.shape[0]):
        for y in range(imgHSV.shape[1]):
            imgHSV[x, y,] = imgHSV[x, y,] + 30