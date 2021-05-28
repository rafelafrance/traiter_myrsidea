"""Common utilities."""
import re
from contextlib import contextmanager
from shutil import rmtree
from tempfile import mkdtemp

import ftfy


def clean_text(text):
    """Format text for output."""
    text = '\n'.join(text)
    text = re.sub(r'([a-z])-\s+([a-z])', r'\1\2', text, flags=re.IGNORECASE)
    text = re.sub(r'\n\s+\n', '\n\n', text)
    text = re.sub(r'(\S)\s(\S)', r'\1 \2', text)
    text = re.sub(r'\n\n', '\n', text)
    text = ftfy.fix_text(text)
    return text


@contextmanager
def make_temp_dir(where=None, prefix=None, keep=False):
    """Handle creation and deletion of temporary directory."""
    temp_dir = mkdtemp(prefix=prefix, dir=where)
    try:
        yield temp_dir
    finally:
        if not keep or not where:
            rmtree(temp_dir, ignore_errors=True)
