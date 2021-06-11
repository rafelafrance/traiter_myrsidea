"""Parse measurement notations."""

import re

import spacy
from traiter.const import FLOAT_RE, INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import list_to_re_choice, to_positive_float, to_positive_int

from myrsidea.pylib.const import COMMON_PATTERNS, REPLACE, TERMS

UNITS_RE = [t['pattern'] for t in TERMS if t['label'] == 'metric_length']
UNITS_RE = '(?<![A-Za-z])' + list_to_re_choice(UNITS_RE) + r'\b'

DECODER = COMMON_PATTERNS | {
    'n': {'LOWER': 'n'},
    'measure': {'ENT_TYPE': 'measure'},
}


SAMPLE = MatcherPatterns(
    'sample',
    on_match='myrsidea.sample.v1',
    decoder=DECODER,
    patterns=['n = 99'],
)


MEASUREMENT = MatcherPatterns(
    'measurement',
    on_match='myrsidea.measurement.v1',
    decoder=DECODER,
    patterns=[
        'measure 99.9 mm?',
        'measure 99.9 - 99.9 mm?',
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
        if label == 'measure':
            data['measure'] = REPLACE.get(token.lower_, token.lower_)
        elif label == 'metric_length':
            data['units'] = REPLACE.get(token.lower_, token.lower_)
        elif re.match(FLOAT_RE, token.text):
            data[key] = to_positive_float(token.text)
            key = 'high'
    ent._.data = data
