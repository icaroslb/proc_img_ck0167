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

def transformada_passa_baixa_dura( ondas, raio ):
    ondas_passadas = np.copy( ondas )

    dim = ondas_passadas.shape
    meio = int( dim[0] / 2 ), int( dim[1] / 2 )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                if( ( abs( i - meio[0] ) + abs( j - meio[1] ) ) > raio ):
                    ondas_passadas[i][j][k] = 0

    return ondas_passadas

def transformada_passa_baixa_suave( ondas, raio, raio_suave ):
    ondas_passadas = np.copy( ondas )

    dim = ondas_passadas.shape
    meio = int( dim[0] / 2 ), int( dim[1] / 2 )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                dist = abs( i - meio[0] ) + abs( j - meio[1] )
                if( dist > raio ):
                    ondas_passadas[i][j][k] = ondas[i][j][k] * max( ( raio_suave - abs( dist - raio ) ) / raio_suave, 0 ) ** 0.5
    
    return ondas_passadas

def transformada_passa_alta_dura( ondas, raio ):
    ondas_passadas = np.copy( ondas )

    dim = ondas_passadas.shape
    meio = int( dim[0] / 2 ), int( dim[1] / 2 )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                if( ( abs( i - meio[0] ) + abs( j - meio[1] ) ) < raio ):
                    ondas_passadas[i][j][k] = 0
    
    return ondas_passadas

def transformada_passa_alta_suave( ondas, raio, raio_suave ):
    ondas_passadas = np.copy( ondas )

    dim = ondas_passadas.shape
    meio = int( dim[0] / 2 ), int( dim[1] / 2 )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                dist = abs( i - meio[0] ) + abs( j - meio[1] )
                if( dist < raio ):
                    ondas_passadas[i][j][k] = ondas[i][j][k] * max( ( raio_suave - abs( raio - dist ) ) / raio_suave, 0 ) ** 0.5
    
    return ondas_passadas

def transformada_terminal( dados, mutex ):
    while ( True ):
        print( "\nEscolha o filtro:\n"
             + "1 - Passa baixa dura\n"
             + "2 - Passa alta dura\n"
             + "3 - Passa faixa dura\n"
             + "4 - Passa baixa suave\n"
             + "5 - Passa alta suave\n"
             + "6 - Passa faixa suave\n" )

        opcao = int( input( ": " ) )

        if ( opcao < 1 or opcao > 6 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break
    
    ondas = np.zeros( dados.I.shape, dtype = complex )
    ondas_resul = np.zeros( dados.I.shape )
    
    for i in range( dados.I.shape[2] ):
        ondas[ :, :, i ] = np.fft.fft2( dados.I[ :, :, i ] )
        ondas[ :, :, i ] = np.fft.fftshift( ondas[ :, :, i ] )
    
    
    if ( opcao == 1 or opcao == 3 ):
        raio = float( input( "Insira o raio passa baixa: " ) )
        ondas = transformada_passa_baixa_dura( ondas, raio )
    
    if ( opcao == 2 or opcao == 3 ):
        raio = float( input( "Insira o raio passa alta: " ) )
        ondas = transformada_passa_alta_dura( ondas, raio )
    
    if ( opcao == 4 or opcao == 6 ):
        raio = float( input( "Insira o raio passa baixa: " ) )
        raio_suave = float( input( "Insira o raio de suavização: " ) )
        ondas = transformada_passa_baixa_suave( ondas, raio, raio_suave )
    
    if ( opcao == 5 or opcao == 6 ):
        raio = float( input( "Insira o raio passa alta: " ) )
        raio_suave = float( input( "Insira o raio de suavização: " ) )
        ondas = transformada_passa_alta_suave( ondas, raio, raio_suave )

    
    for i in range( 3 ):
        ondas[ :, :, i ] = np.fft.fftshift( ondas[ :, :, i ] )
        ondas_resul[ :, :, i ] = np.real( np.fft.ifft2( ondas[ :, :, i ] ) )
    
        mini = min( [ valor for x in ondas_resul[ :, :, i ] for valor in x  ] )
        maxi = max( [ valor for x in ondas_resul[ :, :, i ] for valor in x  ] )

        ondas_resul[ :, :, i ] = ( ondas_resul[ :, :, i ] - mini ) / ( maxi - mini )

    mutex.acquire()
    
    dados.I = ondas_resul

    mutex.release()