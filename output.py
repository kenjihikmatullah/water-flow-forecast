import os
import shutil
from typing import TextIO

from constant import OUTPUT_DIRECTORY, OUTPUT_FILE


def _prepare_dir():
    if os.path.exists(OUTPUT_DIRECTORY):
        shutil.rmtree(OUTPUT_DIRECTORY)

    os.makedirs(OUTPUT_DIRECTORY)


def open_file() -> TextIO:
    _prepare_dir()
    return open(OUTPUT_DIRECTORY + OUTPUT_FILE, 'w')
