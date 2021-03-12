from PIL import Image
import numpy as np

#Ler a imagem como matriz do numpy.
def mostrar_imagem( img ):
    img_mostrar = Image.fromarray( np.uint8( img * 255 ) ).convert( "RGB" )
    img_mostrar.show()

def ler_imagem( caminho ):
    return np.array( Image.open( caminho ) ) / 255

def salvar_imagem( img, caminho, formato ):
    img_salvar = Image.fromarray( np.uint8( img * 255 ) ).convert( "RGB" )
    img_salvar.save( caminho, formato )