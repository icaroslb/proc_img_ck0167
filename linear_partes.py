import numpy as np
import pygame

class Pontos:
    def __init__ ( self, _tela, _dime ):
        self.pontos = [ np.array( [0, 0] ), np.array( [255, 255] ) ]
        self.tela = _tela
        self.dim = np.array( [_dime[0] / 2, _dime[1] ] )

    def run ( self ):
        for i in self.pontos:
            pos = np.array( [ self.dim[0] + ( i[0] * self.dim[0] / 255  )
                            , self.dim[1] - ( i[1] * self.dim[1] / 255  ) ] )
            pygame.draw.circle( self.tela, [255, 255, 255], pos, 5 )

        pos_2 = np.array( [ self.dim[0] + ( self.pontos[0][0] * self.dim[0] / 255  )
                          , self.dim[1] - ( self.pontos[0][1] * self.dim[1] / 255  ) ] )
        for i in range( 1, len( self.pontos ) ):
            pos_1 = pos_2
            pos_2 = np.array( [ self.dim[0] + ( self.pontos[i][0] * self.dim[0] / 255  )
                              , self.dim[1] - ( self.pontos[i][1] * self.dim[1] / 255  ) ] )

            pygame.draw.line( self.tela, [255, 255, 255], pos_1, pos_2 )

    def clique ( self, pos ):
        if ( pos[0] >= self.dim[0] ):
            pos[0] = pos[0] - self.dim[0]

            self.pontos.append( np.array( [ int( ( pos[0] / self.dim[0] ) * 255 )
                                          , int( ( ( self.dim[1] - pos[1] ) / self.dim[1] ) * 255 ) ] ) )
            self.pontos.sort( key = pos_x )

    def limpar ( self ):
        self.pontos = [ np.array( [0, 0] ), np.array( [255, 255] ) ]

def pos_x ( ponto ):
    return ponto[0]

def linear_partes ( M, pontos ):
    qtd_pontos = len( pontos )
    tam_img = M.shape
    pts = pontos

    for i in range( 0, len( pts ) ):
        pts[i] = pts[i] / 255

    if ( pts[0][0] == pts[1][0] ):
        del pts[0]

    ultimo = len( pts ) - 1
    if ( pts[ultimo][0] == pts[ultimo - 1][0] ):
        del pts[pts]
    
    for i in range( tam_img[0] ):
        for j in range( tam_img[1] ):
            for k in range( tam_img[2] ):
                cor = M[i][j][k]
                nova_cor = 0
                
                l = 1
                while ( l < ( qtd_pontos - 1 ) and ( cor > pontos[l][0] ) ):
                    l += 1
                
                if ( pontos[l][0] == cor ):
                    nova_cor = pontos[l][1]
                else:
                    vetor = pontos[l] - pontos[l-1]
                    tam = vetor[0]
                    dist = cor - pontos[l-1][0]
                    
                    novo_ponto = pontos[l-1] + ( vetor * ( dist / tam ) )
                    
                    nova_cor = novo_ponto[1]
                
                M[i][j][k] = nova_cor
    
    return M

def terminal ( dados, pontos ):
    while ( True ):
        aplicar = input( "Aplicar? (S/N): " )

        if ( aplicar == "S" or aplicar == "s" ):
            dados.mutex.acquire()
            print( "Processando..." )
            dados.I = linear_partes( dados.I, pontos.pontos )
            print( "Completo" )

            dados.mutex.release()
            
            return
        elif ( aplicar == "N" or aplicar == "n" ):
            return
        else:
            print( "Opção inválida!\n" )

if __name__ == "__main__":
    M = np.array( [[[0.5], [0.2]], [[0.3], [1.0]]] )
    
    M = linear_partes( M, [np.array([0, 0.2]), np.array([1, 0.8]), np.array([0.5, 1.0])] )
    
    print( M )