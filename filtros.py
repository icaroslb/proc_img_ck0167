import numpy as np
import math

def gerar_matriz_aumentada ( M, tamanho ):
    M_aux = np.copy( M )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[0] + tamanho, :] = M_aux

    return matriz_zero

def convolucao ( dados, tamanho, dim, filtro, qtd, mutex ):
    imagem_inteira = np.copy( dados.I )
    imagem_aumentada = gerar_matriz_aumentada( imagem_inteira, tamanho )

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                conv = imagem_aumentada[ i : i + qtd, j : j + qtd, k ]

                valor = np.sum( conv * filtro )
                imagem_inteira[i][j][k] = valor

    mutex.acquire()

    dados.I = imagem_inteira

    mutex.release()

def media_simples ( dados, tamanho, mutex ):
    dim = dados.I.shape

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    filtro = np.ones( [ qtd, qtd ] ) / ( qtd * qtd )

    convolucao ( dados, tamanho, dim, filtro, qtd, mutex )

def gaussiano ( dados, tamanho, mutex ):
    dim = dados.I.shape

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

    convolucao( dados, tamanho, dim, filtro, qtd, mutex )

def mediana ( dados, tamanho, mutex ):
    M_aux = gerar_matriz_aumentada( dados.I, tamanho )

    dim = dados.I.shape

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    metade = [ int( ( qtd * qtd ) / 2 ), int( ( ( qtd * qtd ) / 2 ) + 1 ) ]

    mutex.acquire()

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
                dados.I[i][j][k] = ( lista_mediana[ metade[0] ] + lista_mediana[ metade[1] ] ) / 2

    mutex.release()

def terminal_filtro_generico ( dados, tamanho, mutex ):
    while ( True ):
        print( "\nEscolha o filtro:\n"
             + "1 - Média simples\n"
             + "2 - Gaussiano\n"
             + "3 - Mediana\n" )

        opcao = int( input( ": " ) )

        if ( opcao < 1 or opcao > 3 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break

    print( "Processando..." )
    if ( opcao == 1 ):
        media_simples( dados, tamanho, mutex )
    elif ( opcao == 2 ):
        gaussiano( dados, tamanho, mutex )
    elif ( opcao == 3 ):
        mediana( dados, tamanho, mutex )
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

    convolucao( dados, tamanho, dim, filtro, qtd, mutex )

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