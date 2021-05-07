"""Common utilities."""
import re

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
