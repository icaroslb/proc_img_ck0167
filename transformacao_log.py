import numpy as np
import gerais
from PIL import Image

def transform_log( I , const):
    logArray = I + 1
    logArray = np.log(logArray)
    logImg = Image.fromarray( np.uint8( logArray * 255 ) ).convert( "RGB" )
    logImg = Image.eval(logImg, (lambda x: x * const))
    logArray = np.array( logImg ) / 255
    #print(logArray)
    return logArray

if __name__ == "__main__":
    imagem = gerais.ler_imagem( "Imagens/Pinguim_1.jpg" )
    
    imagem_log = transform_log(imagem, 1)
    imagens_juntas = np.hstack( ( imagem, imagem_log ) )
    
    gerais.mostrar_imagem( imagens_juntas)
    
    gerais.salvar_imagem( imagens_juntas, "Imagens/Pinguins_normais_e_negativos.jpg", 'JPEG' )