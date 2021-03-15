#include <iostream>
#include <array>
#include <vector>
using namespace std;

template <class T>
void print(std::vector <T> const &a) {
   std::cout << "The vector elements are : ";

   for(int i=0; i < a.size(); i++)
   std::cout << a.at(i) << ' ';
}

template <class T>
T* merge(T* a, T* b){
    T* c = new T[sizeof(a)+sizeof(b)];
    for(int i = 0; i<= sizeof(a)-1; i++){
        c[i] = a[i];
    }
    for(int i = 0; i<= sizeof(b)-1; i++){
        c[sizeof(a)+i] = b[i];
    }
    return c;
}

int main(){
    vector<unsigned char*> dict;
    dict.resize(256);
    for(int val = 0; val <= 255; val++){
        unsigned char* ascii = new unsigned char[1];
        ascii[0] = (unsigned char)('0' + val);
        dict[val] = ascii;
        //cout << *dict[val];
    }
    unsigned char init[] = "";
    unsigned char* I = init;

    unsigned char* c = new unsigned char[1];

    vector<unsigned char> seqcod;
    unsigned char teste[] = "A_ASA_DA_CASA";

    for(int i = 0; i<=sizeof(teste)-1; i++){
        *c = teste[i];
        for(int j = 0; j<=dict.size()-1; j++){
            unsigned char* sum = merge<unsigned char>(I, c);
            //cout << *sum << "vs" << *dict[j] << "\n";
            if(*sum == *dict[j]){
                //cout << "opa deu igual";
                *I = *sum;
            }
            else{
                //i. coloque a palavra código correspondente a I na sequência codificada;
                seqcod.insert( seqcod.end(), *I);
		        //ii. adicione a string I+c ao dicionário;
                dict.insert(dict.end(), sum);
		        //iii. I <= c;
                *I = *c;
                
            }
        }
    }
    print(seqcod);

    return 0;
}