#!/usr/bin/env python3
"""Convert a PDF to text."""

import argparse
import tempfile
import textwrap
from pathlib import Path

# import pandas as pd
import pytesseract
from pdf2image import convert_from_path

# from myrsidea.pylib.util import clean_text


def main(args):
    """Convert the PDF to a text format we can use.

    The standard utilities for for converting PDFs don't really do what
    we need.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        for path in args.pdf:
            text = []
            images = convert_from_path(path, output_folder=temp_dir)
            for image in images:
                # page = pytesseract.image_to_string(image)
                table = pytesseract.image_to_data(image, output_type='data.frame')
                print(table)
                # text.append(page)
            # text = clean_text(text)
            print(text)


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument(
        'pdf', type=Path, nargs='+',
        help="""Path to the PDF paper to parse.""")

    arg_parser.add_argument(
        '--text-file', '-T', type=argparse.FileType('w'),
        help="""Output the results to this text file.""")

    arg_parser.add_argument(
        '--mojibake', '-m', action='append', nargs=2,
        help="""Translation table to use for converting odd mojibake.""")

    args = arg_parser.parse_args()

    if args.mojibake:
        args.mojibake = str.maketrans(args.mojibake)

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
