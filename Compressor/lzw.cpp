#include <iostream>
#include <array>
#include <string>
#include <vector>
using namespace std;


int main(){
    vector<string> dict {};
    //Popula o 
    for(int val = 0; val <= 255; val++){
        string ascii;
        ascii = ('0' + val);
        dict.push_back(ascii);
        cout << dict.at(val);
    }

    string I = "";

    char c;

    string seqcod;
    string teste= "A_ASA_DA_CASA";

    dict.resize(256);
    for(int i = 0; i <= teste.length()-1; i++){
    
        c = teste.at(i);
        bool exist = false;
        cout << "round " << i << " I: " << I << "\n";
        string sum = I + c;
        //Procura a string no dicionário
        int j;
        for(j = 0; j<=dict.size()-1 && !exist; j++){
            if(sum.compare(dict.at(j)) == 0){
                cout << "opa, este existe \n";
                cout << sum << "vs" << dict.at(j) << "\n";
                I = sum;
                exist = true;
            }
            else{
                //cout << sum << "vs" << dict.at(j) << "\n";
            }
        }   
        if(!exist){
            //i. coloque a palavra código correspondente a I na sequência codificada;
            seqcod = seqcod + I;
            //cout << "code = " <<(char)('0' + j) << "\n";
            cout << "seqcod = " << seqcod << "\n";
		    //ii. adicione a string I+c ao dicionário;
            dict.push_back(sum);
            cout << "Inserido: " << dict.at(dict.size()-1) << "\n";
            //cout << "Inserido \n";
		    //iii. I <= c;
            I = c;
        }
        cout << j;
    }

    return 0;
}