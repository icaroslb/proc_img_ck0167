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

No_arvore* proximo_no ( No_arvore *no );
No_arvore* constuir_arvore ( std::vector< No_arvore* > &vetor );
void percorrer_arvore ( No_arvore *raiz, std::map< uint8_t, int > &id_cor );
void deletar_arvore ( No_arvore *raiz );
uint8_t* huffman ( uint8_t *dados, int tamanho, int *novo_tamanho = nullptr );
uint8_t* huffman ( Pixel *dados, int tamanho, int *novo_tamanho = nullptr );
uint8_t* huffman_i ( uint8_t *dados );

#endif