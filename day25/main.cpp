#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm> // for std::remove_if

// Helper to trim whitespace from both ends of a string
static inline void trim(std::string &s) {
    // remove leading spaces
    while (!s.empty() && std::isspace((unsigned char)s.front())) {
        s.erase(s.begin());
    }
    // remove trailing spaces
    while (!s.empty() && std::isspace((unsigned char)s.back())) {
        s.pop_back();
    }
}

std::vector<std::string> read_input(const std::string& file_path) {
    std::ifstream in(file_path);
    if (!in) {
        throw std::runtime_error("Could not open file: " + file_path);
    }

    std::vector<std::string> lines;
    std::string line;

    while (std::getline(in, line)) {
        // Trim line
        trim(line);

        // If the line is not empty, add it
        if (!line.empty()) {
            lines.push_back(line);
        }
    }

    return lines;
}
