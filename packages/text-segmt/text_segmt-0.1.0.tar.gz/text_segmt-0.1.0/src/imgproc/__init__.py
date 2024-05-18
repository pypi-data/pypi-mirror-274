from glob import glob
import multiprocessing
import functools
import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

pn_CPP_FILES = os.path.join("imgproc", "cpp")
fn_CPP_OUT = os.path.join(".", "imgproc.out")

class Image():
    def __init__(self, src):
        self.src = src
        self.out_dir = os.path.join(os.path.dirname(src), "output")  # Output directory is a subdirectory 'output'

        # Ensure the output directory exists
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

def compile():
    """
    Compiles the C++ source files into an executable.
    """
    cpp_files = sorted(glob(os.path.join(pn_CPP_FILES, "*.cpp")))
    cpp = " ".join(cpp_files)
    cmd = f"g++ {cpp} -o {fn_CPP_OUT}"

    if sys.platform == "linux":
        cmd += " -std=c++17 -lstdc++fs `pkg-config --cflags --libs opencv`"

    result = os.system(cmd)
    if result != 0:
        logging.warning("Error with `opencv` tag. Compiling with `opencv4`...")
        result = os.system(cmd.replace("opencv", "opencv4"))
        if result != 0:
            logging.error("Preprocess compilation error.")
        else:
            logging.info("Preprocess compiled successfully.")

def execute(images):
    """
    Executes the compiled C++ program on a list of images using multiprocessing.
    """
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.map(__execute__, images)

def __execute__(image):
    """
    Helper function to execute the compiled C++ program on a single image.
    """
    im = Image(image)
    cmd = f"{fn_CPP_OUT} {im.src} {im.out_dir}"  # Pass the output directory as an argument

    result = os.system(cmd)
    if result != 0:
        logging.error(f"Image process error: {im.src}")
        sys.exit(f"Image process error: {im.src}")



