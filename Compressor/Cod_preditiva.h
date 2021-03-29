#ifndef COD_PRED_H
#define COD_PRED_H

#include "util.h"

struct Inteiro {
    union {
        struct {
            uint8_t c1;
            uint8_t c2;
            uint8_t c3;
            uint8_t c4;
        };
        uint8_t c[4];
        int num;
    };
};

//================================================================================//

void codificacao_preditiva ( Pixel *dados, int largura, int altura )
{
    Pixel *dados_cod = new Pixel[ largura * altura ];

    for ( int i = 0; i < altura; i++ ) {
        dados_cod[ largura * i ] = dados[ largura * i ];
        for ( int j = 1; j < largura; j++ ) {
            for ( int cor = 0; cor < 3; cor++ )
                dados_cod[ j + ( largura * i ) ].cores[cor] = dados[ j + ( largura * i ) ].cores[cor] - dados[ ( j - 1 ) + ( largura * i ) ].cores[cor];
        }
    }

    memcpy( dados, dados_cod, ( largura * altura * sizeof( Pixel ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva_i ( Pixel *dados, int largura, int altura )
{
    Pixel *dados_cod = new Pixel[ largura * altura ];

    for ( int i = 0; i < altura; i++ ) {
        dados_cod[ largura * i ] = dados[ largura * i ];
        for ( int j = 1; j < largura; j++ ) {
            for ( int cor = 0; cor < 3; cor++ )
                dados_cod[ j + ( largura * i ) ].cores[cor] = dados[ j + ( largura * i ) ].cores[cor] + dados_cod[ ( j - 1 ) + ( largura * i ) ].cores[cor];
        }
    }

    memcpy( dados, dados_cod, ( largura * altura * sizeof( Pixel ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva_cores ( Pixel *dados, int largura, int altura )
{
    Pixel *dados_cod = new Pixel[ largura * altura ];

    for ( int i = 0; i < altura; i++ ) {
        for ( int j = 0; j < largura; j++ ) {
            dados_cod[ j + ( largura * i ) ].r = dados[ j + ( largura * i ) ].r;
            for ( int cor = 1; cor < 3; cor++ )
                dados_cod[ j + ( largura * i ) ].cores[ cor ] = dados[ j + ( largura * i ) ].cores[ cor ] - dados[ j + ( largura * i ) ].cores[ cor - 1 ];
        }
    }

    memcpy( dados, dados_cod, ( largura * altura * sizeof( Pixel ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva_cores_i ( Pixel *dados, int largura, int altura )
{
    Pixel *dados_cod = new Pixel[ largura * altura ];

    for ( int i = 0; i < altura; i++ ) {
        for ( int j = 0; j < largura; j++ ) {
            dados_cod [j + ( largura * i ) ].r = dados[ j + ( largura * i ) ].r;
            for ( int cor = 1; cor < 3; cor++ )
                dados_cod[ j + ( largura * i ) ].cores[ cor ] = dados[ j + ( largura * i ) ].cores[ cor ] + dados_cod[ j + ( largura * i ) ].cores[ cor - 1];
        }
    }

    memcpy( dados, dados_cod, ( largura * altura * sizeof( Pixel ) ) );

    delete [] dados_cod;
}
//================================================================================//

void codificacao_preditiva ( uint8_t *dados, int tamanho )
{
    uint8_t *dados_cod = new uint8_t[ tamanho ];

    dados_cod[ 0 ] = dados[ 0 ];
    for ( int i = 1; i < tamanho; i++ ) {
        dados_cod[ i ] = dados[ i ] - dados[ i - 1 ];
    }

    memcpy( dados, dados_cod, ( tamanho * sizeof( uint8_t ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva_i ( uint8_t *dados, int tamanho )
{
    uint8_t *dados_cod = new uint8_t[ tamanho ];

    dados_cod[ 0 ] = dados[ 0 ];
    for ( int i = 1; i < tamanho; i++ ) {
        dados_cod[ i ] = dados[ i ] + dados_cod[ i - 1 ];
    }

    memcpy( dados, dados_cod, ( tamanho * sizeof( uint8_t ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva ( Inteiro *dados, int tamanho )
{
    Inteiro *dados_cod = new Inteiro[ tamanho ];

    dados_cod[ 0 ] = dados[ 0 ];
    for ( int i = 1; i < tamanho; i++ ) {
        for ( int c = 0; c < 4; c++ )
            dados_cod[ i ].c[ c ] = dados[ i ].c[ c ] - dados[ i - 1 ].c[ c ];
    }

    memcpy( dados, dados_cod, ( tamanho * sizeof( Inteiro ) ) );

    delete [] dados_cod;
}

//================================================================================//

void codificacao_preditiva_i ( Inteiro *dados, int tamanho )
{
    Inteiro *dados_cod = new Inteiro[ tamanho ];

    dados_cod[ 0 ] = dados[ 0 ];
    for ( int i = 1; i < tamanho; i++ ) {
        for ( int c = 0; c < 4; c++ )
            dados_cod[ i ].c[ c ] = dados[ i ].c[ c ] + dados_cod[ i - 1 ].c[ c ];
    }

    memcpy( dados, dados_cod, ( tamanho * sizeof( Inteiro ) ) );

    delete [] dados_cod;
}

#endif