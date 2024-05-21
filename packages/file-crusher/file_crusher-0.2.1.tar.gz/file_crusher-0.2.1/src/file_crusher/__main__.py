import argparse

from . import CPdfSqueezeCompressor, PDFCompressor, PNGCompressor, PNGCrushCompressor, \
    PNGQuantCompressor, ADVPNGCompressor


def main():
    parser = argparse.ArgumentParser(description="Process a file through a series of processors.")
    parser.add_argument('input_file', type=str, help="The input file to be processed.")
    parser.add_argument('output_file', type=str, help="The output file after processing.")

    # Customize options for each processor
    processor_help = {
        "CPdfSqueezeCompressor": {
            "description": "Lossless PDF Compression.",
            "class": CPdfSqueezeCompressor
        },
        "PDFCompressor": {
            "description": "Lossy PDF Compression, great for scans.",
            "class": PDFCompressor
        },
        "PNGCompressor": {
            "description": "Combined Lossy PNG compression.",
            "class": PNGCompressor
        },
        "ADVPNGCompressor": {
            "description": "Lossy PNG compression.",
            "class": ADVPNGCompressor
        },
        "PNGQuantCompressor": {
            "description": "Lossy PNG compression.",
            "class": PNGQuantCompressor
        },
        "PNGCrushCompressor": {
            "description": "Lossy PNG compression.",
            "class": PNGCrushCompressor
        },
    }

    processor_group = parser.add_mutually_exclusive_group(required=True)

    for i, processor in enumerate(processor_help.keys()):
        processor_group.add_argument(
            f"-{i}",
            f'--{processor.lower()}',
            action='store_true',
            help=processor_help[processor]["description"]
        )

    args = parser.parse_args()

    for processor in processor_help:
        if getattr(args, processor.lower()):
            processor_help[processor]["class"]().process_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
