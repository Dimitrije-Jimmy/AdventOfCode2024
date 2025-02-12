#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cctype>

using namespace std;

int calculate_mul_sum(const string& input_string) {
    int total_sum = 0;
    bool is_enabled = true;
    size_t i = 0;
    size_t length = input_string.length();

    while (i < length) {
        // Check for 'do()'
        if (input_string.compare(i, 4, "do()") == 0) {
            is_enabled = true;
            cout << "do() encountered: mul instructions enabled" << endl;
            i += 4;
        }
        // Check for "don't()"
        else if (input_string.compare(i, 7, "don't()") == 0) {
            is_enabled = false;
            cout << "don't() encountered: mul instructions disabled" << endl;
            i += 7;
        }
        // Check for 'mul('
        else if (input_string.compare(i, 4, "mul(") == 0) {
            i += 4; // Move past 'mul('
            // Extract first number
            string num1;
            while (i < length && isdigit(input_string[i])) {
                num1 += input_string[i];
                i++;
            }
            // Check for ','
            if (i < length && input_string[i] == ',') {
                i++; // Move past ','
            } else {
                continue; // Invalid format, skip
            }
            // Extract second number
            string num2;
            while (i < length && isdigit(input_string[i])) {
                num2 += input_string[i];
                i++;
            }
            // Check for ')'
            if (i < length && input_string[i] == ')') {
                i++; // Move past ')'
            } else {
                continue; // Invalid format, skip
            }
            // Process the mul instruction
            if (!num1.empty() && !num2.empty()) {
                int x = stoi(num1);
                int y = stoi(num2);
                int product = x * y;
                if (is_enabled) {
                    total_sum += product;
                    cout << "mul(" << x << "," << y << ") = " << product << " (Enabled)" << endl;
                } else {
                    cout << "mul(" << x << "," << y << ") = " << product << " (Disabled)" << endl;
                }
            }
        } else {
            i++; // Move to the next character
        }
    }

    cout << "\nTotal Sum: " << total_sum << endl;
    return total_sum;
}

/*int main() {
    string input_string = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))";
    calculate_mul_sum(input_string);
    return 0;
}*/

int main() {
    // Read the input string from 'input.txt'
    string input_string;
    ifstream input_file("input.txt");
    if (input_file) {
        // Read entire file contents into a string
        stringstream buffer;
        buffer << input_file.rdbuf();
        input_string = buffer.str();
        input_file.close();
    } else {
        cerr << "Error: Unable to open input.txt" << endl;
        return 1;
    }

    calculate_mul_sum(input_string);
    return 0;
}
