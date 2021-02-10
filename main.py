import pygame
#from pygame.local import *

import numpy as np
import funcoes_proc_img as pi
import negativo as neg
import gamma
import linear_partes

def atualiza_tela ( I, tela, tamanho ):
    surface = pygame.surfarray.make_surface( 255 * I.transpose( 1, 0, 2 ) )
    surface = pygame.transform.scale( surface, tamanho )

    tela.fill( [ 0, 0, 0 ] )
    tela.blit( surface, [ 0, 0 ] )

def main ():
    tamanho = [ 0, 0 ]
    I = None

    while ( True ):
        opcao = -1

        while ( opcao < 0 or opcao > 4 ):
            print ( "Menu:" )

            print ( "-1: Sair\n"
                  + " 0: Abrir Imagem\n"
                  + " 1: Mostrar imagem\n"
                  + " 2: Negativo\n"
                  + " 3: Transformações logarítimicas\n"
                  + " 4: Correção de gama\n"
                  + " 5: Linear por partes\n" )

            opcao = int( input ( ": " ) )

            if ( opcao == -1 ):
                return

        if ( opcao == 0 ):
            caminho = input ( "Insira o caminho: " )
            I = pi.ler_imagem( caminho )

            tamanho = largura, altura = [ larg_t, int(larg_t * ( I.shape[0] / I.shape[1] ) ) ]
        elif ( opcao == 1 ):
            pi.mostrar_imagem( I )
        elif ( opcao == 2 ):
            I = neg.negativo( I )
        elif ( opcao == 3 ):
            valor = float( input ( "Insira o valor: " ) )
            I = pi.ler_imagem( "Imagens/Pinguim_1.jpg" )
        elif ( opcao == 4 ):
            valor = float( input ( "Insira o valor: " ) )
            I = gamma.correcao_gamma( I, valor )
        elif ( opcao == 5 ):
            I = pi.ler_imagem( "Imagens/Pinguim_1.jpg" )
        
        if not ( I is None ):
            atualiza_tela( I, tela, tamanho )

        pygame.display.flip()

        print ( "\n" )

if __name__ == "__main__":
    print ( "Programa de Processamento de Imagem - CK0167" )
    print ( "Alunos:\nCaleb de Sousa Vasconcelos\t- 399776\n"
          + "Ícaro da Silva Barbosa\t\t- 399002\n"
          + "\n" )
    
    pygame.init()

    tamanho_tela = larg_t, alt_t = [ 500, 500 ]

    tela = pygame.display.set_mode( tamanho_tela )

    main()