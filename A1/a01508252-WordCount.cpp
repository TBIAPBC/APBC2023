/*
 * commands to compile & run:
 * g++ -std=c++11 a01508252-WordCount.cpp -o a01508252-WordCount && ./a01508252-WordCount WordCount-test1.in
 * g++ -std=c++11 a01508252-WordCount.cpp -o a01508252-WordCount && ./a01508252-WordCount WordCount-test2.in -l
 * g++ -std=c++11 a01508252-WordCount.cpp -o a01508252-WordCount && ./a01508252-WordCount WordCount-test3.in -l -I
 */

#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <algorithm>
#include <vector>

using namespace std;

bool compare(const pair<string, int>& a, const pair<string, int>& b) {
    if (a.second == b.second) {
        return a.first < b.first;
    }
    return a.second > b.second;
}

int main(int argc, char* argv[]) {
    // Check if filename is provided and if not give error message
    if (argc < 2) {
        cerr << "Error: filename not provided." << endl;
        return 1;
    }

    // Check for option flags
    bool ignoreCase = false;
    bool printList = false;
    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "-I") == 0) {
            ignoreCase = true;
        }
        if (strcmp(argv[i], "-l") == 0) {
            printList = true;
        }
    }

    // Open input file and if not give error message
    ifstream inFile(argv[1]);
    if (!inFile) {
        cerr << "Error: could not open file with name " << argv[1] << "." << endl;
        return 1;
    }

    // Read file and create a map
    map<string, int> word_count;
    string word;
    while (inFile >> word) {
        // separate words based on punctuations and special symbols
        string cleaned_word;
        for (char& c : word) {
            if (isalpha(c) || (c & 0x80) != 0) {  // Keep alphabetical and UTF-8 characters
                if (ignoreCase == true) {
                    cleaned_word += tolower(c);
                } else {
                    cleaned_word += c;
                }
            } else {
                if (!cleaned_word.empty()) {
                    ++word_count[cleaned_word];
                    cleaned_word.clear();
                }
            }
        }
        if (!cleaned_word.empty()) {
            ++word_count[cleaned_word];
        }
    }
    inFile.close();

    // Get the inputfile name and find the position of the last dot in the input file name
    string inputFile = argv[1];
    size_t dotPos = inputFile.rfind('.');
    if (dotPos != string::npos) {
        // Remove everything after the last dot
        inputFile.erase(dotPos);
    }

    // Print the word count to console and output file
    string outFilename = "a01508252-" + inputFile + ".out";
    ofstream outFile(outFilename);

    if (printList == false) {
        int totalValues = 0;
        for (const auto& pair : word_count) {
            totalValues += pair.second;
        }
        cout << word_count.size() << " / " << totalValues << endl;
        outFile << word_count.size() << " / " << totalValues << endl;
    } else {
        // print word count
        vector<pair<string, int>> sorted_word_count(word_count.begin(), word_count.end());
        sort(sorted_word_count.begin(), sorted_word_count.end(), compare);

        for (const auto& pair : sorted_word_count) {
            cout << pair.first << "\t" << pair.second << endl;
            outFile << pair.first << "\t" << pair.second << endl;
        }
    }
    outFile.close();

    return 0;
}

