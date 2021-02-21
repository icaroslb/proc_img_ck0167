import numpy as np
import math

from gerais import salvar_imagem
import fourier

def gerar_matriz_aumentada ( M, tamanho ):
    M_aux = np.copy( M )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[1] + tamanho, :] = M_aux

    return matriz_zero

def convolucao ( imagem, tamanho, dim, filtro, qtd ):
    retorno = np.zeros( imagem.shape )
    imagem_aumentada = gerar_matriz_aumentada( imagem, tamanho )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                conv = imagem_aumentada[ i : i + qtd, j : j + qtd, k ]

                valor = 0
                for x in range( qtd ):
                    for y in range( qtd ):
                        valor = valor + ( conv[x][y] * filtro[x][y] )

                retorno[i][j][k] = valor
    
    return retorno

def media_simples ( imagem, tamanho ):
    dim = imagem.shape

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    filtro = np.ones( [ qtd, qtd ] ) / ( qtd * qtd )

    return convolucao( imagem, tamanho, dim, filtro, qtd )

def gaussiano ( imagem, tamanho ):
    dim = imagem.shape

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9
    
    filtro = np.zeros( [ qtd, qtd ] )

    metade = int( qtd / 2 )
    
    sigma = qtd / 5

    divisao = 1 / ( 2 * math.pi * ( sigma ** 2 ) )

    for i in range( qtd ):
        for j in range( qtd ):
            exp = math.exp( - ( ( ( ( i - metade ) ** 2 ) + ( ( j - metade ) ** 2 ) ) / ( 2 * ( sigma ** 2 ) ) ) )
            filtro[i][j] = divisao * exp

    return convolucao( imagem, tamanho, dim, filtro, qtd )

def mediana ( imagem, tamanho ):
    M_aux = gerar_matriz_aumentada( imagem, tamanho )

    dim = imagem.shape

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    metade = [ int( ( qtd * qtd ) / 2 ), int( ( ( qtd * qtd ) / 2 ) + 1 ) ]

    lista_mediana = []

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                lista_mediana.clear()

                filtro = M_aux[ i:i+qtd, j:j+qtd, k ]
                for x in filtro:
                    for y in x:
                        lista_mediana.append( y )
                
                lista_mediana = sorted( lista_mediana )
                imagem[i][j][k] = ( lista_mediana[ metade[0] ] + lista_mediana[ metade[1] ] ) / 2
    
    return imagem

def laplaciano ( imagem, constante ):
    filtro = np.array( [ [ 1, 1, 1 ], [ 1, -8, 1 ], [ 1, 1, 1 ] ] )

    mascara = convolucao( imagem, 1, imagem.shape, filtro, 3 )
    mascara = -1 * mascara

    laplace = imagem + ( constante * mascara )

    maior_valor = max( [ valor for linha in laplace for profundidade in linha for valor in profundidade ] )
    menor_valor = min( [ valor for linha in laplace for profundidade in linha for valor in profundidade ] )

    return ( laplace - menor_valor ) / ( maior_valor - menor_valor )

def high_boost ( imagem, constante ):
    img = np.copy( imagem )
    borrada = mediana( img, 1 )

    mascara = imagem - borrada

    boost = imagem + ( constante * mascara )

    maior_valor = max( [ valor for linha in boost for profundidade in linha for valor in profundidade ] )
    menor_valor = min( [ valor for linha in boost for profundidade in linha for valor in profundidade ] )

    return ( boost - menor_valor ) / ( maior_valor - menor_valor ) 

def sobel_x ( imagem ):
    filtro = np.array( [ [ -1, 0, 1 ], [ -2, 0, 2 ], [ -1, 0, 1 ] ] )
    
    imagem_filtrada = convolucao( imagem, 1, imagem.shape, filtro, 3 )

    maior_valor = max( [ valor for linha in imagem_filtrada for profundidade in linha for valor in profundidade ] )
    menor_valor = min( [ valor for linha in imagem_filtrada for profundidade in linha for valor in profundidade ] )

    return ( imagem_filtrada - menor_valor ) / ( maior_valor - menor_valor )

def sobel_y ( imagem ):
    filtro = np.array( [ [ 1, 2, 1 ], [ 0, 0, 0 ], [ -1, -2, -1 ] ] )
    
    imagem_filtrada = convolucao( imagem, 1, imagem.shape, filtro, 3 )

    maior_valor = max( [ valor for linha in imagem_filtrada for profundidade in linha for valor in profundidade ] )
    menor_valor = min( [ valor for linha in imagem_filtrada for profundidade in linha for valor in profundidade ] )

    return ( imagem_filtrada - menor_valor ) / ( maior_valor - menor_valor )

def sobel_xy ( imagem ):
    mascara_x = sobel_x( imagem )
    mascara_y = sobel_y( imagem )

    #return ( mascara_x + mascara_y ) / 2
    return ( mascara_x + mascara_y ) / 2

def terminal_filtro_generico ( dados, tamanho, mutex ):
    while ( True ):
        print( "\nEscolha o filtro:\n"
             + "1 - Média simples\n"
             + "2 - Gaussiano\n"
             + "3 - Mediana\n"
             + "4 - Laplaciano\n"
             + "5 - High boost\n"
             + "6 - Sobel x\n"
             + "7 - Sobel y\n"
             + "8 - Sobel xy\n"
             + "9 - Fourier\n" )

        opcao = int( input( ": " ) )

        if ( opcao < 1 or opcao > 9 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break

    print( "Processando..." )

    mutex.acquire()

    if ( opcao == 1 ):
        dados.I = media_simples( dados.I, tamanho )
    elif ( opcao == 2 ):
        dados.I = gaussiano( dados.I, tamanho )
    elif ( opcao == 3 ):
        dados.I = mediana( dados.I, tamanho )
    elif ( opcao == 4 ):
        dados.I = laplaciano( dados.I, 0.2 )
    elif ( opcao == 5 ):
        dados.I = high_boost( dados.I, 0.5 )
    elif ( opcao == 6 ):
        dados.I = sobel_x( dados.I )
    elif ( opcao == 7 ):
        dados.I = sobel_y( dados.I )
    elif ( opcao == 8 ):
        dados.I = sobel_xy( dados.I )
    elif ( opcao == 9 ):
        dados.I = fourier.transformada_fourier( dados.I )

    mutex.release()

    print( "Completo" )

def terminal_filtro_customizado ( dados, tamanho, mutex ):
    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    filtro = np.zeros( [ qtd, qtd ] )

    print( "\n**separe os números com espaço**\n" )
    for i in range( qtd ):
        filtro[ i, : ] = [ float( i ) for i in input( "Insira a linha {}: ".format( i ) ).split( " " ) ]

    dim = dados.I.shape

    print( "Processando..." )

    mutex.acquire()

    dados.I = convolucao( dados.I, tamanho, dim, filtro, qtd )

    mutex.release()

    print( "Completo" )

def terminal ( dados, mutex ):
    while ( True ):
        print( "\nEscolha o tipo de filtro:\n"
             + "1 - Filtros genérico\n"
             + "2 - Filtros customizados\n" )

        opcao_filtro = int( input( ": " ) )

        if ( opcao_filtro < 1 or opcao_filtro > 2 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break
    
    while ( True ):
        print( "\nQual o tamanho do filtro?\n"
             + "1 - 3x3\n"
             + "2 - 5x5\n"
             + "3 - 7x7\n"
             + "4 - 9x9\n")

        opcao_tamanho = int( input( ": " ) )

        if ( opcao_tamanho < 1 or opcao_tamanho > 4 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break

    if ( opcao_filtro == 1 ):
        terminal_filtro_generico( dados, opcao_tamanho, mutex )
    elif ( opcao_filtro == 2 ):
        terminal_filtro_customizado( dados, opcao_tamanho, mutex )