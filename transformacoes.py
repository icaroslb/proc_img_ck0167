import numpy as np
import gerais

def escala_proximo ( img, aumento ):
    novo_shape = [ int( img.shape[0] * aumento ), int( img.shape[1] * aumento ), img.shape[2] ]
    img_escalada = np.zeros( novo_shape )

    if ( aumento == 1 ):
        img_escalada = img
    else:
        for i in range( novo_shape[0] ):
            pos_x = int( i / aumento )

            for j in range( novo_shape[1] ):
                pos_y = int( j / aumento )

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
            pos_x_1 = int( pos_x )
            pos_x_2 = pos_x_1 + 1

            peso_x_1 = abs( pos_x - pos_x_2 )
            peso_x_2 = pos_x - pos_x_1
            if ( pos_x_2 >= img.shape[0] ):
                pos_x_2 = pos_x_1
                peso_x_2 = 0
            
            for j in range( novo_shape[1] ):
                pos_y = j / aumento
                pos_y_1 = int( pos_y )
                pos_y_2 = pos_y_1 + 1
                    
                peso_y_1 = abs( pos_y - pos_y_2 )
                peso_y_2 = pos_y - pos_y_1
                if ( pos_y_2 >= img.shape[1] ):
                    pos_y_2 = pos_y_1
                    peso_y_2 = 0

                for k in range( novo_shape[2] ):
                    media_1 = ( peso_x_1 * img[pos_x_1][pos_y_1][k] ) + ( peso_x_2 * img[pos_x_2][pos_y_1][k] )
                    media_2 = ( peso_x_1 * img[pos_x_1][pos_y_2][k] ) + ( peso_x_2 * img[pos_x_2][pos_y_2][k] )

                    img_escalada[i][j][k] = ( peso_y_1 * media_1 ) + ( peso_y_2 * media_2 )

    return img_escalada

def rotacao_proximo ( img, angulo ):
    novo_shape = [ int( img.shape[0] * aumento ), int( img.shape[1] * aumento ), img.shape[2] ]
    img_escalada = np.zeros( novo_shape )

    if ( aumento == 1 ):
        img_escalada = img
    else:
        for i in range( novo_shape[0] ):
            pos_x = int( i / aumento )

            for j in range( novo_shape[1] ):
                pos_y = int( j / aumento )

                for k in range( novo_shape[2] ):
                    img_escalada[i][j][k] = img[pos_x][pos_y][k]

    return img_escalada

if __name__ == "__main__":
    img_lida = gerais.ler_imagem( "pikachu.png" )
    
    if ( len( img_lida.shape ) != 3 ):
        img = np.zeros( [ img_lida.shape[0], img_lida.shape[1], 3 ] )
        for i in range( 3 ):
            img[ :, :, i ] = img_lida
    else:
        img = img_lida
    
    print( "Processando..." )
    img = escala_proximo( img, 2.5 )
    #img = escala_bilinear( img, 0.45 )
    print( "Completo!" )

    gerais.mostrar_imagem( img )