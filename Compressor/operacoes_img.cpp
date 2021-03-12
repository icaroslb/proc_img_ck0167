#include "operacoes_img.h"

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