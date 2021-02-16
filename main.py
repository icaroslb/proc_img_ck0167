#from esteganografia import codificar_dados, decodificar_dados
import esteganografia
import pygame, sys
from pygame.locals import *
#from pygame.local import *

import threading
from threading import Thread

import numpy as np
import funcoes_proc_img as pi
import transformacao_log as t_log
import negativo as neg
import gamma
import linear_partes
import filtros

class Dados :
    def __init__ ( self ):
        self.I = None
        self.I_aux = None

        self.mostrar_I = True
        self.tamanho = None

        self.mutex = threading.Semaphore( 1 )

        self.rodar = True

class Console ( Thread ):
    def __init__ ( self, _dados ):
        Thread.__init__( self )
        self.dados = _dados
    
    def run ( self ):
        while ( True ):
            opcao = -1

            while ( opcao < 0 or opcao > 6 ):
                print ( "Menu:" )

                print ( "-1: Sair\n"
                      + " 0: Abrir Imagem\n"
                      + " 1: Negativo\n"
                      + " 2: Transformações logarítimicas\n"
                      + " 3: Correção de gama\n"
                      + " 4: Linear por partes\n"
                      + " 5: Filtros\n"
                      + " 6: Esteganografia\n")

                opcao = int( input ( ": " ) )

                if ( opcao == -1 ):
                    self.dados.rodar = False
                    return

            #Abrir imagem.
            if ( opcao == 0 ):
                caminho = input ( "Insira o caminho: " )

                esteg = esteganografia.Esteganografia(caminho)
                esteg.start()
                
                self.dados.mutex.acquire()
                
                self.dados.I = pi.ler_imagem( caminho )

                if ( self.dados.I.shape[1] > self.dados.I.shape[0] ):
                    self.dados.tamanho = largura, altura = [ int( larg_t / 2 ), int( ( larg_t / 2 ) * ( self.dados.I.shape[0] / self.dados.I.shape[1] ) ) ]
                else:
                    self.dados.tamanho = largura, altura = [ int( alt_t * ( self.dados.I.shape[1] / self.dados.I.shape[0] ) ), alt_t ]

                self.dados.mutex.release()
            elif ( opcao == 1 ):
                self.dados.mutex.acquire()

                self.dados.I = neg.negativo( self.dados.I )

                self.dados.mutex.release()
            elif ( opcao == 2 ):
                valor = float( input ( "Insira o valor: " ) )

                self.dados.mutex.acquire()

                self.dados.I = t_log.transform_log( self.dados.I, valor )

                self.dados.mutex.release()
            elif ( opcao == 3 ):
                valor = float( input ( "Insira o valor: " ) )

                self.dados.mutex.acquire()

                self.dados.I = gamma.correcao_gamma( self.dados.I, valor )

                self.dados.mutex.release()
            elif ( opcao == 4 ):
                linear_partes.terminal( self.dados, lin )
                lin.limpar()
            elif ( opcao == 5 ):
                filtros.terminal( self.dados )
            elif ( opcao == 6 ):
                esteganografia.codificar_dados( caminho )

            print ( "\n" )

    def terminar ( self ):
        self.rodar = False

def atualiza_tela ( I, tela, tamanho ):
    surface = pygame.surfarray.make_surface( 255 * I.transpose( 1, 0, 2 ) )
    surface = pygame.transform.scale( surface, tamanho )

    tela.blit( surface, [ 0, 0 ] )

def main ():
    dados = Dados()
    tr = Console( dados )
    tr.start()

    while ( dados.rodar ):
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT ):
                dados.rodar = False

        if ( pygame.mouse.get_pressed()[0] ):
            pos = np.array( pygame.mouse.get_pos() )
            lin.clique( pos )

        dados.mutex.acquire()

        tela.fill( [ 0, 0, 0 ] )
        
        if not ( dados.I is None ):
            atualiza_tela( dados.I, tela, dados.tamanho )

        dados.mutex.release()

        lin.run()
        
        pygame.display.update()

        pygame.event.wait( 500 )

    pygame.quit()
        

if __name__ == "__main__":
    print ( "Programa de Processamento de Imagem - CK0167" )
    print ( "Alunos:\nCaleb de Sousa Vasconcelos\t- 399776\n"
          + "Ícaro da Silva Barbosa\t\t- 399002\n"
          + "\n" )
    
    tamanho_tela = larg_t, alt_t = [ 1000, 500 ]

    pygame.init()

    tela = pygame.display.set_mode( tamanho_tela )
    pygame.display.set_caption('Processador de imagens')

    lin = linear_partes.Pontos( tela, tamanho_tela )

    main()