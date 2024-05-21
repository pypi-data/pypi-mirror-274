import os.path
import re


class CompressionPostprocessor:
    __compressor_name: str

    def __init__(self, compressor_name: str):
        self.__compressor_name = compressor_name

    def postprocess(self, source_file: str, destination_file: str) -> None:
        print(f"** - Compressed Files with {self.__compressor_name}")
