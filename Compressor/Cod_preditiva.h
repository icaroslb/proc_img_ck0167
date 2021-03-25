#ifndef COD_PRED_H
#define COD_PRED_H

#include "util.h"

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

void codificacao_preditiva ( uint8_t *dados, int tamanho )
{
    uint8_t *dados_cod = new uint8_t[ tamanho ];

    dados_cod[ tamanho ] = dados[ tamanho ];
    for ( int i = 1; i < tamanho; i++ ) {
        dados_cod[ i ] = dados[ i ] - dados[ i - 1 ];
    }

    memcpy( dados, dados_cod, ( tamanho * sizeof( uint8_t ) ) );

    delete [] dados_cod;
}

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

#endif