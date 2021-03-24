#ifndef COD_PRED_H
#define COD_PRED_H

#include "util.h"

void codificacao_preditiva ( Pixel *dados, int largura, int altura );
void codificacao_preditiva_i ( Pixel *dados, int largura, int altura );
void codificacao_preditiva ( uint8_t *dados, int tamanho );
void codificacao_preditiva_i ( uint8_t *dados, int tamanho );

#endif