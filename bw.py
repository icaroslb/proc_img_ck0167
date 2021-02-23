from rgbHsv import gerar_matriz_aux
import numpy as np
from PIL import Image

def bwMediana(imgArray):
    #L = R*0.3 + B*0.59 + G*0.11
    bwArray = gerar_matriz_aux(imgArray)
    for x in range(imgArray.shape[0]):
        for y in range(imgArray.shape[1]):
            r, g, b = imgArray[x, y, :]
            lum = int(r*0.3 + g*0.59 + b*0.11)
            bwArray[x, y, :] = lum, lum, lum
    
    return Image.fromarray((bwArray).astype(np.uint8))

def bwMedia(imgArray):
    #L = (R + B + G)/3
    bwArray = gerar_matriz_aux(imgArray)
    for x in range(imgArray.shape[0]):
        for y in range(imgArray.shape[1]):
            r, g, b = imgArray[x, y, :]
            lum = int((int(r) + int(g) + int(b))/3)
            bwArray[x, y, :] = lum, lum, lum
    
    return Image.fromarray((bwArray).astype(np.uint8))

def salvarprompt(img):
    print("Deseja Salvar a imagem?")
    print (" 0: Não\n"
            + " 1: Sim\n")
    salvar = int( input ( ": " ) )
    if(salvar == 1):
        path = input("Insira o caminho da nova imagem: ")
        img.save(path)

def converter(caminho):
    salvar = 0
    imgArray = np.asarray(Image.open(caminho))
    print("Como deseja converter?")
    print (" 0: Conversão por média\n"
            + " 1: Conversão por mediana\n"
            + "-1: Sair\n")

    opcao = int( input ( ": " ) )

    if(opcao == 0):
        img = bwMedia(imgArray)
        img.show()
        salvarprompt(img)
    elif(opcao == 1):
        img = bwMediana(imgArray)
        img.show()
        salvarprompt(img)
    else:
        return
        
        

converter("pikachu.png")