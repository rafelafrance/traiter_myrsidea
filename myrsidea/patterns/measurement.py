"""Parse measurement notations."""

import re

import spacy
from traiter.const import FLOAT_RE, INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import list_to_re_choice, to_positive_float, to_positive_int

from myrsidea.pylib.const import COMMON_PATTERNS, REPLACE, TERMS

UNITS_RE = [t['pattern'] for t in TERMS if t['label'] == 'metric_length']
UNITS_RE = '(?<![A-Za-z])' + list_to_re_choice(UNITS_RE) + r'\b'

MEASURE_KEY = """measure labial_seta head_seta """.split()
RATIO_SYM = """ : / """.split()

DECODER = COMMON_PATTERNS | {
    'n': {'LOWER': 'n'},
    'measure_key': {'ENT_TYPE': {'IN': MEASURE_KEY}},
    ':': {'TEXT': {'IN': RATIO_SYM}},
    '11': {'IS_DIGIT': True},
}

SAMPLE = MatcherPatterns(
    'sample',
    on_match='myrsidea.sample.v1',
    decoder=DECODER,
    patterns=['n = 99'],
)

RATIO = MatcherPatterns(
    'ratio',
    on_match='myrsidea.ratio.v1',
    decoder=DECODER,
    patterns=[
        'measure_key : measure_key 99.9 mm?',
        'measure_key : measure_key 99.9 - 99.9 mm?',
        'measure_key : 11 99.9 mm?',
        'measure_key : 11 99.9 - 99.9 mm?',
    ],
)

MEASUREMENT = MatcherPatterns(
    'measurement',
    on_match='myrsidea.measurement.v1',
    decoder=DECODER,
    patterns=[
        'measure_key ,? 99.9 mm?',
        'measure_key ,? 99.9 - 99.9 mm?',
        'measure_key ( measure_key ) ,? 99.9 mm?',
        'measure_key ( measure_key ) ,? 99.9 - 99.9 mm?',
    ],
)


@spacy.registry.misc(SAMPLE.on_match)
def sample(ent):
    """Enrich the entity."""
    match = re.search(INT_RE, ent.text)
    value = match.group(0)
    ent._.data = {'n': to_positive_int(value)}


@spacy.registry.misc(MEASUREMENT.on_match)
def measurement(ent):
    """Enrich the entity."""
    data = {}
    key = 'low'
    for token in ent:
        label = token._.cached_label
        if label in MEASURE_KEY:
            data['measurement'] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'metric_length':
            data['units'] = REPLACE.get(token.lower_, token.lower_)
        elif re.match(FLOAT_RE, token.text):
            data[key] = to_positive_float(token.text)
            key = 'high'
    ent._.data = data


@spacy.registry.misc(RATIO.on_match)
def ratio(ent):
    """Enrich the entity."""
    data = {}
    value_key = 'low'
    ratio_key = []
    for token in ent:
        label = token._.cached_label
        if label in MEASURE_KEY:
            ratio_key.append(token.lower_)
        elif token.text in RATIO_SYM:
            ratio_key.append(token.text)
        elif re.search(INT_RE, token.text) and len(ratio_key) < 3:
            ratio_key.append(token.text)
        elif label == 'metric_length':
            data['units'] = REPLACE.get(token.lower_, token.lower_)
        elif re.match(FLOAT_RE, token.text):
            data[value_key] = to_positive_float(token.text)
            value_key = 'high'
    data['ratio'] = ''.join(ratio_key)
    ent._.data = data
