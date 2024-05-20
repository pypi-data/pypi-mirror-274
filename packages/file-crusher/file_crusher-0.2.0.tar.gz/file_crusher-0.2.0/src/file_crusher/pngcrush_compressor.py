import os
import subprocess
import sys
from subprocess import CalledProcessError

from .config import PNGCRUSH_PATH
from .file_operations import compare_and_use_better_option, check_if_valid_image
from .processor import processor


class PNGCrushCompressor:
    def __init__(
            self,
            event_handlers=None
    ):
        """
        Compresses PNG images using pngcrush.
        :param event_handlers: (list of EventHandler) A list of event handlers. (pre and postprocessors)
        :returns: None
        """

        pngcrush_path = PNGCRUSH_PATH
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if not os.path.isfile(pngcrush_path):
            linux_error = "Install it with 'sudo apt install pngcrush'." if os.name != "nt" else ""
            raise FileNotFoundError(rf"pngcrush path not found at '{pngcrush_path}'. {linux_error}")

        system_extra = "powershell.exe" if os.name == 'nt' else ""
        pngcrush_options = "-rem alla -rem text -reduce"  # -brute"
        # TODO add option brute when compression mode is high
        self.pngcrush_command = f"{system_extra} {pngcrush_path} {pngcrush_options}"

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        check_if_valid_image(source_file)
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        subprocess.check_output(rf'{self.pngcrush_command} "{source_file}" "{source_file[:-4] + "-comp.png"}"',
                                stderr=subprocess.STDOUT, shell=True)
        result_file = source_file[:-4] + '-comp.png'
        compare_and_use_better_option(source_file, result_file, destination_path)
        if os.path.exists(result_file):
            os.remove(result_file)
