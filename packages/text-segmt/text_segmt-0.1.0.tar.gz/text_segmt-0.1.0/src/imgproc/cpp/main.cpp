#include "Binarization.hpp"
#include "Scanner.hpp"
#include "LineSegmentation.hpp"
#include <filesystem>
#include <string>
#include <opencv2/opencv.hpp>

namespace fs = std::filesystem;

int main(int argc, char *argv[]) {

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_image_path>\n";
        return 1;
    }

    std::string srcPath = argv[1];
    fs::path inputDir = fs::path(srcPath).parent_path(); // Get the input image's directory

    cv::Mat image = cv::imread(srcPath);

    if (image.empty()) {
        std::cerr << "Error: Could not open or read the image file\n";
        return 1;
    }

    fs::path outPath = inputDir / "output"; // Define the output directory as a subdirectory named 'output'

    // Create the output directory if it doesn't exist
    fs::create_directories(outPath);

    // START Step 1: crop //
    Scanner scanner;
    cv::Mat imageCropped;
    scanner.process(image, imageCropped);

    // START Step 1.1: resize and definitions //
    int newW = 1280;
    int newH = ((newW * imageCropped.rows) / imageCropped.cols);
    cv::resize(imageCropped, imageCropped, cv::Size(newW, newH));

    int chunksNumber = 8;
    int chunksProcess = 4;
    // END Step 1.1 //

    // START Step 2: binarization //
    Binarization threshold;
    cv::Mat imageBinary;
    // default = 0 | otsu = 1 | niblack = 2 | sauvola = 3 | wolf = 4 //
    threshold.binarize(imageCropped, imageBinary, true, 3);

    // START Step 3: line segmentation //
    LineSegmentation line;
    std::vector<cv::Mat> lines;
    cv::Mat imageLines = imageBinary.clone();
    line.segment(imageLines, lines, chunksNumber, chunksProcess);
    
    // Save segmented lines in the output directory
    for (size_t i = 0; i < lines.size(); ++i) {
        std::string lineName = std::to_string(i) + ".png";
        fs::path saveLine = outPath / lineName;
        cv::imwrite(saveLine.u8string(), lines[i]);
    }

    return 0;
}

