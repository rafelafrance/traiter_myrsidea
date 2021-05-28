#!/usr/bin/env python3

"""Extract myrsidea traits from scientific literature (PDFs to text)."""

import argparse
import textwrap

from myrsidea.pylib.pipeline import pipeline


def main(args):
    """Extract data from the files."""
    nlp = pipeline()
    rows = []

    with open(args.text) as in_file:
        lines = [ln.strip() for ln in in_file.readlines()]

    for doc in nlp.pipe(lines):
        rows.append({'doc': doc})


def parse_args():
    """Process command-line arguments."""
    description = """Parse data from lice papers."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description),
        fromfile_prefix_chars='@')

    arg_parser.add_argument('--text', '-t', help="""Path to the text file to parse.""")

    arg_parser.add_argument(
        '--html-file', '-H', type=argparse.FileType('w'),
        help="""Output the results to this HTML file.""")

    args = arg_parser.parse_args()

    return args


if __name__ == '__main__':
    ARGS = parse_args()
    main(ARGS)