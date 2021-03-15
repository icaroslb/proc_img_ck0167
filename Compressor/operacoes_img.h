#ifndef OPERACOES_IMG
#define OPERACOES_IMG

#include <iostream>
#include <fstream>
#include <cstdint>
#include <cstring>
#include <cmath>

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

#endif