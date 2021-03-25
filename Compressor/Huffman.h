#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <map>
#include <vector>
#include <algorithm>
#include "util.h"

struct No_arvore {
    union {
        struct {
            int repeticao;
            uint8_t cor;
        };
        uint8_t dados[5];
    };
    int id;

    struct No_arvore *pai;
    struct No_arvore *filho_e;
    struct No_arvore *filho_d;

    No_arvore ( uint8_t cor, int repeticao, int id, struct No_arvore *pai, struct No_arvore *filho_e, struct No_arvore *filho_d )
    : cor( cor )
    , repeticao( repeticao )
    , id( id )
    , pai( pai )
    , filho_e( filho_e )
    , filho_d( filho_d )
    {}
};

No_arvore* proximo_no ( No_arvore *no )
{
    No_arvore *anterior;

    if ( no->filho_d != nullptr ) {
        no = no->filho_d;
        while ( no->filho_e != nullptr )
            no = no->filho_e;
    } else {
        do {
            anterior = no;
            no = no->pai;
        } while ( no != nullptr && no->filho_d == anterior );
    }

    return no;
}

No_arvore* constuir_arvore ( std::vector< No_arvore* > &vetor )
{
    No_arvore *novo_no;
    No_arvore *no_e;
    No_arvore *no_d;
    
    while ( vetor.size() > 1 ) {
        std::sort( vetor.begin(), vetor.end(), []( No_arvore* n_1, No_arvore* n_2 ) { return n_1->repeticao > n_2->repeticao; } );
        
        no_e = vetor.back();
        vetor.pop_back();
        no_d = vetor.back();
        vetor.pop_back();

        novo_no = new No_arvore( 0, no_e->repeticao + no_d->repeticao, 0, nullptr, no_e, no_d );
        no_e->pai = novo_no;
        no_d->pai = novo_no;

        vetor.push_back( novo_no );
    }

    return vetor[0];
}

void percorrer_arvore ( No_arvore *raiz, std::map< uint8_t, int > &id_cor )
{
    No_arvore *percorrer = raiz;
    No_arvore *anterior;
    int id = 0;

    while ( percorrer->filho_e != nullptr )
        percorrer = percorrer->filho_e;

    while ( percorrer != nullptr ) {
        percorrer->id = id++;
        if ( percorrer->filho_d == nullptr && percorrer->filho_e == nullptr )
            id_cor.insert( std::pair< uint8_t, int >( percorrer->cor, percorrer->id ) );

        percorrer = proximo_no( percorrer );
    }
}

void deletar_arvore ( No_arvore *raiz )
{
    No_arvore *deletar;

    while ( raiz->filho_e != nullptr )
        raiz = raiz->filho_e;

    while ( raiz != nullptr ) {

        if ( raiz->filho_d != nullptr ) {
            raiz = raiz->filho_d;
            while ( raiz->filho_e != nullptr )
                raiz = raiz->filho_e;
        } else {
            do {
                deletar = raiz;
                raiz = raiz->pai;

                delete deletar;
            } while ( raiz != nullptr && raiz->filho_d == deletar );
        }

    }
}

uint8_t* huffman ( uint8_t *dados, int tamanho, int *novo_tamanho = nullptr )
{
    std::map< uint8_t, int > qtd_cor;

    //calcula a quantidade de vezes que cada cor aparece
    for ( int i = 0; i < tamanho; i++ ) {
            try {
                qtd_cor.at( dados[i] )++;
            } catch ( const std::out_of_range& oor ) {
                qtd_cor[ dados[i] ] = 1;
            }
    }

    std::vector< uint8_t > dados_retorno;
    std::vector< No_arvore* > ordem_no;
    No_arvore *raiz;
    int pos_vetor = 0;

    //Inicializa o vetor com um nó pra cada cor
    dados_retorno.reserve( ( qtd_cor.size() * 5 ) + 4 );
    ordem_no.reserve( qtd_cor.size() );
    for ( auto i = qtd_cor.begin(); i != qtd_cor.end(); i++ ) {
        ordem_no.push_back( new No_arvore( i->first, i->second, 0, nullptr, nullptr, nullptr ) );

        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );

        memcpy( &dados_retorno.data()[ pos_vetor ], &i->second, 4 );
        pos_vetor += 4;

        dados_retorno.push_back( i->first );
        pos_vetor++;
    }

    //Limite das informações dos nós da árvore
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    pos_vetor += 4;

    raiz = constuir_arvore( ordem_no );

    std::map< uint8_t, int > id_cor;
    No_arvore *percorrer;
    uint8_t mascara = 0b10000000;
    int posicao;

    //Inicializa os ids
    percorrer_arvore( raiz, id_cor );

    dados_retorno.push_back( 0 );
    
    for ( int i = 0; i < tamanho; i++ ) {
        posicao = id_cor[ dados[ i ] ];
            
        percorrer = raiz;
        while ( posicao != percorrer->id ) {
            if ( posicao > percorrer->id ) {
                percorrer = percorrer->filho_d;
            } else {
                percorrer = percorrer->filho_e;
                dados_retorno[ pos_vetor ] = dados_retorno[ pos_vetor ] | mascara;
            }

            mascara = mascara >> 1;
            if ( mascara == 0 ) {
                mascara = 0b10000000;
                dados_retorno.push_back( 0 );
                pos_vetor++;
            }
        }
    }

    uint8_t *retorno = new uint8_t[ dados_retorno.size() + 4 ];
    memcpy( retorno, &tamanho, 4 );
    memcpy( &retorno[4], dados_retorno.data(), dados_retorno.size() );
    
    deletar_arvore( raiz );

    if ( novo_tamanho != nullptr )
        *novo_tamanho = dados_retorno.size() + 4;

    return retorno;
}

uint8_t* huffman ( Pixel *dados, int tamanho, int *novo_tamanho = nullptr )
{
    std::map< uint8_t, int > qtd_cor;

    //calcula a quantidade de vezes que cada cor aparece
    for ( int i = 0; i < tamanho; i++ ) {
        for ( int cor = 0; cor < 3; cor++ ) {
            try {
                qtd_cor.at( dados[i].cores[cor] )++;
            } catch ( const std::out_of_range& oor ) {
                qtd_cor[ dados[i].cores[cor] ] = 1;
            }
        }
    }

    std::vector< uint8_t > dados_retorno;
    std::vector< No_arvore* > ordem_no;
    No_arvore *raiz;
    int pos_vetor = 0;

    //Inicializa o vetor com um nó pra cada cor
    dados_retorno.reserve( ( qtd_cor.size() * 5 ) + 4 );
    ordem_no.reserve( qtd_cor.size() );
    for ( auto i = qtd_cor.begin(); i != qtd_cor.end(); i++ ) {
        ordem_no.push_back( new No_arvore( i->first, i->second, 0, nullptr, nullptr, nullptr ) );

        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );
        dados_retorno.push_back( 0 );

        memcpy( &dados_retorno.data()[ pos_vetor ], &i->second, 4 );
        pos_vetor += 4;

        dados_retorno.push_back( i->first );
        pos_vetor++;
    }

    //Limite das informações dos nós da árvore
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    dados_retorno.push_back( 0 );
    pos_vetor += 4;

    raiz = constuir_arvore( ordem_no );

    std::map< uint8_t, int > id_cor;
    No_arvore *percorrer;
    uint8_t mascara = 0b10000000;
    int posicao;

    //Inicializa os ids
    percorrer_arvore( raiz, id_cor );

    dados_retorno.push_back( 0 );
    
    for ( int i = 0; i < tamanho; i++ ) {
        for ( int cor = 0; cor < 3; cor++ ) {
            posicao = id_cor[ dados[ i ].cores[ cor ] ];
            
            percorrer = raiz;
            while ( posicao != percorrer->id ) {
                if ( posicao > percorrer->id ) {
                    percorrer = percorrer->filho_d;
                } else {
                    percorrer = percorrer->filho_e;
                    dados_retorno[ pos_vetor ] = dados_retorno[ pos_vetor ] | mascara;
                }

                mascara = mascara >> 1;
                if ( mascara == 0 ) {
                    mascara = 0b10000000;
                    dados_retorno.push_back( 0 );
                    pos_vetor++;
                }
            }
        }
    }

    uint8_t *retorno = new uint8_t[ dados_retorno.size() + 4 ];
    int tamanho_dados = tamanho * 3;
    memcpy( retorno, &tamanho_dados, 4 );
    memcpy( &retorno[4], dados_retorno.data(), dados_retorno.size() );
    
    deletar_arvore( raiz );

    if ( novo_tamanho != nullptr )
        *novo_tamanho = dados_retorno.size() + 4;

    return retorno;
}

uint8_t* huffman_i ( uint8_t *dados, int *novo_tamanho = nullptr )
{
    int tamanho_original;
    memcpy( &tamanho_original, dados, 4 );

    uint8_t *retorno = new uint8_t[ tamanho_original ];
    No_arvore *percorrer;
    uint8_t mascara = 0b10000000;
    uint8_t bit_lido;
    int pos_retorno = 0;
    int pos_dados = 4;

    int repeticoes = 0;
    uint8_t cor;
    std::vector< No_arvore* > ordem_no;
     No_arvore* raiz;

    do {
        memcpy( &repeticoes, &dados[ pos_dados ], 4 );
        pos_dados += 4;
        if ( repeticoes != 0 ) {
            cor = dados[ pos_dados++ ];
            ordem_no.push_back( new No_arvore( cor, repeticoes, 0, nullptr, nullptr, nullptr ) );
        }
    } while ( repeticoes != 0 );

    raiz = constuir_arvore( ordem_no );

    percorrer = raiz;

    while ( pos_retorno < tamanho_original ) {
        bit_lido = 0;
        bit_lido = mascara & dados[ pos_dados ];

        if ( bit_lido == 0 )
            percorrer = percorrer->filho_d;
        else
            percorrer = percorrer->filho_e;
        
        if ( percorrer->filho_d == nullptr && percorrer->filho_e == nullptr ) {
            retorno[ pos_retorno++ ] = percorrer->cor;
            percorrer = raiz;
        }

        mascara = mascara >> 1;

        if ( mascara == 0 ) {
            mascara = 0b10000000;
            pos_dados++;
        }
    }

    deletar_arvore( raiz );

    if ( novo_tamanho != nullptr )
        *novo_tamanho = tamanho_original;

    return retorno;
}

#endif