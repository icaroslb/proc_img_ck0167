import numpy as np
from PIL import Image

def negativo ( I ):
    M_uns = np.ones( I.shape )
    return M_uns - I

def ler_imagem( caminho ):
    return np.array( Image.open( caminho ) ) / 255

def mostrar_imagem( img ):
    img_mostrar = Image.fromarray( np.uint8( img * 255 ) ).convert( "RGB" )
    img_mostrar.show()

def salvar_imagem( img, caminho, formato ):
    img_salvar = Image.fromarray( np.uint8( img * 255 ) ).convert( "RGB" )
    img_salvar.save( caminho, formato )

if __name__ == "__main__":
    imagem = ler_imagem( "Imagens/Pinguim_1.jpg" )

    imagem_neg = negativo(imagem)
    imagens_juntas = np.hstack( ( imagem, imagem_neg ) )

    mostrar_imagem( imagens_juntas)

    salvar_imagem( imagens_juntas, "Imagens/Pinguins_normais_e_negativos.jpg", 'JPEG' )