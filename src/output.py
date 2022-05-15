import os

from constant import OUTPUT_DIR


def prepare_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
