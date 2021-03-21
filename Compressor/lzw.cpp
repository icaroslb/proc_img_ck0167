#include <iostream>
#include <array>
#include <string>
#include <vector>
#include <windows.h>
using namespace std;


vector<int> lzwCompressor(string teste){
    //Codificador
    //cout << "Codificador \n";
    vector<string> dict {};
    //Popula o dionário
    for(int val = 0; val <= 255; val++){
        string ascii;
        ascii = ('0' + val);
        dict.push_back(ascii);
        //cout << dict.at(val);
    }



    vector<int> seqcod;
    string I = "";
    I = I + teste.at(0);
    char c;

    dict.resize(256);
    seqcod.resize(0);
    //cout << "dict.size() é: " << dict.size() << "\n";
    int i = 1;
    int track;
    while (i <= teste.length())
    {
        if(i < teste.length()){
            c = teste.at(i);
        }
        //cout << "c: " << c << "\n";
        bool exist = false;
        //cout << "round " << i << " I: " << I << "\n";
        //cout << "I: " << I << "\n";
        //Procura a string no dicionário
        int j;
        for(j = 0; j<=dict.size()-1 && exist == false; j++){
            if(I.compare(dict.at(j)) == 0){
                //cout << "opa, este existe \n";
                //cout << I << "vs" << dict.at(j) << "\n";
                track = j;
                I = I + c;
                i++;
                exist = true;
            }
        }   
        if(!exist){
            //i. coloque a palavra código correspondente a I na sequência codificada;
            seqcod.push_back(track);
            //cout << "o tamanho de seqcod é " << seqcod.size() << "(" << dict.at(track) << " foi inserido)\n";
		    //ii. adicione a string I+c ao dicionário;
            dict.push_back(I);
            //cout << I <<" foi inserido no dicionário: " << dict.at(dict.size()-1) << "\n";
            //cout << "Inserido \n";
		    //iii. I <= c;
            I = teste.at(i-1);
        }
    }
    seqcod.push_back(track);
    //cout << "o tamanho de seqcod é " << seqcod.size() << "\n \n";
    return seqcod;
}
string lzwDescompressor(vector<int>seqcod){
    //cout << "Decodificador \n";
    vector<string> dict {};
    //Popula o dionário
    for(int val = 0; val <= 255; val++){
        string ascii;
        ascii = ('0' + val);
        dict.push_back(ascii);
        //cout << dict1.at(val);
    }
    int cw = seqcod.at(0);
    string str = "";
    str = str + (char)('0' + cw);
    string P;
    string C;
    
    for(int i = 1; i <= seqcod.size()-1; i++){
        int pw = cw;
        cw = seqcod.at(i);
        string cstr = "";
        P = "";
        cstr = cstr + (char)('0' + cw);
        //Checa se cw é um índice no dicionário
        if(cw <= dict.size()-1){
            //i. coloque a string(cW) na sequência de saída;
                //cout << "str insere " << dict.at(cw) << "\n";
                str = str + dict.at(cw);
                //cout << "string de saída atual: " << str << "\n";
		        //ii. P <= string(pW);
                P = P + (char)('0' + pw);
		        //iii. C <= primeiro caracter da string(cW);
		        //iv. adicione a string P+C ao dicionário;
                dict.push_back(P+cstr[0]);
                //cout << "Inserido no dicionário: " << dict1.at(dict1.size()-1) << "\n";
        }
        else{
            P = P + (char)('0' + pw);
            str = str + (P + cstr[0]);
            //cout << "Inserido no dicionário: " << dict.at(dict.size()-1) << "\n";
        }
        //cout << "cw " << cw << " string " << cstr << "\n";
    }
    //cout << "\n Descompactei: " << str << "\n";
    return str;
}