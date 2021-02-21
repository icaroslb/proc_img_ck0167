import numpy as np
import math

def transformada_fourier ( imagem ):
    dim = imagem.shape
    matriz_exp = np.zeros( dim, dtype = complex )
    matriz_transformada = np.zeros( dim, dtype = complex )

    for i in range( dim[0] ):
        for j in range( dim[1] ):

            for l in range( dim[0] ):
                for m in range( dim[1] ):
                    for n in range( dim[2] ):
                        matriz_exp[l][m][n] = np.exp( - np.complex( 2 * np.pi * ( ( i * l / dim[0] ) + ( j * m / dim[1] ) ) ) )

            for k in range( dim[2] ):
                matriz_transformada[i][j][k] = np.sum( imagem[ :, :, k ] * matriz_exp[ :, :, k ] )
    #matriz_transformada = np.fft.fft2( imagem )
    return transformada_inversa_fourier( matriz_transformada )

def transformada_inversa_fourier ( imagem ):
    dim = imagem.shape
    matriz_exp = np.zeros( dim, dtype = complex )
    matriz_transformada = np.zeros( dim, dtype = complex )

    for i in range( dim[0] ):
        for j in range( dim[1] ):

            for l in range( dim[0] ):
                for m in range( dim[1] ):
                    for n in range( dim[2] ):
                        matriz_exp[l][m][n] = np.exp( np.complex( 2 * np.pi * ( ( i * l / dim[0] ) + ( j * m / dim[1] ) ) ) )

            for k in range( dim[2] ):
                matriz_transformada[i][j][k] = ( 1 / ( dim[0] * dim[1] ) ) * np.sum( imagem[ :, :, k ] * matriz_exp[ :, :, k ] )
    #matriz_transformada = np.real( np.fft.ifft2( imagem ) )
    return np.real( matriz_transformada )