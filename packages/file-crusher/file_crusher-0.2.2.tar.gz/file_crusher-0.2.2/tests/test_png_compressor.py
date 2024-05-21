import os
import shutil
import tempfile
from unittest import TestCase

from file_crusher import PNGQuantCompressor, PNGCompressor, PNGCrushCompressor, ADVPNGCompressor


class PngCompressorTest(TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, 'input.png')
        self.output_file = os.path.join(self.test_dir, 'output.png')
        shutil.copyfile(os.path.join("test_data", "testimage.png"), self.input_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_pngquant_processor_single_file(self):
        compressor = PNGQuantCompressor()
        self.assertFalse(os.path.exists(self.output_file))
        compressor.process_file(self.input_file, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_pngcrush_processor_single_file(self):
        compressor = PNGCrushCompressor()
        compressor.process_file(self.input_file, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_advpng_processor_single_file(self):
        compressor = ADVPNGCompressor()
        compressor.process_file(self.input_file, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def test_png_processor_single_file(self):
        compressor = PNGCompressor()
        compressor.process_file(self.input_file, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))
