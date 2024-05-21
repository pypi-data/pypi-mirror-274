# linesegmt

## Description
`linesegmt` is a Python package for line segmentation in images.

## Installation
You can install `linesegmt` using pip:

```bash```
pip install linesegmt

## Using process_image function:
from linesegmt.run import process_image

# Example usage
input_image_path = "input_image.jpg"
output_directory = "output/"
process_image(input_image_path, output_directory)

# Running from command line:
python -m linesegmt.run input_image.jpg output_directory

Replace input_image.jpg with the path to your input image and output_directory with the directory where you want the segmented images to be saved.

# License

This project is licensed under the MIT License - see the LICENSE file for details.


