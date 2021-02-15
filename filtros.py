import numpy as np

def convolucao ( dados, M_aux, dim, filtro, qtd ):
    dados.mutex.acquire()

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                valor = 0
                aux = M_aux[ i:i+qtd, j:j+qtd, k ]

                valor = np.sum( aux * filtro )
                dados.I[i][j][k] = valor

    dados.mutex.release()

def media_simples ( dados, tamanho ):
    M_aux = np.copy( dados.I )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[0] + tamanho, :] = M_aux
    M_aux = matriz_zero

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    filtro = np.ones( [ qtd, qtd ] ) / ( qtd * qtd )

    metade = [ int( ( qtd * qtd ) / 2 ), int( ( ( qtd * qtd ) / 2 ) + 1 ) ]

    convolucao ( dados, M_aux, dim, filtro, qtd )

def gaussiano ( dados, tamanho ):
    return

def mediana ( dados, tamanho ):
    M_aux = np.copy( dados.I )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[0] + tamanho, :] = M_aux
    M_aux = matriz_zero

    if ( tamanho == 1 ):
        qtd = 3
    elif ( tamanho == 2 ):
        qtd = 5
    elif ( tamanho == 3 ):
        qtd = 7
    elif ( tamanho == 4 ):
        qtd = 9

    metade = [ int( ( qtd * qtd ) / 2 ), int( ( ( qtd * qtd ) / 2 ) + 1 ) ]

    dados.mutex.acquire()

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                dados.I[i][j][k] = np.median( M_aux[ i:i+qtd, j:j+qtd, k ] )

    dados.mutex.release()

def terminal_filtro_generico ( dados, tamanho ):
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
        media_simples( dados, tamanho )
    elif ( opcao == 2 ):
        gaussiano( dados, tamanho )
    elif ( opcao == 3 ):
        mediana( dados, tamanho )
    print( "Completo" )

def terminal_filtro_customizado ( dados, tamanho ):
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

    print( filtro )

    M_aux = np.copy( dados.I )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[0] + tamanho, :] = M_aux
    M_aux = matriz_zero

    print( "Processando..." )

    convolucao( dados, M_aux, dim, filtro, qtd )

    print( "Completo" )

def terminal ( dados ):
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
        terminal_filtro_generico( dados, opcao_tamanho )
    elif ( opcao_filtro == 2 ):
        terminal_filtro_customizado( dados, opcao_tamanho )

    if ( opcao_tamanho == 1 ):
        filtro = np.zeros( [ 3, 3 ] )
    elif ( opcao_tamanho == 2 ):
        filtro = np.zeros( [ 5, 5 ] )
    elif ( opcao_tamanho == 3 ):
        filtro = np.zeros( [ 7, 7 ] )
    elif ( opcao_tamanho == 4 ):
        filtro = np.zeros( [ 9, 9 ] )

