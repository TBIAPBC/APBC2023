/*
 * compile & run:
 * g++ julian-zim-HelloWorld.cpp -o julian-zim-HelloWorld && ./julian-zim-HelloWorld HelloWorld-test1.in
 */

#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>

int main(int argc, char* argv[]) {
	if (argc != 2) {
		std::cout << "Usage: " << argv[0] << " <filename>\n";
		return EXIT_FAILURE;
	}
	std::string filename = argv[1];
	std::ifstream file;
	file.open(filename);
	if (!file.is_open()) {
		throw std::runtime_error("File \""
			+ std::filesystem::current_path().string()
			+ "/" + filename
			+ "\" couldn't be found.");
	}
	std::string content = "Hello World!";
	std::string line;
	while (getline(file, line)) {
		content += "\n" + line;
	}
	file.close();
	std::cout << content;
	return EXIT_SUCCESS;
}

