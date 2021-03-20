// Compressor.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//

#include <iostream>
#include "metodos_compressao.h"
#include "Huffman.h"
#include "Cod_preditiva.h"

int main()
{
       Pixel *img;
       uint8_t *c_huffman;
       Pixel *d_huffman;
       No_arvore *raiz;
       int largura;
       int altura;
       int canais;
       int tamanho;
       int tamanho_huffman_1;
       int tamanho_huffman_2;

       img = abrir_bmp( "benchmark.bmp", &largura, &altura, &canais );

       tamanho = largura * altura;

       codificacao_preditiva( img, largura, altura );
       transpor_img( img, largura, altura );
       codificacao_preditiva( img, altura, largura );

       c_huffman = huffman( (uint8_t*)img, tamanho * 3, &tamanho_huffman_1 );
       c_huffman = huffman( c_huffman, tamanho_huffman_1, &tamanho_huffman_2 );

       d_huffman = (Pixel*)huffman_i( c_huffman );
       d_huffman = (Pixel*)huffman_i( (uint8_t*)d_huffman );

       codificacao_preditiva_i( d_huffman, altura, largura );
       transpor_img( d_huffman, altura, largura );
       codificacao_preditiva_i( d_huffman, largura, altura );
       
       salvar_bmp( "teste.bmp", largura, altura, canais, d_huffman );
       std::cout << "fim" << std::endl;
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
