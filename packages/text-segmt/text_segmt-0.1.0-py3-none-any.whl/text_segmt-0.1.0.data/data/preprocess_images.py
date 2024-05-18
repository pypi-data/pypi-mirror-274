from glob import glob
import os
import logging
import imgproc

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def preprocess_images(image_directory, compile_cpp=False, preprocess=False, specific_image=None):
    """
    Preprocesses images in the specified directory using C++ and Python.

    Args:
        image_directory (str): Path to the directory containing images.
        compile_cpp (bool): Whether to compile C++ files before preprocessing.
        preprocess (bool): Whether to preprocess images.
        specific_image (str): Name of a specific image file to preprocess.
    """
    # Collect images based on provided arguments
    if specific_image:
        images = [os.path.join(image_directory, specific_image)]
    else:
        images = glob(os.path.join(image_directory, "*.png"))

    if not images:
        logging.warning("No images found to process.")
        return

    # Compile C++ files if specified
    if compile_cpp:
        logging.info("Compiling C++ files...")
        imgproc.compile()

    # Preprocess images if specified
    if preprocess:
        logging.info("Starting preprocessing of images...")
        imgproc.execute(images)

# Example usage:
if __name__ == '__main__':
    
