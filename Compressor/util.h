#ifndef UTIL_H
#define UTIL_H

#include <iostream>
#include <fstream>
#include <cstdint>
#include <cstring>
#include <vector>
#include <cmath>

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "stb_image.h"
#include "stb_image_write.h"


struct Pixel {
    union{
        uint8_t cores[3];
        struct {
            uint8_t r;
            uint8_t g;
            uint8_t b;
        };
    };
};

//================================================================================//

void transpor_img ( Pixel *img, int largura, int altura )
{
    Pixel *img_aux = new Pixel[ largura * altura ];

    memcpy( img_aux, img, largura * altura * sizeof( Pixel ) );

    for ( int i = 0; i < altura; i++ ) {
        for ( int j = 0; j < largura; j++ ) {
            img[ ( j * altura ) + i ] = img_aux[ j + ( i * largura ) ];
        }
    }

    delete [] img_aux;
}

//================================================================================//

void reposicionar_cores ( Pixel *array, int tamanho )
{
    uint8_t *novo_array = new uint8_t[ tamanho * 3 ];
    
    for ( int i = 0; i < tamanho; i++ ) {
        for ( int cor = 0; cor < 3; cor++ ) {
            novo_array[ ( cor * tamanho ) + i ] = array[ i ].cores[ cor ];
        }
    }

    memcpy( array, novo_array, tamanho * 3 );
    delete [] novo_array;
}

//================================================================================//

void reposicionar_cores_i ( uint8_t *array, int tamanho )
{
    Pixel *novo_array = new Pixel[ tamanho ];
    
    for ( int i = 0; i < tamanho; i++ ) {
        for ( int cor = 0; cor < 3; cor++ ) {
            novo_array[ i ].cores[ cor ] = array[ ( cor * tamanho ) + i ];
        }
    }

    memcpy( array, novo_array, tamanho * 3 );
    delete [] novo_array;
}

//================================================================================//

Pixel* abrir_bmp ( const char *nome_img, int *largura, int *altura, int *canais )
{
    return (Pixel*)stbi_load( nome_img, largura, altura, canais, 0 );
}

//================================================================================//

void salvar_bmp ( const char *nome_img, int largura, int altura, int canais, Pixel *img )
{
    stbi_write_bmp( nome_img, largura, altura, canais, img );
}

//================================================================================//

void salvar_compresso ( const char *nome_arquivo, uint8_t *dados, int largura, int altura, int tamanho )
{
    std::ofstream arquivo( nome_arquivo, std::ofstream::out | std::ofstream::trunc | std::ofstream::binary );

    arquivo.write( (char*)&largura, sizeof(int) );
    arquivo.write( (char*)&altura, sizeof(int) );
    arquivo.write( (char*)&tamanho, sizeof(int) );
       
    arquivo.write( (char*)dados, tamanho );

    arquivo.close();
}

//================================================================================//

uint8_t* abrir_compresso ( const char *nome_arquivo, int *largura, int *altura, int *tamanho )
{
    std::ifstream arquivo( nome_arquivo, std::ifstream::in | std::ifstream::binary );
    uint8_t *dados;

    arquivo.read( (char*)largura, sizeof(int) );
    arquivo.read( (char*)altura, sizeof(int) );
    arquivo.read( (char*)tamanho, sizeof(int) );

    dados = new uint8_t[ *tamanho ];
       
    arquivo.read( (char*)dados, *tamanho );

    arquivo.close();

    return dados;
}

//================================================================================//

template <class T>
void salvar_compresso ( const char *nome_arquivo, std::vector<T> &dados, int largura, int altura )
{
    int tamanho = dados.size();
    std::ofstream arquivo( nome_arquivo, std::ofstream::out | std::ofstream::trunc | std::ofstream::binary );

    arquivo.write( (char*)&largura, sizeof(int) );
    arquivo.write( (char*)&altura, sizeof(int) );
    arquivo.write( (char*)&tamanho, sizeof(int) );
    
    arquivo.write( (char*)dados.data(), tamanho * sizeof(T));

    arquivo.close();
}

//================================================================================//

template <class T>
void abrir_compresso ( const char *nome_arquivo, int *largura, int *altura, std::vector<T> &dados )
{
    std::ifstream arquivo( nome_arquivo, std::ifstream::in | std::ifstream::binary );
    uint8_t *retorno;
    int tamanho = 0;

    arquivo.read( (char*)largura, sizeof(int) );
    arquivo.read( (char*)altura, sizeof(int) );
    arquivo.read( (char*)&tamanho, sizeof(int) );
       
    retorno = new uint8_t [ tamanho * sizeof( T ) ];
    arquivo.read( (char*)retorno, tamanho * sizeof( T ) );
    dados = std::vector<T>( (T*)&retorno, ( (T*)&retorno ) + tamanho );
        
    delete [] retorno;
    arquivo.close();
}
#endif