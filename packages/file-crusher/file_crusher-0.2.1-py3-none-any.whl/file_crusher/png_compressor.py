import os
import sys

from .pipeline_processor import PipelineProcessor
from .CompressionPostprocessor import CompressionPostprocessor
from .advpng_compressor import ADVPNGCompressor
from .file_operations import print_stats, get_file_size
from .pngcrush_compressor import PNGCrushCompressor
from .pngquant_compressor import PNGQuantCompressor
from .processor import processor


class PNGCompressor:
    def __init__(
            self,
            compression_mode: int = 3,
            event_handlers=None
    ):
        """
         Compresses PNG images using a combination of compression tools.
         :param compression_mode: Speed of compression,
            where 0 is the slowest (best quality) and 5 is the fastest.
         :param event_handlers: A list of event handlers. (pre and postprocessors)
         :returns: None
         """

        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if compression_mode <= 0 or compression_mode >= 6:
            raise ValueError("Compression mode must be in range 1-5")

        advcomp_iterations = None
        advcomp_shrink_rate = None
        pngquant_max_quality = None
        pngquant_min_quality = None
        pngquant_speed = None
        match compression_mode:
            case 1:
                advcomp_iterations = 3
                advcomp_shrink_rate = 4
                pngquant_max_quality = 80
                pngquant_min_quality = 0
                pngquant_speed = 1
            case 2:
                advcomp_iterations = 2
                advcomp_shrink_rate = 3
                pngquant_max_quality = 85
                pngquant_min_quality = 25
                pngquant_speed = 2
            case 3:
                advcomp_iterations = 2
                advcomp_shrink_rate = 2
                pngquant_max_quality = 85
                pngquant_min_quality = 25
                pngquant_speed = 2
            case 4:
                advcomp_iterations = 1
                advcomp_shrink_rate = 2
                pngquant_max_quality = 90
                pngquant_min_quality = 25
                pngquant_speed = 8
            case 5:
                advcomp_iterations = 1
                advcomp_shrink_rate = 1
                pngquant_max_quality = 99
                pngquant_min_quality = 25
                pngquant_speed = 9

        try:
            self.__advcomp = ADVPNGCompressor(
                shrink_rate=advcomp_shrink_rate,
                iterations=advcomp_iterations,
                event_handlers=[CompressionPostprocessor("advcomp")]
            )
        except FileNotFoundError:
            print("Error: Program advcomp not found, skipped compression with advcomp.", file=sys.stderr)
            self.__advcomp = None

        try:
            self.__pngquant = PNGQuantCompressor(
                speed=pngquant_speed,
                min_quality=pngquant_min_quality,
                max_quality=pngquant_max_quality,
                event_handlers=[CompressionPostprocessor("pngquant")]
            )
        except FileNotFoundError:
            print("Error: Program pngquant not found, skipped compression with pngquant.", file=sys.stderr)
            self.__pngquant = None

        try:
            self.__pngcrush = PNGCrushCompressor(
                event_handlers=[CompressionPostprocessor("pngcrush")]
            )
        except FileNotFoundError:
            print("Error: Program pngcrush not found, skipped compression with pngcrush.", file=sys.stderr)
            self.__pngcrush = None

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        if os.path.isdir(destination_path):
            destination_path = os.path.join(destination_path, os.path.basename(source_file))
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        start_file_size = get_file_size(source_file)
        processor = PipelineProcessor(True, [self.__pngquant, self.__advcomp, self.__pngcrush])
        processor.process_file(source_file, destination_path)
        print_stats(start_file_size, get_file_size(destination_path))
