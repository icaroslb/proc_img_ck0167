#include "Huffman.h"

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

uint8_t* huffman ( Pixel *dados, int tamanho, No_arvore **raiz_retorno, int *novo_tamanho )
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

    std::vector< No_arvore* > ordem_no;
    No_arvore *novo_no;
    No_arvore *no_e;
    No_arvore *no_d;
    int id = 0;

    //Inicializa a heap com um nó pra cada cor
    ordem_no.reserve( qtd_cor.size() );
    for ( auto i = qtd_cor.begin(); i != qtd_cor.end(); i++ ) {
        novo_no = new No_arvore( i->first, i->second, 0, nullptr, nullptr, nullptr );
        ordem_no.push_back( novo_no );
    }

    //Constroi a árvore
    while ( ordem_no.size() > 1 ) {
        std::sort( ordem_no.begin(), ordem_no.end(), []( No_arvore* n_1, No_arvore* n_2 ) { return n_1->repeticao > n_2->repeticao; } );
        
        no_e = ordem_no.back();
        ordem_no.pop_back();
        no_d = ordem_no.back();
        ordem_no.pop_back();

        novo_no = new No_arvore( 0, no_e->repeticao + no_d->repeticao, 0, nullptr, no_e, no_d );
        no_e->pai = novo_no;
        no_d->pai = novo_no;

        ordem_no.push_back( novo_no );
    }

    std::map< uint8_t, int > id_cor;
    std::vector< uint8_t > dados_retorno;
    No_arvore *raiz;
    No_arvore *percorrer;
    uint8_t mascara = 0b10000000;
    int pos_vetor = 0;
    int posicao;

    raiz = ordem_no[0];
    dados_retorno.reserve( tamanho * 3 );
    dados_retorno.push_back( 0 );

    //Inicializa os ids
    percorrer_arvore( raiz, id_cor );

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

    uint8_t *retorno = new uint8_t[ dados_retorno.size() ];
    memcpy( retorno, dados_retorno.data(), dados_retorno.size() );
    
    //deletar_arvore( raiz );

    *raiz_retorno = raiz;

    if ( novo_tamanho != nullptr )
        *novo_tamanho = dados_retorno.size();

    std::cout << tamanho * 3 << " vs " << dados_retorno.size() << std::endl;

    return retorno;
}

uint8_t* huffman_i ( uint8_t *dados, int tamanho, No_arvore *raiz, int tamanho_original )
{
    uint8_t *retorno = new uint8_t[ tamanho_original ];
    No_arvore *percorrer = raiz;
    int pos_cor = 0;
    int pos_dados = 0;
    uint8_t mascara = 0b10000000;
    uint8_t bit_lido;

    while ( pos_cor < tamanho_original ) {
        bit_lido = 0;
        bit_lido = mascara & dados[ pos_dados ];

        if ( bit_lido == 0 )
            percorrer = percorrer->filho_d;
        else
            percorrer = percorrer->filho_e;
        
        if ( percorrer->filho_d == nullptr && percorrer->filho_e == nullptr ) {
            retorno[ pos_cor++ ] = percorrer->cor;
            percorrer = raiz;
        }

        mascara = mascara >> 1;

        if ( mascara == 0 ) {
            mascara = 0b10000000;
            pos_dados++;
        }
    }

    std::cout << __FILE__ << std::endl;

    return retorno;
}