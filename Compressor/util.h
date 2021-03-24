#ifndef UTIL_H
#define UTIL_H

#include <iostream>
#include <fstream>
#include <cstdint>
#include <cstring>
#include <cmath>

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

void transpor_img ( Pixel *img, int largura, int altura );

Pixel* abrir_bmp ( char *nome_img, int *largura, int *altura, int *canais );
void salvar_bmp ( char *nome_img, int largura, int altura, int canais, Pixel *img );

#endif