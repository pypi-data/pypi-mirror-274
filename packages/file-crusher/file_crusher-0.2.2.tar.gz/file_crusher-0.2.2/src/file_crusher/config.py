import os

COMPRESSOR_LIB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "compressor_lib"
))

# ---------------------------------------
if "WINE_PATH" in os.environ:
    WINE_PATH = os.environ["WINE_PATH"]
else:
    WINE_PATH = os.path.join("/", "usr", "bin", "wine")

# ---------------------------------------
if "ADVPNG_PATH" in os.environ:
    ADVPNG_PATH = os.environ["ADVPNG_PATH"]
elif os.name == "nt":  # Windows default
    ADVPNG_PATH = os.path.join(COMPRESSOR_LIB_PATH, "advpng", "advpng.exe")
else:  # Linux default
    ADVPNG_PATH = os.path.join("/", "usr", "bin", "advpng")

# ---------------------------------------
if "PNGQUANT_PATH" in os.environ:
    PNGQUANT_PATH = os.environ["PNGQUANT_PATH"]
elif os.name == "nt":  # Windows default
    PNGQUANT_PATH = os.path.join(COMPRESSOR_LIB_PATH, "pngquant", "pngquant.exe")
else:  # Linux default
    PNGQUANT_PATH = os.path.join("/", "usr", "bin", "pngquant")

# ---------------------------------------
if "PNGCRUSH_PATH" in os.environ:
    PNGCRUSH_PATH = os.environ["PNGCRUSH_PATH"]
elif os.name == "nt":  # Windows default
    PNGCRUSH_PATH = os.path.join(COMPRESSOR_LIB_PATH, "pngcrush", "pngcrush.exe")
else:  # Linux default
    PNGCRUSH_PATH = os.path.join("/", "usr", "bin", "pngcrush")

# ---------------------------------------
if "CPDFQUEEZE_PATH" in os.environ:
    CPDFQUEEZE_PATH = os.environ["CPDFQUEEZE_PATH"]
else:
    CPDFQUEEZE_PATH = os.path.join(COMPRESSOR_LIB_PATH, "cpdfsqueeze", "cpdfsqueeze.exe")

# ---------------------------------------
if "TESSERACT_PATH" in os.environ:
    TESSERACT_PATH = os.environ["TESSERACT_PATH"]
elif os.name == "nt":  # Windows default
    TESSERACT_PATH = os.path.join(os.path.abspath(os.path.expanduser('~')), "AppData", "Local", "Programs",
                                 "Tesseract-OCR", "tesseract.exe")
else:  # Linux default
    TESSERACT_PATH = os.path.join("/", "usr", "bin", "tesseract")

# ---------------------------------------
if "TESSDATA_PREFIX" in os.environ:
    TESSDATA_PREFIX = os.environ["TESSDATA_PREFIX"]
elif os.name == "nt":  # Windows default
    TESSDATA_PREFIX = "--tessdata-dir '" + os.path.join(os.path.expanduser('~'), 'AppData', 'Local', 'Programs',
                                                        'Tesseract-OCR', 'tessdata')
else:  # Linux default
    TESSDATA_PREFIX = ""
