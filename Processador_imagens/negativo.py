from gerais import ler_imagem, mostrar_imagem, salvar_imagem
import numpy as np
from PIL import Image

def negativo ( I ):
    M_uns = np.ones( I.shape )
    return M_uns - I





if __name__ == "__main__":
    imagem = ler_imagem( "Imagens/Pinguim_1.jpg" )

    imagem_neg = negativo(imagem)
    imagens_juntas = np.hstack( ( imagem, imagem_neg ) )

    mostrar_imagem( imagens_juntas)

    salvar_imagem( imagens_juntas, "Imagens/Pinguins_normais_e_negativos.jpg", 'JPEG' )