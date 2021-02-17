import numpy as np
from PIL import Image
from gerais import ler_imagem, mostrar_imagem

def limiarizar(I):

    limiar = int(input("Insira um valor inteiro entre 0 e 255 para servir de limiar: "))

    bw = Image.fromarray( np.uint8( I * 255 ) ).convert( "RGB" )
    bw = bw.convert('L')

    for x in range(bw.width):
        for y in range(bw.height):
            if bw.getpixel((x,y)) < limiar:
                bw.putpixel( (x,y), 0 )
            else:
                bw.putpixel( (x,y), 255 )
    
    print("Exibindo resultado da limiarização...")
    bw.show()