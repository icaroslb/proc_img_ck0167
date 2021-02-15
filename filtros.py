import numpy as np

def convolucao ( M, tamanho, filtro ):
    return

def media_simples ( M, tamanho ):
    return

def gaussiano ( M, tamanho ):
    return

def mediana ( M, tamanho ):
    M_aux = np.copy( M )
    dim = M.shape

    matriz_zero = np.zeros( [ dim[0] + tamanho, dim[1] + tamanho, dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho - 1, tamanho : dim[0] + tamanho - 1, :] = M_aux
    M_aux = matriz_zero

    if ( opcao_tamanho == 1 ):
        qtd = 3
    elif ( opcao_tamanho == 2 ):
        qtd = 5
    elif ( opcao_tamanho == 3 ):
        qtd = 7
    elif ( opcao_tamanho == 4 ):
        qtd = 9

    metade = [ ( qtd * qtd ) / 2, ( ( qtd * qtd ) / 2 ) + 1 ]

    for i in range( dim[0] ):
        for j in range( dim[1] ):
            for k in range( dim[2] ):
                ordem = []

                for l in range( i, i + qtd ):
                    for m in range( j, j + qtd ):
                        ordem.append( M_aux[l][m][k] )

                M[i][j][k] = ( ordem[ metade[0] ] + ordem[ metade[1] ] ) / 2

    return M

def terminal_filtro_generico ( M, tamanho ):
    while ( True ):
        print( "\nEscolha o filtro:\n"
             + "1 - Média simples"
             + "2 - Gaussiano"
             + "3 - Mediana" )

        opcao = int( input( ": " ) )

        if ( opcao < 1 or opcao > 3 ):
            print( "\nOpção inexistente!!\n" )
        else:
            break

    return

def terminal_filtro_customizado ( M, filtro ):
    return

def terminal ( M ):
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

    if ( opcao_tamanho == 1 ):
        filtro = np.zeros( [ 3, 3 ] )
    elif ( opcao_tamanho == 2 ):
        filtro = np.zeros( [ 5, 5 ] )
    elif ( opcao_tamanho == 3 ):
        filtro = np.zeros( [ 7, 7 ] )
    elif ( opcao_tamanho == 4 ):
        filtro = np.zeros( [ 9, 9 ] )

