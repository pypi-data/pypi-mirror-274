from glob import glob
import argparse
import imgproc
import os
import logging

def process_images(compile=False, preprocess=False, image=None):
    """
    Function to compile and preprocess images using C++ and Python.
    """
    # Constants for directories
    pn_SRC = os.path.abspath(os.path.join("..", "data"))

    # Collect images based on provided arguments
    if image:
        images = sorted(glob(os.path.join(pn_SRC, image)))
    else:
        images = sorted(glob(os.path.join(pn_SRC, "*.png")))

    if not images:
        logging.warning("No images found to process.")
        return

    # Compile C++ files if the compile flag is set
    if compile:
        logging.info("Compiling C++ files...")
        imgproc.compile()

    # Preprocess images if the preprocess flag is set
    if preprocess:
        logging.info("Starting preprocessing of images...")
        imgproc.execute(images)






