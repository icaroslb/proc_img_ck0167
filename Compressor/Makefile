main: Compressor

met_comp.o: metodos_compressao.cpp metodos_compressao.h
	g++ -g -c $< -o $@ -O3

ope_img.o: operacoes_img.cpp operacoes_img.h
	g++ -g -c $< -o $@ -O3

Huffman.o: Huffman.cpp Huffman.h
	g++ -g -c $< -o $@ -O3

Compressor: Compressor.cpp met_comp.o ope_img.o Huffman.o
	g++ $^ -o $@ -O3

clean:
	del Compressor.exe *.o