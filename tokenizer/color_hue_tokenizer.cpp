#include <iostream>
#include <fstream>
#include <bitset>
#include <string>

// Convert hue to frequency (simplified visible light range 400-700 THz)
double calculateFrequency(int hue) {
    return 400.0 + (hue / 360.0) * 300.0;
}

// Build a binary token from hue, RGB, and frequency
std::string generateColorToken(int hue, int r, int g, int b, double freq) {
    return std::bitset<16>(hue).to_string() + "," +
           std::bitset<8>(r).to_string() + "," +
           std::bitset<8>(g).to_string() + "," +
           std::bitset<8>(b).to_string() + "," +
           std::to_string(freq);
}

int main() {
    std::ofstream file("full_color_tokens.csv");
    file << "Token,Hue,Red,Green,Blue,Frequency\n";  // CSV Header

    for (int hue = 0; hue < 360; hue += 10) {
        for (int r = 0; r <= 255; r += 64) {
            for (int g = 0; g <= 255; g += 64) {
                for (int b = 0; b <= 255; b += 64) {
                    double freq = calculateFrequency(hue);
                    std::string token = generateColorToken(hue, r, g, b, freq);
                    file << token << "," << hue << "," << r << "," << g << "," << b << "," << freq << "\n";
                }
            }
        }
    }

    file.close();
    std::cout << "Systematic color tokens saved to full_color_tokens.csv\n";
    return 0;
}
