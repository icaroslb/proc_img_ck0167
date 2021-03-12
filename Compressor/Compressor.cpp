// Compressor.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include <iostream>
#include "stb_image.h"
#include "stb_image_write.h"
#include "metodos_compressao.h"

int main()
{
       //cimg_library::CImg<uint8_t> imagem( "benchmark.bmp" );

       Pixel *img;
       int largura;
       int altura;
       int canais;
       int tamanho; 

       img = (Pixel*)stbi_load( "benchmark.bmp", &largura, &altura, &canais, 0 );

       tamanho = largura * altura;

       wavelets_rgb_shift_rotativo( img, tamanho, 0 );
       wavelets_rgb_shift_rotativo( img, tamanho, 0 );
       wavelets_rgb_shift_rotativo( img, tamanho, 0 );
       wavelets_rgb_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_shift_rotativo( img, tamanho, 2 );
       wavelets_rgb_shift_rotativo( img, tamanho, 2 );
       wavelets_rgb_shift_rotativo( img, tamanho, 2 );
       
       wavelets_rgb_i_shift_rotativo( img, tamanho, 2 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 2 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 2 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 1 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 0 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 0 );
       wavelets_rgb_i_shift_rotativo( img, tamanho, 0 );

       transpor_img( img, largura, altura );
       transpor_img( img, altura, largura );
       
       stbi_write_bmp( "teste.bmp", largura, altura, canais, (char*)img );
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
