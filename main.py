#from esteganografia import codificar_dados, decodificar_dados
import esteganografia
import pygame, sys
from pygame.locals import *
#from pygame.local import *

import threading
from threading import Thread

import numpy as np
import gerais as ge
import transformacao_log as t_log
import negativo as neg
import gamma
import linear_partes
import filtros

class Dados :
    def __init__ ( self, caminho ):
        self.caminho = caminho

        self.I = ge.ler_imagem( caminho )
        self.I_aux = None

        self.mostrar_I = True
        self.tamanho = None

        #self.mutex = threading.Semaphore( 1 )

        if ( self.I.shape[1] > self.I.shape[0] ):
            self.tamanho = largura, altura = [ int( larg_t / 2 ), int( ( larg_t / 2 ) * ( self.I.shape[0] / self.I.shape[1] ) ) ]
        else:
            self.tamanho = largura, altura = [ int( alt_t * ( self.I.shape[1] / self.I.shape[0] ) ), alt_t ]
        
        #Se for cinza, converte pra colorido
        if ( len( self.I.shape ) == 2 ):
            zeros = np.zeros( [ self.I.shape[0], self.I.shape[1], 3 ] )
            for i in range( 3 ):
                zeros[ :, :, i ] = self.I
            
            self.I = zeros

class Console ( Thread ):
    def __init__ ( self ):
        Thread.__init__( self )
        
    
    def run ( self ):
        global dados
        global rodar
        global mutex

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
                    rodar = False
                    return

            #Abrir imagem.
            if ( opcao == 0 ):
                caminho = input ( "Insira o caminho: " )

                esteg = esteganografia.Esteganografia(caminho)
                esteg.start()
                
                mutex.acquire()
                
                #self.dados = ge.ler_imagem( self, caminho )
                dados = Dados( caminho )


                mutex.release()
            elif ( opcao == 1 ):
                mutex.acquire()

                dados.I = neg.negativo( dados.I )

                mutex.release()
            elif ( opcao == 2 ):
                valor = float( input ( "Insira o valor: " ) )

                mutex.acquire()

                dados.I = t_log.transform_log( dados.I, valor )

                mutex.release()
            elif ( opcao == 3 ):
                valor = float( input ( "Insira o valor: " ) )

                mutex.acquire()

                dados.I = gamma.correcao_gamma( dados.I, valor )

                mutex.release()
            elif ( opcao == 4 ):
                linear_partes.terminal( dados, lin, mutex )
                lin.limpar()
            elif ( opcao == 5 ):
                filtros.terminal( dados, mutex )
            elif ( opcao == 6 ):
                esteganografia.codificar_dados( caminho )

            print ( "\n" )

    def terminar ( self ):
        rodar = False

def atualiza_tela ( I, tela, tamanho ):
    img_mostrar = I.transpose( 1, 0, 2 )

    surface = pygame.surfarray.make_surface( 255 * img_mostrar )
    
    surface = pygame.transform.scale( surface, tamanho )

    tela.blit( surface, [ 0, 0 ] )

def main ():
    #dados = Dados()
    #tr = Console( dados )

    global dados
    global rodar
    global mutex

    tr = Console()
    tr.start()

    clock = pygame.time.Clock()

    while ( rodar ):
        for event in pygame.event.get():
            if ( event.type == pygame.QUIT ):
                rodar = False

        if ( pygame.mouse.get_pressed()[0] ):
            pos = np.array( pygame.mouse.get_pos() )
            lin.clique( pos )

        tela.fill( [ 0, 0, 0 ] )

        if not ( dados is None ):
            mutex.acquire()

            if not ( dados.I is None ):
                atualiza_tela( dados.I, tela, dados.tamanho )

            mutex.release()

        lin.run()
        
        pygame.display.update()

        #pygame.event.wait( 500 )
        clock.tick( 30 )

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

    dados = None
    rodar = True
    mutex = threading.Semaphore( 1 )

    main()