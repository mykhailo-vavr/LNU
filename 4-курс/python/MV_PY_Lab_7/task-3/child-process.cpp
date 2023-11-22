#include <iostream>
#include <fstream>

int main() {
    std::ofstream outFile("file.txt", std::ios::app);
    if (!outFile.is_open()) {
        std::cerr << "== Child process == Error opening file.txt for reading and writing!" << std::endl;
        return 1;
    }

    std::cout << "== Child process == Updating file content" << std::endl;
    outFile << "\nЦей рядок додано в дочірньому процесі";

    outFile.close();

    std::cout << "== Child process == Child process finish" << std::endl;

    return 0;
}
