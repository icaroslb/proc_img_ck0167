import numpy as np
import gerais

def mais_prox ( valor ):
    valor_1 = int( valor )
    valor_2 = valor_1 + 1

    dif_1 = valor - valor_1
    dif_2 = valor_2 - valor

    if ( valor_1 < dif_2 ):
        return valor_1
    else:
        return valor_2

def bilinear ( img, pos_x, pos_y, k ):
    pos_x_1 = int( pos_x )
    pos_x_2 = pos_x_1 + 1

    peso_x_1 = abs( pos_x - pos_x_2 )
    peso_x_2 = pos_x - pos_x_1
    if ( pos_x_2 >= img.shape[0] ):
        pos_x_2 = pos_x_1
        peso_x_2 = 0
    
    pos_y_1 = int( pos_y )
    pos_y_2 = pos_y_1 + 1
                    
    peso_y_1 = abs( pos_y - pos_y_2 )
    peso_y_2 = pos_y - pos_y_1
    if ( pos_y_2 >= img.shape[1] ):
        pos_y_2 = pos_y_1
        peso_y_2 = 0
    
    media_1 = ( peso_x_1 * img[pos_x_1][pos_y_1][k] ) + ( peso_x_2 * img[pos_x_2][pos_y_1][k] )
    media_2 = ( peso_x_1 * img[pos_x_1][pos_y_2][k] ) + ( peso_x_2 * img[pos_x_2][pos_y_2][k] )

    return ( peso_y_1 * media_1 ) + ( peso_y_2 * media_2 )

def escala_proximo ( img, aumento ):
    novo_shape = [ int( img.shape[0] * aumento ), int( img.shape[1] * aumento ), img.shape[2] ]
    img_escalada = np.zeros( novo_shape )

    if ( aumento == 1 ):
        img_escalada = img
    else:
        for i in range( novo_shape[0] ):
            pos_x = min( mais_prox( i / aumento ), img.shape[0] - 1 )

            for j in range( novo_shape[1] ):
                pos_y = min( mais_prox( j / aumento ), img.shape[1] - 1 )

                for k in range( novo_shape[2] ):
                    img_escalada[i][j][k] = img[pos_x][pos_y][k]

    return img_escalada

def escala_bilinear ( img, aumento ):
    novo_shape = [ int( img.shape[0] * aumento ), int( img.shape[1] * aumento ), img.shape[2] ]
    img_escalada = np.zeros( novo_shape )

    if ( aumento == 1 ):
        img_escalada = img
    else:
        for i in range( novo_shape[0] ):
            pos_x = i / aumento
            
            for j in range( novo_shape[1] ):
                pos_y = j / aumento

                for k in range( novo_shape[2] ):
                    img_escalada[i][j][k] = bilinear( img, pos_x, pos_y, k )

    return img_escalada

def dimensao_pos0__rot( vetor_x_r, vetor_y_r, angulo ):
    p0 = np.array( [ [0], [0] ] )
    p1 = vetor_x_r
    p2 = vetor_x_r + vetor_y_r
    p3 = vetor_y_r

    angulo = angulo % ( 2 * np.pi )
    if ( angulo < 0 ):
        angulo = angulo + ( 2 * np.pi )
    
    if ( angulo >= 0 and angulo < ( np.pi / 2 ) ):
        largura = abs( ( p2 - p0 )[0][0] )
        altura  = abs( ( p3 - p1 )[1][0] )

        pos_zero = np.array( [ [ p0[0][0] ], [ p1[1][0] ] ] )
        novo_shape = [ int( altura ), int( largura ), img.shape[2] ]

    elif ( angulo >= ( np.pi / 2 ) and angulo < np.pi ):
        largura = abs( ( p3 - p1 )[0][0] )
        altura  = abs( ( p2 - p0 )[1][0] )

        pos_zero = np.array( [ [ p1[0][0] ], [ p2[1][0] ] ] )
        novo_shape = [ int( altura ), int( largura ), img.shape[2] ]

    elif ( angulo >= np.pi and angulo < ( 3 * np.pi / 2 ) ):
        largura = abs( ( p2 - p0 )[0][0] )
        altura  = abs( ( p3 - p1 )[1][0] )

        pos_zero = np.array( [ [ p2[0][0] ], [ p3[1][0] ] ] )
        novo_shape = [ int( altura ), int( largura ), img.shape[2] ]

    elif ( angulo >= ( 3 * np.pi / 2 ) and angulo < ( 2 * np.pi ) ):
        largura = abs( ( p3 - p1 )[0][0] )
        altura  = abs( ( p2 - p0 )[1][0] )

        pos_zero = np.array( [ [ p3[0][0] ], [ p0[1][0] ] ] )
        novo_shape = [ int( altura ), int( largura ), img.shape[2] ]
    
    return pos_zero, novo_shape

def rotacao_proximo ( img, angulo ):
    matriz_rotacao = np.array( [ [ np.cos( angulo ), np.sin( angulo ) ], [ -np.sin( angulo ), np.cos( angulo ) ] ] )
    vetor_x = np.array( [ [ img.shape[1] ], [ 0 ] ] )
    vetor_y = np.array( [ [ 0 ], [ img.shape[0] ] ] )
    vetor_y_u = np.array( [ [ 0 ], [ 1 ] ] )

    vetor_x_r = matriz_rotacao @ vetor_x
    vetor_y_r = matriz_rotacao @ vetor_y
    matriz_rotacao_i = matriz_rotacao.transpose()

    soma = vetor_x_r + vetor_y_r
    dife = vetor_x_r - vetor_y_r

    pos_zero, novo_shape = dimensao_pos0__rot( vetor_x_r, vetor_y_r, angulo )
    
    img_rotacionada = np.zeros( novo_shape )

    for i in range( novo_shape[0] ):
        for j in range( novo_shape[1] ):
            pos = np.copy( pos_zero )

            pos[0][0] = pos[0][0] + j
            pos[1][0] = pos[1][0] + i

            pos_img = matriz_rotacao_i @ pos
            
            pos_x = mais_prox( pos_img[0][0] )
            pos_y = mais_prox( pos_img[1][0] )

            if ( pos_x >= 0 and pos_y >= 0 and pos_x < img.shape[1] and pos_y < img.shape[0] ):
                for k in range( novo_shape[2] ):
                    img_rotacionada[i][j][k] = img[pos_y][pos_x][k]

    return img_rotacionada

def rotacao_bilinear ( img, angulo ):
    matriz_rotacao = np.array( [ [ np.cos( angulo ), np.sin( angulo ) ], [ -np.sin( angulo ), np.cos( angulo ) ] ] )
    vetor_x = np.array( [ [ img.shape[1] ], [ 0 ] ] )
    vetor_y = np.array( [ [ 0 ], [ img.shape[0] ] ] )
    vetor_y_u = np.array( [ [ 0 ], [ 1 ] ] )

    vetor_x_r = matriz_rotacao @ vetor_x
    vetor_y_r = matriz_rotacao @ vetor_y
    matriz_rotacao_i = matriz_rotacao.transpose()

    soma = vetor_x_r + vetor_y_r
    dife = vetor_x_r - vetor_y_r

    pos_zero, novo_shape = dimensao_pos0__rot( vetor_x_r, vetor_y_r, angulo )
    
    img_rotacionada = np.zeros( novo_shape )

    for i in range( novo_shape[0] ):
        for j in range( novo_shape[1] ):
            pos = np.copy( pos_zero )

            pos[0][0] = pos[0][0] + j
            pos[1][0] = pos[1][0] + i

            pos_img = matriz_rotacao_i @ pos
            
            pos_x = pos_img[0][0]
            pos_y = pos_img[1][0]

            if ( pos_x >= 0 and pos_y >= 0 and pos_x < img.shape[1] and pos_y < img.shape[0] ):
                for k in range( novo_shape[2] ):
                    img_rotacionada[i][j][k] = bilinear( img, pos_y, pos_x, k )

    return img_rotacionada

if __name__ == "__main__":
    img_lida = gerais.ler_imagem( "pikachu.png" )
    
    if ( len( img_lida.shape ) != 3 ):
        img = np.zeros( [ img_lida.shape[0], img_lida.shape[1], 3 ] )
        for i in range( 3 ):
            img[ :, :, i ] = img_lida
    else:
        img = img_lida
    
    print( "Processando..." )
    #img = escala_proximo( img, 2.5 )
    #img = escala_bilinear( img, 0.45 )
    img = rotacao_proximo( img, ( ( 3 * np.pi / 4 ) ) )
    #img = rotacao_bilinear( img, ( ( -3 * np.pi / 4 ) ) )
    print( "Completo!" )

    gerais.mostrar_imagem( img )