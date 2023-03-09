/*
 * How to produce the desired outputs:
 * g++ julian-zim-WordCount.cpp -o julian-zim-WordCount && ./julian-zim-WordCount WordCount-test1.in
 * g++ julian-zim-WordCount.cpp -o julian-zim-WordCount && ./julian-zim-WordCount WordCount-test2.in -l
 * g++ julian-zim-WordCount.cpp -o julian-zim-WordCount && ./julian-zim-WordCount WordCount-test3.in -l -I
 */

#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <filesystem>

bool compare(std::pair<std::string, unsigned>& a, std::pair<std::string, unsigned>& b) {
	if (a.second == b.second) {
		return a.first < b.first;
	}
	return a.second > b.second;
}

/* 
 * runtime complexity with n as the number of words in the text:
 * map creation is n log n
 * map value summing is n, map to vector copying is n, vector outputting is n
 * vector sorting is n log n
 * => this makes n log n in total
*/
int main(int argc, char* argv[]) {

	bool ignore_case = false;
	bool list = false;
	std::string filename = "";

	// PARSE
	if (argc < 2 || argc > 4) {
		std::cout << "Usage: " << argv[0] << " <filename> [-I] [-l]\n";
		return EXIT_FAILURE;
	}
	for (unsigned i = 1; i < argc; i++) {
		std::string argument = argv[i];
		if (argument[0] == '-') {
			if (argument == "-I") {
				ignore_case = true;
			}
			else if (argument == "-l") {
				list = true;
			}
			else {
				throw std::runtime_error("Unknown argument: \"" + argument + "\"!");
			}
		}
		else if (filename.length() == 0) {
			filename = argv[i];
		}
		else {
			throw std::runtime_error("Unexpected parameter: \"" + argument + "\"! Note that a filename has already been passed (\"" + filename + "\")");
		}
	}

	// FILE
	std::ifstream file;
	if (filename.length() != 0) {
		file.open(filename);
	}
	else {
		throw std::runtime_error("Please pass a filename!");
	}
	if (!file.is_open()) {
		throw std::runtime_error("File \"" + std::filesystem::current_path().string() + "/" + filename + "\" couldn't be found.");
	}

	// MAP
	std::map<std::string, unsigned> words;
	std::string line;
	while (getline(file, line)) {
		line += "\n";

		std::string word = "";
		for (unsigned i = 0; i < line.length(); i++) {
			char character = line[i];

			// lower case letter
			if (character >= 97 && character <= 122) {
				word += character;
			}
			// upper case letter
			else if (character >= 65 && character <= 90) {
				if (ignore_case) {
					character += 32;
				}
				word += character;
			}
			// two sized utf8 char letter (ß, ä, ü, ö, Ä, Ü, Ö)
			else if (character == -61) {
				i += 1;
				char character2 = line[i];

				if (character2 == -68 || character2 == -74 || character2 == -92 || character2 == -97) {
					word += character;
					word += character2;
				}
				else if (character2 == -100 || character2 == -106 || character2 == -124) {
					if (ignore_case) {
						character2 += 32;
					}
					word += character;
					word += character2;
				}
			}
			// no letter
			else {
				if (word.length() > 0) {
					try {
						unsigned& count = words.at(word);
						count += 1;
					}
					catch (std::out_of_range e) {
						words.emplace(word, 1);
					}
					word = "";
				}
			}
		}

	}
	file.close();

	// OUTPUT
	if (list) {
		std::vector<std::pair<std::string, unsigned>> words_sorted;
		for (std::pair<std::string, unsigned> entry : words) {
			words_sorted.push_back(entry);
		}
		std::sort(words_sorted.begin(), words_sorted.end(), compare);
		for (std::pair<std::string, unsigned> entry: words_sorted) {
			std::cout << entry.first << "\t" << entry.second << std::endl;
		}
	}
	else {
		unsigned sum = 0;
		for (std::pair<std::string, unsigned> entry : words) {
			sum += entry.second;
		}
		std::cout << words.size() << " / " << sum << std::endl;
	}

	return EXIT_SUCCESS;
}
