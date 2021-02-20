import numpy as np
import math

def gerar_matriz_aumentada ( M, tamanho ):
    M_aux = np.copy( M )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[1] + tamanho, :] = M_aux

    return matriz_zero

def convolucao ( imagem, tamanho, dim, filtro, qtd ):
    retorno = np.copy( imagem )
    imagem_aumentada = gerar_matriz_aumentada( retorno, tamanho )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                conv = imagem_aumentada[ i : i + qtd, j : j + qtd, k ]

                valor = np.sum( conv * filtro )
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

def laplaciano ( imagem, tamanho ):
    dim = imagem.shape

    if ( tamanho == 1 ):
        qtd = 3
        filtro = np.array( [ [ -1, -1, -1 ], [ -1, 8, -1 ], [ -1, -1, -1 ] ] ) / 8
    elif ( tamanho == 2 ):
        qtd = 5
        filtro = np.array( [ [ 1, 1, 1 ], [ 1, -8, 1 ], [ 1, 1, 1 ] ] )
    elif ( tamanho == 3 ):
        qtd = 7
        filtro = np.array( [ [ 1, 1, 1 ], [ 1, -8, 1 ], [ 1, 1, 1 ] ] )
    elif ( tamanho == 4 ):
        qtd = 9
        filtro = np.array( [ [ 1, 1, 1 ], [ 1, -8, 1 ], [ 1, 1, 1 ] ] )
    
    return imagem + convolucao( imagem, tamanho, dim, filtro, qtd )

def high_boost ( imagem, constante ):
    np.copy( imagem )
    
    borrada = media_simples( imagem, 2 )

    mascara = imagem - borrada

    return imagem + ( constante * mascara )

def terminal_filtro_generico ( dados, tamanho, mutex ):
    while ( True ):
        print( "\nEscolha o filtro:\n"
             + "1 - Média simples\n"
             + "2 - Gaussiano\n"
             + "3 - Mediana\n"
             + "4 - Laplaciano\n"
             + "5 - High boost" )

        opcao = int( input( ": " ) )

        if ( opcao < 1 or opcao > 5 ):
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
        dados.I = laplaciano( dados.I, tamanho )
    elif ( opcao == 5 ):
        dados.I = high_boost( dados.I, 4.5 )

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