#!/usr/bin/env python
"""Convert a PDF to text."""

import argparse
import json
import re
import tempfile
from pathlib import Path
from textwrap import dedent

import pytesseract
from pdf2image import convert_from_path
from tqdm import tqdm
from traiter.util import clean_text

from myrsidea.pylib.const import TESS_CONFIG


# MOJIBAKE = '{"¼": "=", "⫻": "×", "#": "♂", "$": "♀", "(*": "(X"}'
MOJIBAKE = '{"¼": "=", "⫻": "×", "(*": "(X"}'


def main(args):
    """Convert a PDF to text."""
    if args.pdf and args.raw:
        get_raw_text(args)

    if args.raw and args.format:
        format_text(args)


def get_raw_text(args):
    """Convert the PDF to raw text.

    Tesseract only reads text from images, so we need to convert
    each page of the PDF to an image and use tesseract on that.
    """
    pages = []
    with tempfile.TemporaryDirectory() as temp_dir:
        images = convert_from_path(args.pdf, output_folder=temp_dir)
        for image in tqdm(images):
            page = pytesseract.image_to_string(image, config=TESS_CONFIG)
            page = clean_text(page, replace=args.mojibake)
            pages.append(page)

    paper = '\n\n'.join(pages)
    paper = re.sub(r'(\S)\n(\S)', r'\1 \2', paper)

    with open(args.raw, 'w') as txt_file:
        txt_file.write(paper)


def format_text(args):
    """Format text for trait extraction."""
    with open(args.raw) as txt_file:
        paper = txt_file.read()

    paper = re.sub(r'(\S)\n(\S)', r'\1 \2', paper)
    paper = re.sub(r'\n\n+', r'\n', paper)

    with open(args.format, 'w') as txt_file:
        txt_file.write(paper)


def parse_args():
    """Process command-line arguments."""
    description = """Convert a PDF to text then format the text for trait extraction."""

    epilog = dedent("""\
        This is a 3-step process, one of which is manual.
          1) Convert the --pdf to --raw text.
          2) Manually edit the text to remove headers, footers, figure
             captions, etc. You may also fix any other text issues,
             like replacing odd characters, caused imperfect
             character conversions during step 1.
          3) --format the --raw text to make it ready for trait extraction.
          ** --raw and --format may be the same file.
        """)

    arg_parser = argparse.ArgumentParser(
        description=description, epilog=epilog, fromfile_prefix_chars='@',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    arg_parser.add_argument(
        '--pdf', type=Path, help="""Input PDF file to convert.""")

    arg_parser.add_argument(
        '--raw', type=Path, metavar='TEXT',
        help="""Output the raw text to this file.""")

    arg_parser.add_argument(
        '--format', type=Path, metavar='TEXT',
        help="""Output formatted text to this file.""")

    arg_parser.add_argument(
        '--mojibake', type=json.loads, default='{}', metavar='DICT',
        help=f"""Fix odd characters that happen during the pdf to raw text conversion.
            Enter the argument as a JSON dictionary. Then the script will search for
            the odd strings given as a key and replace them with the value.
            For example: --mojibake='{MOJIBAKE}'.""")

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)
