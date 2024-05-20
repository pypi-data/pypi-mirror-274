import sys

from PIL.Image import DecompressionBombError

import os
# package name pillow
from PIL import Image
from img2pdf import convert

from ..config import TESSDATA_PREFIX, TESSERACT_PATH
from ..file_operations import get_filename
from ..processor import processor

# OCR for pdf
try:
    import pytesseract

    PY_TESS_AVAILABLE = True
except:
    PY_TESS_AVAILABLE = False


# TODO consoleUI processor


class ImagesToPdfConverter:
    def __init__(
            self,
            force_ocr: bool = False,
            no_ocr: bool = False,
            tesseract_language: str = "eng",
            event_handlers=None
    ):
        """
        :param force_ocr: (bool) force ocr even and fail if not possible
        :param no_ocr: (bool) skip ocr if not necessary or to preserve file size
        :param tesseract_language: (str) which language(s) are used for ocr
        :param event_handlers: (list of EventHandler) A list of event handlers. (pre and postprocessors) (pre and postprocessors)

        possible_files_endings = ['.jpc', '.xbm', '.j2k', '.icns', '.png', '.bmp', '.jp2', '.apng', '.j2c', '.jpe', '.tif',
                          '.rgb', '.tiff', '.jpx', '.bw', '.gif', '.jpg', '.jpf', '.jfif', '.rgba', '.sgi', '.webp',
                          '.dib', '.jpeg']

        """
        self.event_handlers = event_handlers
        if self.event_handlers is None:
            self.event_handlers = []

        if force_ocr and no_ocr:
            raise ValueError("force_ocr and no_ocr can't be used together")
        self.force_ocr = (force_ocr or not no_ocr) and PY_TESS_AVAILABLE
        self.no_ocr = no_ocr
        self.tesseract_language = tesseract_language

        try:
            self.__init_pytesseract(TESSERACT_PATH)
        except ValueError:
            self.force_ocr = False

    def __init_pytesseract(self, pytesseract_path) -> None:
        # either initiates pytesseract or deactivate ocr if not possible
        try:
            if not os.path.isfile(pytesseract_path):
                raise FileNotFoundError(r"[ ! ] - tesseract Path not found. Install "
                                        "https://github.com/UB-Mannheim/tesseract/wiki or edit "
                                        "'TESSERACT_PATH' to your specific tesseract executable")
            # set command (not sure why windows needs it differently)
            elif os.name == "nt":
                pytesseract.pytesseract.tesseract_cmd = f"{pytesseract_path}"
            else:
                pytesseract.tesseract_cmd = f"{pytesseract_path}"

        except Exception:
            if self.force_ocr:
                print("Tesseract Not Loaded, Can't create OCR."
                      "(leave out option '--ocr-force' to compress without ocr)", file=sys.stderr)
                self.force_ocr = False
            raise ValueError("Tesseract (-> no OCR on pdfs)")

    @processor
    def process_file(self, source_file: str, destination_path: str) -> None:
        if os.path.isdir(destination_path):
            destination_path = os.path.join(destination_path, get_filename(source_file) + ".pdf")

        try:
            if not self.force_ocr or self.no_ocr:
                raise ValueError("skipping tesseract")

            result = pytesseract.image_to_pdf_or_hocr(
                Image.open(source_file), lang=self.tesseract_language,
                extension="pdf",
                config=rf"{TESSDATA_PREFIX}"
            )
        except DecompressionBombError as e:
            raise e
        except ValueError:  # if ocr/tesseract fails or is skipped on purpose
            result = convert(source_file)
            print("No OCR applied.", file=sys.stderr)

        with open(destination_path, "wb") as f:
            f.write(result)
