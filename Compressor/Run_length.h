#ifndef RUN_LENGTH_H
#define RUN_LENGTH_H

#include <vector>
#include <cstdlib>
#include "util.h"

uint8_t* run_length ( uint8_t *dados, int tamanho, int *novo_tamanho = nullptr )
{
    std::vector<uint8_t> calculado;
    uint8_t *retorno;
    uint8_t qtd_repeticoes = 0;
    uint8_t num_repetido = dados[0];
    uint8_t num_lido;
    bool maior_255 = false;

    calculado.push_back( num_repetido );

    for ( int i = 0; i < tamanho; i++ ) {
        num_lido = dados[i];
        if ( num_repetido == num_lido ) {
            if ( qtd_repeticoes == 255 ) {
                maior_255 = true;
                calculado.push_back( qtd_repeticoes );
                qtd_repeticoes = 0;
            }
            qtd_repeticoes++;
        } else {
            calculado.push_back( qtd_repeticoes );
            if ( maior_255 || qtd_repeticoes == 255 ) {
                calculado.push_back( 0 );
                maior_255 = false;
            }

            num_repetido = num_lido;
            calculado.push_back( num_repetido );
        }
    }

    tamanho = calculado.size();
    retorno = new uint8_t[tamanho + 4];
    memcpy( retorno, &tamanho, 4 );

    memcpy( retorno + 4, calculado.data(), tamanho );

    if ( novo_tamanho != nullptr )
        *novo_tamanho = tamanho + 4;
    
    return retorno;
}

//================================================================================//

uint8_t* run_length_i ( uint8_t *dados, int *novo_tamanho = nullptr )
{
    std::vector<uint8_t> calculado;
    uint8_t *retorno;
    uint8_t num_repetido;
    int tamanho;
    bool maior_255 = false;

    memcpy( dados, &tamanho, 4 );
    tamanho += 4;

    int i = 4;
    while ( i < tamanho ) {
        num_repetido = dados[i++];
        calculado.push_back( num_repetido );

        if ( dados[i] == 255 )
            maior_255 = true;
        
        do {
            for ( int j = 0; j < dados[i]; j++ )
                calculado.push_back( num_repetido );
            
            i++;
        } while ( maior_255 && dados[i] != 0 );

        if ( maior_255 ) {
            maior_255 = false;
            i++;
        }
    }

    if ( novo_tamanho != nullptr )
        *novo_tamanho = calculado.size();
    
    retorno = new uint8_t[calculado.size()];
    memcpy( retorno, calculado.data(), calculado.size() );

    return retorno;
}

#endif