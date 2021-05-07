"""Utilities and constants."""
from pathlib import Path

# from traiter.terms.itis import Itis

DATA_DIR = Path.cwd() / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = Path.cwd() / 'output'
MODEL_DIR = Path.cwd() / 'models'
VOCAB_DIR = Path.cwd() / 'myrsidea' / 'vocabulary'

# #########################################################################
# Term relate constants

# TERMS = Itis.shared('animals insect_anatomy numerics')
# TERMS += Itis.shared('units', labels='metric_length')
# TERMS += Itis.read_csv(VOCAB_DIR / 'common_terms.csv')
# TERMS += Itis.read_csv(VOCAB_DIR / 'myrsidea_terms.csv')
# TERMS += Itis.read_csv(VOCAB_DIR / 'myrsidea_species.csv')
# TERMS += Itis.abbrev_species(TERMS, label='myrsidea')
# TERMS += Itis.taxon_level_terms(
#     TERMS, label='myrsidea', new_label='myrsidea_genus', level='genus')
# TERMS += Itis.taxon_level_terms(TERMS, label='mammalia')
# TERMS += Itis.abbrev_species(TERMS, label='mammalia')

# REPLACE = TERMS.pattern_dict('replace')

# #########################################################################
# Pattern related constants

COMMON_PATTERNS = {
}

# #########################################################################
# Remove these stray entities
FORGET = """ """.split()
