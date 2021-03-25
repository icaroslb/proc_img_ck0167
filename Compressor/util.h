#ifndef UTIL_H
#define UTIL_H

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

void transpor_img ( Pixel *img, int largura, int altura )
{
    Pixel *img_aux = new Pixel[ largura * altura ];

    memcpy( img_aux, img, largura * altura * sizeof( Pixel ) );

    for ( int i = 0; i < altura; i++ ) {
        for ( int j = 0; j < largura; j++ ) {
            img[ ( j * altura ) + i ] = img_aux[ j + ( i * largura ) ];
        }
    }

    delete [] img_aux;
}

#endif