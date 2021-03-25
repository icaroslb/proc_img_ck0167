// Compressor.cpp : Este arquivo contém a função 'main'. A execução do programa começa e termina ali.
//

#include <iostream>
#include "metodos_compressao.h"
#include "Huffman.h"
#include "Cod_preditiva.h"
#include "lzw.h"

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "stb_image.h"
#include "stb_image_write.h"

Pixel* abrir_bmp ( char *nome_img, int *largura_retorno, int *altura_retorno );
void salvar_bmp ( char *nome_img, int largura, int altura, int canais, Pixel *img );

std::vector<int> comprimir_imagem (char *nome_img, int *largura_retorno, int *altura_retorno );
void descomprimir_imagem ( char *nome_img, std::vector<int> dados_compressos, int largura, int altura );

uint8_t* comprimir_imagem_2 (char *nome_img, int *largura_retorno, int *altura_retorno, int *novo_tamanho );
void descomprimir_imagem_2 ( char *nome_img, uint8_t* dados_compressos, int largura, int altura );

uint8_t* comprimir_imagem_3 (char *nome_img, int *largura_retorno, int *altura_retorno, int *novo_tamanho );
void descomprimir_imagem_3 ( char *nome_img, uint8_t* dados_compressos, int largura, int altura );

int main()
{
       std::vector<int> dados_compressos;
       uint8_t *dados_compressos_2;
       int largura;
       int altura;
       int tamanho_2;

       dados_compressos = comprimir_imagem( "benchmark.png", &largura, &altura );
       std::cout << "Compressor 1: " << largura * altura * 3 << " vs " << dados_compressos.size() << std::endl;
       descomprimir_imagem( "teste_1.bmp", dados_compressos, largura, altura );

       dados_compressos_2 = comprimir_imagem_2( "benchmark.png", &largura, &altura, &tamanho_2 );
       std::cout << "Compressor 2: " << largura * altura * 3 << " vs " << tamanho_2 << std::endl;
       descomprimir_imagem_2( "teste_2.bmp", dados_compressos_2, largura, altura );
       delete [] dados_compressos_2;

       dados_compressos_2 = comprimir_imagem_3( "benchmark.png", &largura, &altura, &tamanho_2 );
       std::cout << "Compressor 3: " << largura * altura * 3 << " vs " << tamanho_2 << std::endl;
       descomprimir_imagem_3( "teste_3.bmp", dados_compressos_2, largura, altura );
       delete [] dados_compressos_2;
       
       std::cout << "fim" << std::endl;
}

Pixel* abrir_bmp ( char *nome_img, int *largura, int *altura, int *canais )
{
    return (Pixel*)stbi_load( nome_img, largura, altura, canais, 0 );
}

void salvar_bmp ( char *nome_img, int largura, int altura, int canais, Pixel *img )
{
    stbi_write_bmp( nome_img, largura, altura, canais, img );
}

std::vector<int> comprimir_imagem ( char *nome_img, int *largura_retorno, int *altura_retorno )
{
       //Primeiro abre a imagem requerida
       int largura;
       int altura;
       int canais;
       int tamanho_huffman;
       Pixel *img = abrir_bmp( nome_img, &largura, &altura, &canais );
       uint8_t *huffman_dados;
       std::string dados_string;
       std::vector<int> dados_compressos;

       //Faz a codificação preditiva nas linhas e nas colunas da imagem
       codificacao_preditiva( img, largura, altura );
       transpor_img( img, largura, altura );
       codificacao_preditiva( img, altura, largura );

       //Faz duas vezes o huffman
       huffman_dados = huffman( (uint8_t*)img, largura * altura * 3, &tamanho_huffman );
       huffman_dados = huffman( huffman_dados, tamanho_huffman, &tamanho_huffman );

       //Faz o lzw
       dados_string = std::string( (char*)huffman_dados, (char*)(huffman_dados + tamanho_huffman) );
       dados_compressos = lzwCompressor( dados_string );

       //Salva o arquivo compresso

       *largura_retorno = largura;
       *altura_retorno = altura;

       return dados_compressos;
}

void descomprimir_imagem ( char *nome_img, std::vector<int> dados_compressos, int largura, int altura )
{
       //int largura;
       //int altura;
       int canais = 3;
       Pixel *img;
       uint8_t *huffman_dados;
       std::string dados_string;
       //std::vector<int> dados_compressos;

       //Abrir o arquivo compresso

       //Faz a inversa do lzw
       dados_string = lzwDescompressor( dados_compressos );

       huffman_dados = huffman_i( (uint8_t*)dados_string.data() );
       img = (Pixel*)huffman_i( huffman_dados );

       codificacao_preditiva_i( img, altura, largura );
       transpor_img( img, altura, largura );
       codificacao_preditiva_i( img, largura, altura );

       salvar_bmp( nome_img, largura, altura, canais, img );
}

uint8_t* comprimir_imagem_2 ( char *nome_img, int *largura_retorno, int *altura_retorno, int *novo_tamanho )
{
       //Primeiro abre a imagem requerida
       int largura;
       int altura;
       int canais;
       int tamanho_huffman;
       char *img_char;
       Pixel *img = abrir_bmp( nome_img, &largura, &altura, &canais );
       uint8_t *huffman_dados;
       std::string dados_string;
       std::vector<int> dados_compressos;

       //Faz a codificação preditiva nas linhas e nas colunas da imagem
       codificacao_preditiva( img, largura, altura );
       transpor_img( img, largura, altura );
       codificacao_preditiva( img, altura, largura );

       //Faz o lzw
       img_char = (char*)img;
       dados_string = std::string( img_char, img_char + ( largura * altura * 3 ) );
       dados_compressos = lzwCompressor( dados_string );

       //Faz duas vezes o huffman
       huffman_dados = new uint8_t [ dados_compressos.size() * sizeof(int) ];
       memcpy( huffman_dados, dados_compressos.data(), dados_compressos.size() * sizeof(int) );
       huffman_dados = huffman( (uint8_t*)huffman_dados, dados_compressos.size() * sizeof(int), &tamanho_huffman );

       //Salva o arquivo compresso

       *largura_retorno = largura;
       *altura_retorno = altura;

       *novo_tamanho = tamanho_huffman;

       return huffman_dados;
}

void descomprimir_imagem_2 ( char *nome_img, uint8_t* huffman_dados, int largura, int altura )
{
       //int largura;
       //int altura;
       int canais = 3;
       Pixel *img;
       //uint8_t *huffman_dados;
       int *huffman_dados_int;
       int tamanho_huffman;
       std::string dados_string;
       std::vector<int> dados_compressos;

       //Abrir o arquivo compresso

       huffman_dados_int = (int*)huffman_i( huffman_dados, &tamanho_huffman );

       //Faz a inversa do lzw
       dados_compressos = std::vector<int>( huffman_dados_int, huffman_dados_int + ( tamanho_huffman / sizeof(int) ) );
       dados_string = lzwDescompressor( dados_compressos );

       img = (Pixel*) new uint8_t [ dados_string.size() ];
       memcpy( img, dados_string.data(), dados_string.size() );
       codificacao_preditiva_i( img, altura, largura );
       transpor_img( img, altura, largura );
       codificacao_preditiva_i( img, largura, altura );

       salvar_bmp( nome_img, largura, altura, canais, img );

       delete [] img;
}

uint8_t* comprimir_imagem_3 ( char *nome_img, int *largura_retorno, int *altura_retorno, int *novo_tamanho )
{
       //Primeiro abre a imagem requerida
       int largura;
       int altura;
       int canais;
       int tamanho_huffman;
       char *img_char;
       Pixel *img = abrir_bmp( nome_img, &largura, &altura, &canais );
       uint8_t *huffman_dados;
       std::string dados_string;
       std::vector<int> dados_compressos;

       //Faz a codificação preditiva nas linhas e nas colunas da imagem
       codificacao_preditiva( img, largura, altura );
       transpor_img( img, largura, altura );
       codificacao_preditiva( img, altura, largura );

       //Faz o lzw
       img_char = (char*)img;
       dados_string = std::string( img_char, img_char + ( largura * altura * 3 ) );
       dados_compressos = lzwCompressor( dados_string );

       //Faz duas vezes o huffman
       huffman_dados = new uint8_t [ dados_compressos.size() * sizeof(int) ];
       memcpy( huffman_dados, dados_compressos.data(), dados_compressos.size() * sizeof(int) );
       huffman_dados = huffman( (uint8_t*)huffman_dados, dados_compressos.size() * sizeof(int), &tamanho_huffman );
       huffman_dados = huffman( (uint8_t*)huffman_dados, tamanho_huffman, &tamanho_huffman );

       //Salva o arquivo compresso

       *largura_retorno = largura;
       *altura_retorno = altura;

       *novo_tamanho = tamanho_huffman;

       return huffman_dados;
}

void descomprimir_imagem_3 ( char *nome_img, uint8_t* huffman_dados, int largura, int altura )
{
       //int largura;
       //int altura;
       int canais = 3;
       Pixel *img;
       //uint8_t *huffman_dados;
       int *huffman_dados_int;
       int tamanho_huffman;
       std::string dados_string;
       std::vector<int> dados_compressos;

       //Abrir o arquivo compresso

       huffman_dados_int = (int*)huffman_i( huffman_dados );
       huffman_dados_int = (int*)huffman_i( (uint8_t*)huffman_dados_int, &tamanho_huffman );

       //Faz a inversa do lzw
       dados_compressos = std::vector<int>( huffman_dados_int, huffman_dados_int + ( tamanho_huffman / sizeof(int) ) );
       dados_string = lzwDescompressor( dados_compressos );

       img = (Pixel*) new uint8_t [ dados_string.size() ];
       memcpy( img, dados_string.data(), dados_string.size() );
       codificacao_preditiva_i( img, altura, largura );
       transpor_img( img, altura, largura );
       codificacao_preditiva_i( img, largura, altura );

       salvar_bmp( nome_img, largura, altura, canais, img );

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
