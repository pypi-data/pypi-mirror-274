import os
import subprocess
import sys

from .config import WINE_PATH, CPDFQUEEZE_PATH
from .processor import processor


class CPdfSqueezeCompressor:
    def __init__(
            self,
            use_wine_on_linux: bool = True,
            extra_args: str = "",
            event_handlers=None
    ):
        """
        Pdf Compression via cpdf
        :param use_wine_on_linux:
             True means it runs the command via wine.
                Only should be active when using linux or unix.
                If it is active on Windows, it will be automatically disabled.
            False means it directly runs the executable file at the path.
        :param extra_args: extra args to pass the executable (e.g. -upw <password> for a user password)
        :param event_handlers: (list of EventHandler) A list of event handlers. (pre and postprocessors)
        """
        self.extra_args = extra_args
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        self.__cpdfsqueeze_path = CPDFQUEEZE_PATH

        if not os.path.exists(self.__cpdfsqueeze_path):
            raise ValueError(rf"cpdfsqueeze_path couldn't be found. '{self.__cpdfsqueeze_path}'")

        # optionally add wine to the command on Linux
        if os.name != "nt" and use_wine_on_linux:
            if not os.path.exists(WINE_PATH):
                raise ValueError(
                    rf"'{WINE_PATH}' wine path couldn't be found. Install it with 'sudo apt install wine'.")
            self.__cpdfsqueeze_path = f"{WINE_PATH} {self.__cpdfsqueeze_path}"

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        if not os.path.exists(source_file) or not source_file.endswith(".pdf"):  # TODO maybe switch to mime type
            raise ValueError("Only pdf files are accepted")
        if not os.path.exists(os.path.dirname(destination_path)):
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        command = f'{self.__cpdfsqueeze_path} "{source_file}" "{destination_path}" {self.extra_args}'
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
