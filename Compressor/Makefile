main: Compressor

met_comp.o: metodos_compressao.cpp metodos_compressao.h
	g++ -g -c $< -o $@ -O3

util.o: util.cpp util.h
	g++ -g -c $< -o $@ -O3

Huffman.o: Huffman.cpp Huffman.h
	g++ -g -c $< -o $@ -O3

Cod_preditiva.o: Cod_preditiva.cpp Cod_preditiva.h
	g++ -g -c $< -o $@ -O3

Compressor: Compressor.cpp met_comp.o util.o Huffman.o Cod_preditiva.o
	g++ $^ -o $@ -O3

clean:
	del Compressor.exe *.o