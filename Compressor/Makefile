main: Compressor

build/met_comp.o: metodos_compressao.cpp metodos_compressao.h
	g++ -g -c $< -o $@ -O3

build/ope_img.o: operacoes_img.cpp operacoes_img.h
	g++ -g -c $< -o $@ -O3

Compressor: Compressor.cpp build/met_comp.o build/ope_img.o
	g++ $^ -o $@ -O3