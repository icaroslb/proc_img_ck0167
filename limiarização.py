import numpy as np
from gerais import ler_imagem, mostrar_imagem

def limiarizar(dados, tamanho):

    limiar = np.double(input("Insira um valor real entre 0 e 1 para servir de limiar: "))
    image = ler_imagem(dados.I)/255

    M_aux = np.copy( dados.I )
    dim = M_aux.shape

    matriz_zero = np.zeros( [ dim[0] + ( 2 * tamanho ), dim[1] + ( 2 * tamanho ), dim[2] ] )
    matriz_zero[ tamanho : dim[0] + tamanho, tamanho : dim[0] + tamanho, :] = M_aux
    M_aux = matriz_zero

    for i, value in enumerate(matriz_zero):
        if value < limiar:
            matriz_zero[i] = 0
        else:
            matriz_zero[i] = 1

    mostrar_imagem(matriz_zero)

limiarizar("pikachu.png")
