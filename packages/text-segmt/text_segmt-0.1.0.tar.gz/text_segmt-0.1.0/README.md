# Text Segmentation Package

This package provides tools for text segmentation on images.

## Installation

You can install the package using pip:

```bash```
pip install text-seg
Usage

The main script main.py performs text segmentation on images.
Usage
python main.py -c -p --image <image_path>
Arguments

    -c, --config: Optional. Path to configuration file.
    -p, --preprocess: Optional. Perform preprocessing.
    --image: Required. Path to the input image.

Example

bash

python main.py -c -p --image /home/beijuka/Textsegm/20240418_101538.png

This command will perform text segmentation on the specified image with preprocessing and using the provided configuration file.
Dependencies

    opencv-python >= 4.0
    tensorflow == 2.14.0

License

This package is licensed under the MIT License.
