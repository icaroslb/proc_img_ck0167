from rgbHsv import gerar_matriz_aux
import numpy as np
from PIL import Image

def equalizaCores(imgArray, r1, g1, b1):
    #imgArray é uma imagem em array e r1, g1 e b1 representam as expressões a serem calculadas nos componentes
    eqArray = gerar_matriz_aux(imgArray)
    for x in range(imgArray.shape[0]):
        for y in range(imgArray.shape[1]):
                r, g, b = imgArray[x, y, :]
                if(r1 != 0):
                    if(r1 + r > 255):
                        r = 255
                    elif(r1 + r < 0):
                        r = 0
                    else:
                        r = r + r1
                if(g1 != 0):
                    if(g1 + g > 255):
                        g = 255
                    elif(b1 + b < 0):
                        g = 0
                    else:
                        g = g + g1
                if(b1 != 0):
                    if(b1 + b > 255):
                        b = 255
                    elif(b1 + b < 0):
                        b = 0
                    else:
                        b = b + b1
                eqArray[x, y, :] = r, g, b
    
    return Image.fromarray((eqArray).astype(np.uint8))
