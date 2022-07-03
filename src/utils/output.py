import os

from properties.constant import OUTPUT_DIR, OUTPUT_EMIT_DIR


def prepare_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if not os.path.exists(OUTPUT_EMIT_DIR):
        os.makedirs(OUTPUT_EMIT_DIR)

    if not os.path.exists(f'{OUTPUT_EMIT_DIR}temp-hill-climbing'):
        os.makedirs(f'{OUTPUT_EMIT_DIR}temp-hill-climbing')
