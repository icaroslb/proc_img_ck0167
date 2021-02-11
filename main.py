import pygame
#from pygame.local import *

import threading
from threading import Thread

import numpy as np
import funcoes_proc_img as pi
import transformacao_log as t_log
import negativo as neg
import gamma
import linear_partes

class Dados :
    def __init__ ( self ):
        self.I = None
        self.I_aux = None

        self.mostrar_I = True
        self.tamanho = None

        self.mutex = threading.Semaphore( 1 )

class Tela ( Thread ):
    def __init__ ( self, _dados, _tela ):
        Thread.__init__( self )
        self.dados = _dados
        self.tela = _tela

        self.rodar = True
    
    def run ( self ):
        while ( self.rodar ):

            self.dados.mutex.acquire()
            
            if not ( self.dados.I is None ):
                atualiza_tela( self.dados.I, self.tela, self.dados.tamanho )

            self.dados.mutex.release()

            pygame.display.flip()
    
    def terminar ( self ):
        self.rodar = False

def atualiza_tela ( I, tela, tamanho ):
    surface = pygame.surfarray.make_surface( 255 * I.transpose( 1, 0, 2 ) )
    surface = pygame.transform.scale( surface, tamanho )

    tela.fill( [ 0, 0, 0 ] )
    tela.blit( surface, [ 0, 0 ] )

def main ():
    dados = Dados()
    tr = Tela( dados, tela )
    tr.start()

    while ( True ):
        opcao = -1

        while ( opcao < 0 or opcao > 4 ):
            print ( "Menu:" )

            print ( "-1: Sair\n"
                  + " 0: Abrir Imagem\n"
                  + " 1: Negativo\n"
                  + " 2: Transformações logarítimicas\n"
                  + " 3: Correção de gama\n"
                  + " 4: Linear por partes\n" )

            opcao = int( input ( ": " ) )

            if ( opcao == -1 ):
                tr.terminar()
                return

        if ( opcao == 0 ):
            caminho = input ( "Insira o caminho: " )
            
            dados.mutex.acquire()
            
            dados.I = pi.ler_imagem( caminho )
            dados.tamanho = largura, altura = [ larg_t, int(larg_t * ( dados.I.shape[0] / dados.I.shape[1] ) ) ]

            dados.mutex.release()
        elif ( opcao == 1 ):
            dados.mutex.acquire()

            dados.I = neg.negativo( dados.I )

            dados.mutex.release()
        elif ( opcao == 2 ):
            valor = float( input ( "Insira o valor: " ) )

            dados.mutex.acquire()

            dados.I = t_log.transform_log( dados.I, valor )

            dados.mutex.release()
        elif ( opcao == 3 ):
            valor = float( input ( "Insira o valor: " ) )

            dados.mutex.acquire()

            dados.I = gamma.correcao_gamma( dados.I, valor )

            dados.mutex.release()
        elif ( opcao == 4 ):
            dados.I = pi.ler_imagem( "Imagens/Pinguim_1.jpg" )

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