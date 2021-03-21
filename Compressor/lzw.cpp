#include <iostream>
#include <array>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <windows.h>
using namespace std;

string lzwDescompressor(vector<int> entrada) 
{ 
    string decom = "";
    unordered_map<int, string> dict; 
    for (int i = 0; i <= 255; i++) { 
        string ascii = ""; 
        ascii += char(i); 
        dict[i] = ascii; 
    } 
    int pw = entrada[0], n; 
    string s = dict[pw]; 
    string c = "";
    c += s[0]; 
    decom += c;
    int count = 256; 
    for (int i = 0; i < entrada.size() - 1; i++) { 
        n = entrada[i + 1]; 
        if (dict.find(n) == dict.end()) { 
            s = dict[pw]; 
            s = s + c; 
        } 
        else { 
            s = dict[n]; 
        } 
        //cout << s;
        decom += s; 
        c = ""; 
        c += s[0]; 
        dict[count] = dict[pw] + c; 
        count++; 
        pw = n; 
    }
    return decom; 
}

vector<int> lzwCompressor(string entrada) 
{ 
    unordered_map<string, int> dict; 
    for (int i = 0; i <= 255; i++) { 
        string ascii = ""; 
        ascii += char(i); 
        dict[ascii] = i; 
    } 
  
    string I = "", c = ""; 
    I += entrada[0]; 
    int code = 256; 
    vector<int> seqcod; 
    for (int i = 0; i < entrada.length(); i++) { 
        if (i != entrada.length() - 1) 
            c += entrada[i + 1]; 
        if (dict.find(I + c) != dict.end()) { 
            I = I + c; 
        } 
        else {  
            seqcod.push_back(dict[I]); 
            dict[I + c] = code; 
            code++; 
            I = c; 
        } 
        c = ""; 
    } 
    //cout << I << "\t" << dict[I] << endl; 
    seqcod.push_back(dict[I]); 
    return seqcod; 
} 

int main(){
    string teste = "A_ASA_DA_CASAAAAAAA_AAAAAs";
    cout << lzwDescompressor(lzwCompressor(teste));
    ///cout << "Espaço economizado: " << teste.length() - lzwCompressor(teste).size() << "\n";
}