import numpy as np

def pos_x ( ponto ):
    return ponto[0]

def linear_partes ( M, pontos ):
    qtd_pontos = len( pontos )
    tam_img = M.shape
    pontos.sort( key = pos_x )
    
    for i in range( tam_img[0] ):
        for j in range( tam_img[1] ):
            for k in range( tam_img[2] ):
                cor = M[i, j, k]
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
                
                M[i, j, k] = nova_cor
    
    return M

if __name__ == "__main__":
    M = np.array( [[[0.5], [0.2]], [[0.3], [1.0]]] )
    
    M = linear_partes( M, [np.array([0, 0.2]), np.array([1, 0.8]), np.array([0.5, 1.0])] )
    
    print( M )


