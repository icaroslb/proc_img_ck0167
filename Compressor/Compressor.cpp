// Compressor.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//

#include <iostream>
#include "metodos_compressao.h"
#include "Huffman.h"
#include "Cod_preditiva.h"
#include "lzw.h"
#include "Run_length.h"
#include "Duplicador.h"

void comprimir_imagem ( const char *nome_img, const char *nome_comp );
void descomprimir_imagem ( const char *nome_comp, const char *nome_img );

int main()
{
       bool rodar = true;
       int opcao_escolhida;
       std::string arquivo_abrir;
       std::string arquivo_salvar;

       std::cout << "!!Bem vindo ao compressor!!"         << std::endl
                 << "Produzido por: "                     << std::endl
                 << "399776 - Caleb de Sousa Vasconcelos" << std::endl
                 << "399002 - Ícaro da Silva Barbosa"     << std::endl << std::endl;

       while ( rodar ) {
              do {
                     std::cout << " Menu:"           << std::endl
                               << "1 - Comprimir"    << std::endl
                               << "2 - Descomprimir" << std::endl
                               << ": ";
                     std::cin >> opcao_escolhida;
              } while( opcao_escolhida < 1 || opcao_escolhida > 2 );

              std::cout << std::endl << std::endl
                        << "Insira o arquivo que deseja abrir: ";
              std::cin >> arquivo_abrir;

              std::cout << std::endl << std::endl
                        << "Insira o arquivo que deseja salvar: ";
              std::cin >> arquivo_salvar;

              switch ( opcao_escolhida ) {
                     case 1: comprimir_imagem( arquivo_abrir.data(), arquivo_salvar.data() );    break;
                     case 2: descomprimir_imagem( arquivo_abrir.data(), arquivo_salvar.data() ); break;
                     default:                                                                    break;
              }

              break;
       }
       
       std::cout << "fim" << std::endl;
}

void comprimir_imagem ( const char *nome_img, const char *nome_comp )
{
       //Primeiro abre a imagem requerida
       int largura;
       int altura;
       int canais;
       int tamanho_huffman;

       Pixel *img = abrir_bmp( nome_img, &largura, &altura, &canais );

       uint8_t *huffman_dados_1;
       uint8_t *huffman_dados_2;

       //Aplica codificação preditiva nas linhas, colunas e entre as cores
       codificacao_preditiva( img, largura, altura );
       transpor_img( img, largura, altura );
       codificacao_preditiva( img, altura, largura );
       codificacao_preditiva_cores( img, altura, largura );

       //Aplica Huffman
       huffman_dados_1 = huffman( (uint8_t*)img, largura * altura * 3, &tamanho_huffman );
       huffman_dados_2 = huffman( huffman_dados_1, tamanho_huffman, &tamanho_huffman );

       //Salva o arquivo compresso
       salvar_compresso( nome_comp, huffman_dados_2, largura, altura, tamanho_huffman );

       //Libera a memória usada
       delete [] img;
       delete [] huffman_dados_1;
       delete [] huffman_dados_2;

       std::cout << largura * altura * 3 << " vs "<< tamanho_huffman << std::endl;
}

void descomprimir_imagem ( const char *nome_comp, const char *nome_img )
{
       int largura;
       int altura;
       int canais = 3;
       
       Pixel *img;
       uint8_t *huffman_dados_2;
       uint8_t *huffman_dados_1;
       
       int tamanho_huffman;

       //Abrir o arquivo compresso
       huffman_dados_2 = abrir_compresso( nome_comp, &largura, &altura, &tamanho_huffman );

       //Aplica Huffman
       huffman_dados_1 = huffman_i( huffman_dados_2, &tamanho_huffman );
       img = (Pixel*)huffman_i( huffman_dados_1, &tamanho_huffman );
       
       //Aplica codificação preditiva nas linhas, colunas e entre as cores
       codificacao_preditiva_cores_i( img, altura, largura );
       codificacao_preditiva_i( img, altura, largura );
       transpor_img( img, altura, largura );
       codificacao_preditiva_i( img, largura, altura );

       //Salva o arquivo bmp
       salvar_bmp( nome_img, largura, altura, canais, img );

       //Libera a memória usada
       delete [] huffman_dados_2;
       delete [] huffman_dados_1;
       delete [] img;
}

// Executar programa: Ctrl + F5 ou Menu Depurar > Iniciar Sem Depuração
// Depurar programa: F5 ou menu Depurar > Iniciar Depuração

// Dicas para Começar:
//   1. Use a janela do Gerenciador de Soluções para adicionar/gerenciar arquivos
//   2. Use a janela do Team Explorer para conectar-se ao controle do código-fonte
//   3. Use a janela de Saída para ver mensagens de saída do build e outras mensagens
//   4. Use a janela Lista de Erros para exibir erros
//   5. Ir Para o Projeto > Adicionar Novo Item para criar novos arquivos de código, ou Projeto > Adicionar Item Existente para adicionar arquivos de código existentes ao projeto
//   6. No futuro, para abrir este projeto novamente, vá para Arquivo > Abrir > Projeto e selecione o arquivo. sln
