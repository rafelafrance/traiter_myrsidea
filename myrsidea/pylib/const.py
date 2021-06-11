"""Utilities and constants."""
from pathlib import Path

from traiter.const import CLOSE, COMMA, CROSS, DASH, EQ, FLOAT_TOKEN_RE, OPEN
from traiter.terms.itis import ITIS_DB, Itis

ROOT_DIR = Path('.') if str(Path.cwd()).endswith('myrsidea') else Path('..')

DATA_DIR = ROOT_DIR / 'data'
DOC_DIR = DATA_DIR
PDF_DIR = DOC_DIR / 'pdf'
TXT_DIR = DOC_DIR / 'txt'
OUTPUT_DIR = ROOT_DIR / 'output'
MODEL_DIR = ROOT_DIR / 'models'
VOCAB_DIR = ROOT_DIR / 'myrsidea' / 'vocabulary'

# #########################################################################
CHAR_BLACKLIST = '¥€£¢$«»®©§{}[]<>|'
TESS_CONFIG = ' '.join([
    '-l eng',
    f"-c tessedit_char_blacklist='{CHAR_BLACKLIST}'",
])

# #########################################################################
# Term relate constants

TERMS = Itis.shared('animals insect_anatomy numerics')
TERMS += Itis.shared('units', labels='metric_length')
TERMS += Itis.read_csv(VOCAB_DIR / 'myrsidea_terms.csv')
TERMS += Itis.read_csv(VOCAB_DIR / 'myrsidea_species.csv')
TERMS += Itis.abbrev_species(TERMS, label='myrsidea')

if ITIS_DB.exists():
    TERMS += Itis.itis('Aves', label='aves')
    TERMS += Itis.itis_common_names('Aves')
    TERMS += Itis.taxon_level_terms(
        TERMS, label='myrsidea', new_label='myrsidea_genus', level='genus')
else:
    TERMS += Itis.mock_itis_traits(VOCAB_DIR / 'mock_itis_terms.csv', 'aves')

TERMS += Itis.abbrev_species(TERMS, label='aves')

REPLACE = TERMS.pattern_dict('replace')

# #########################################################################
# Tokenizer constants
ABBREVS = """
        Jan. Feb. Mar. Apr. Jun. Jul. Aug. Sep. Sept. Oct. Nov. Dec.
        mm. cm. m.
        al. Am. Anim. Bio. Biol. Bull. Bull. Conserv. D.C. Ecol. Entomol. Fig. Figs.
        Hist. Inst. Int. Lond. Me´m. Mol. Mus. Nat. nov. Physiol. Rep. Sci. Soc.
        sp. Syst. Zool.
        """.split()

# #########################################################################
# Pattern related constants
MISSING = """ no without missing lack lacking except excepting """.split()
EQ_ = EQ + ['¼']
CONJ = ['and', '&', 'or']

COMMON_PATTERNS = {
    '(': {'TEXT': {'IN': OPEN}},
    ')': {'TEXT': {'IN': CLOSE}},
    '=': {'TEXT': {'IN': EQ_}},  # ¼ = 0xbc
    'x': {'LOWER': {'IN': CROSS + ['⫻']}},  # ⫻ = 0x3f
    '-': {'TEXT': {'IN': DASH}},
    ',': {'TEXT': {'IN': COMMA}},
    '-/to': {'LOWER': {'IN': DASH + ['to']}},
    '&/or': {'LOWER': {'IN': CONJ}},
    '&/,/or': {'LOWER': {'IN': CONJ + COMMA}},
    '99': {'IS_DIGIT': True},
    '99.9': {'TEXT': {'REGEX': FLOAT_TOKEN_RE}},
    'mm': {'ENT_TYPE': 'metric_length'},
    'part': {'ENT_TYPE': 'part'},
    'any_part': {'ENT_TYPE': {'IN': ['part_loc', 'part']}},
    'part_loc': {'ENT_TYPE': {'IN': ['part_loc']}},
    'missing': {'LOWER': {'IN': MISSING}},
    'not_ent': {'ENT_TYPE': ''},
}

# #########################################################################
# Remove these stray entities
FORGET = """ number_word """.split()
