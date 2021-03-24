#ifndef METODOS_COMPRESSAO_H
#define METODOS_COMPRESSAO_H

#include "util.h"

void wavelets ( uint8_t *dados, int tamanho );
void wavelets_i ( uint8_t *dados, int tamanho );
void wavelets ( uint8_t *dados, int tamanho, int nivel );
void wavelets_i ( uint8_t *dados, int tamanho, int nivel );
void wavelets ( Pixel *dados, int tamanho, int nivel );
void wavelets_i ( Pixel *dados, int tamanho, int nivel );
void wavelets_shift_rotativo ( Pixel *dados, int tamanho, int nivel );
void wavelets_i_shift_rotativo ( Pixel *dados, int tamanho, int nivel );

#endif