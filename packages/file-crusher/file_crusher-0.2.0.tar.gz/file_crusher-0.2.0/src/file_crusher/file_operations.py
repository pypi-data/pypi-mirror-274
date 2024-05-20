import os
import re
import shutil
import uuid
from glob import glob

from PIL import Image


def check_if_valid_image(file: str, return_bool: bool = False):
    try:
        with Image.open(file) as img:
            img.verify()
        return True
    except Exception:
        # couldn't open and verify -> not a valid image
        if return_bool:
            return False
        else:
            raise ValueError(rf"'{file}' does not appear to be a valid path to a PNG file")


def get_file_size(file_path: str) -> int:
    return 0 if not os.path.isfile(file_path) else os.stat(file_path).st_size


def copy_file(from_file: str, to_file: str):
    # skip copy if equals
    if from_file == to_file:
        return
    # create directory if not already exists
    output_dir = os.path.dirname(os.path.abspath(to_file))
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    shutil.copy(from_file, to_file)


def compare_and_use_better_option(file_path_1: str, file_path_2: str, destination_file: str) -> None:
    size_option_1 = get_file_size(file_path_1)
    size_option_2 = get_file_size(file_path_2)

    # compression worked -> copy file to final destination
    if check_if_valid_image(file_path_2) and size_option_1 > size_option_2 or \
            not check_if_valid_image(file_path_1):
        copy_file(file_path_2, destination_file)
    # error in output file -> copy source file to destination
    else:
        copy_file(file_path_1, destination_file)


def get_files_in_folder(folder_path: str, ending: str = "*"):
    return glob(os.path.join(folder_path, ending), include_hidden=True)


def get_filename(full_path_to_file: str) -> str:
    filename_with_ending = os.path.basename(full_path_to_file)
    return re.split(r"\.[^.]*$", filename_with_ending)[0]


def print_stats(orig: int, result: int) -> None:
    if orig < 0:
        raise ValueError("orig must be greater than or equal to 0")
    if result < 0:
        raise ValueError("result can't be less than 0")
    orig_size = str(round(orig / 1000000, 2))
    result_size = str(round(result / 1000000, 2))
    percentage = 0 if orig == 0 else str(-1 * round(100 - (result / orig * 100), 2))
    print(f"Compressed File from {orig_size}mb to {result_size}mb ({percentage}%)\n")
