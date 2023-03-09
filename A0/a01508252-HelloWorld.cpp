/*
 * command to compile & run:
 * g++ a01508252-HelloWorld.cpp -o HelloWorld && ./HelloWorld HelloWorld-test1.in
 */

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    // Check if the correct number of arguments is provided
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <filename>\n";
        return 1;
    }
    
    // Get the file name
    string filename = argv[1];
    
    // Print "Hello World!" with a line break
    cout << "Hello World!" << endl;
    
    // Open the file and print its contents without an additional line break
    ifstream file(filename);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            cout << line;
        }
        file.close();
    } else {
        cerr << "Error: Could not open file " << filename << "\n";
        return 1;
    }
    
    return 0;
}