#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION

#include "util.h"

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

Pixel* abrir_bmp ( char *nome_img, int *largura, int *altura, int *canais )
{
    return (Pixel*)stbi_load( nome_img, largura, altura, canais, 0 );
}

void salvar_bmp ( char *nome_img, int largura, int altura, int canais, Pixel *img )
{
    stbi_write_bmp( nome_img, largura, altura, canais, img );
}