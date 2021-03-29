#ifndef METODOS_COMPRESSAO_H
#define METODOS_COMPRESSAO_H

#include "util.h"

void wavelets ( uint8_t *dados, int tamanho )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       int metade = tamanho / 2;
       uint8_t soma;
       uint8_t divisao;

       memcpy( dados_aux, dados, tamanho );

       for ( int i = 0; i < metade; i++ ) {
              soma = dados_aux[ 2 * i ] + dados_aux[ (2 * i ) + 1 ];
              divisao = soma >> 1;
              
              //divide a soma por 2 e joga o último bit para o mais significativo para saber se a soma foi impar
              dados[ i ] = divisao | ( soma << 7 );
              dados[ metade + i ] = dados_aux[ 2 * i ] - divisao;
       }

       delete [] dados_aux;
}

void wavelets_i ( uint8_t *dados, int tamanho )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       int metade = tamanho / 2;
       uint8_t valor_media;

       memcpy( dados_aux, dados, tamanho );

       for ( int i = 0; i < metade; i++ ) {
              valor_media = dados_aux[ i ] & 0b01111111;
              dados[ 2 * i ] = valor_media + dados_aux[ metade + i ];
              dados[ ( 2 * i ) + 1 ] = ( valor_media - dados_aux[ metade + i ] ) + ( dados_aux[ i ] >> 7 );
       }

       delete [] dados_aux;
}

void wavelets ( uint8_t *dados, int tamanho, int nivel )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       uint8_t soma;
       uint8_t divisao;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                     soma = dados_aux[ j ] + dados_aux[ j + 1 ];
                     divisao = soma >> 1;
              
                     dados[ j ] = divisao | ( soma << 7 );
                     dados[ j + 1 ] = dados_aux[ j ] - divisao;
              }

       }

       delete [] dados_aux;
}

void wavelets_i ( uint8_t *dados, int tamanho, int nivel )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       uint8_t valor_media;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade = tamanho / 2;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                     valor_media = dados_aux[ j ] & 0b01111111;
                     dados[ j ] = valor_media + dados_aux[ j + 1 ];
                     dados[ j + 1 ] = ( valor_media - dados_aux[ j + 1 ] ) + ( dados_aux[ j ] >> 7 );
              }
       
       }

       delete [] dados_aux;
}

void wavelets ( Pixel *dados, int tamanho, int nivel )
{
       Pixel *dados_aux = new Pixel[ tamanho ];
       uint8_t soma;
       uint8_t divisao;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(Pixel) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {

                     for ( int cor = 0; cor < 3; cor++ ) {
                            soma = dados_aux[ j ].cores[ cor ] + dados_aux[ j + 1 ].cores[ cor ];
                            divisao = soma >> 1;
              
                            dados[ j ].cores[ cor ] = soma;
                            dados[ j + 1 ].cores[ cor ] = dados_aux[ j ].cores[ cor ] - divisao;
                     }

              }

       }

       delete [] dados_aux;
}

void wavelets_i ( Pixel *dados, int tamanho, int nivel )
{
       Pixel *dados_aux = new Pixel[ tamanho ];
       uint8_t valor_media;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade = tamanho / 2;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(Pixel) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                     
                     for ( int cor = 0; cor < 3; cor++ ) {
                            valor_media = dados_aux[ j ].cores[cor] >> 1;
                            dados[ j ].cores[cor] = valor_media + dados_aux[ j + 1 ].cores[cor];
                            dados[ j + 1 ].cores[cor] = ( valor_media - dados_aux[ j + 1 ].cores[cor] ) + ( dados_aux[ j ].cores[cor] & 0b00000001 );
                     }

              }
       
       }

       delete [] dados_aux;
}

void wavelets_shift_rotativo ( Pixel *dados, int tamanho, int nivel )
{
       Pixel *dados_aux = new Pixel[ tamanho ];
       uint8_t soma;
       uint8_t divisao;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(Pixel) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {

                     for ( int cor = 0; cor < 3; cor++ ) {
                            soma = dados_aux[ j ].cores[ cor ] + dados_aux[ j + 1 ].cores[ cor ];
                            divisao = soma >> 1;
              
                            dados[ j ].cores[ cor ] = divisao | ( soma << 7 );
                            dados[ j + 1 ].cores[ cor ] = dados_aux[ j ].cores[ cor ] - divisao;
                     }

              }

       }

       delete [] dados_aux;
}

void wavelets_i_shift_rotativo ( Pixel *dados, int tamanho, int nivel )
{
       Pixel *dados_aux = new Pixel[ tamanho ];
       uint8_t valor_media;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade = tamanho / 2;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(Pixel) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                     
                     for ( int cor = 0; cor < 3; cor++ ) {
                            valor_media = dados_aux[ j ].cores[cor] & 0b01111111;
                            dados[ j ].cores[cor] = valor_media + dados_aux[ j + 1 ].cores[cor];
                            dados[ j + 1 ].cores[cor] = ( valor_media - dados_aux[ j + 1 ].cores[cor] ) + ( dados_aux[ j ].cores[cor] >> 7 );
                     }

              }
       
       }

       delete [] dados_aux;
}

void wavelets_shift_rotativo ( uint8_t *dados, int tamanho, int nivel )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       uint8_t soma;
       uint8_t divisao;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(uint8_t) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                     soma = dados_aux[ j ] + dados_aux[ j + 1 ];
                     divisao = soma >> 1;
              
                     dados[ j ] = divisao | ( soma << 7 );
                     dados[ j + 1 ] = dados_aux[ j ] - divisao;

              }

       }

       delete [] dados_aux;
}

void wavelets_i_shift_rotativo ( uint8_t *dados, int tamanho, int nivel )
{
       uint8_t *dados_aux = new uint8_t[ tamanho ];
       uint8_t valor_media;

       int qtd_divisoes = pow( 2, nivel );
       int tam_divisoes = tamanho / qtd_divisoes;
       int metade = tamanho / 2;
       int metade_div = tam_divisoes / 2;
       int inicio;
       int fim;

       memcpy( dados_aux, dados, tamanho * sizeof(uint8_t) );

       for ( int i = 0; i < qtd_divisoes; i++ ) {
              inicio = tam_divisoes * i;
              fim = inicio + tam_divisoes - 1;

              for ( int j = inicio; j < fim; j += 2 ) {
                            valor_media = dados_aux[ j ] & 0b01111111;
                            dados[ j ] = valor_media + dados_aux[ j + 1 ];
                            dados[ j + 1 ] = ( valor_media - dados_aux[ j + 1 ] ) + ( dados_aux[ j ] >> 7 );
              }
       
       }

       delete [] dados_aux;
}

#endif