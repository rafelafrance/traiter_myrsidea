"""Parse body part count notations."""

import re

import spacy
from traiter.const import DASH, INT_RE
from traiter.patterns.matcher_patterns import MatcherPatterns
from traiter.util import to_positive_int

from myrsidea.pylib.const import COMMON_PATTERNS, MISSING, REPLACE

BOTH = """ both each """.split()
SIDE = """ side sides """.split()

DECODER = COMMON_PATTERNS | {
    'part': {'ENT_TYPE': 'body_part'},
    'loc': {'ENT_TYPE': 'part_loc'},
    'subpart': {'ENT_TYPE': 'subpart'},
    'seta': {'ENT_TYPE': 'cheta'},
    'each': {'LOWER': {'IN': BOTH}},
    'side': {'LOWER': {'IN': SIDE}},
    'prep': {'DEP': 'prep'},
    'adj': {'POS': 'ADJ'},
}

SETA_COUNT = MatcherPatterns(
    'seta_count',
    on_match='myrsidea.seta_count.v1',
    decoder=DECODER,
    patterns=[
        'loc subpart? missing? seta',
        'loc? subpart? prep 99 + 99 seta',
        'loc? subpart? prep 99 seta prep each side',
        'loc? subpart? prep 99 seta',
        'part missing seta',
        'part prep 99 seta prep each side',
        'part prep 99 seta',
        'loc? subpart? prep 99 - 99 seta',
        'part prep? 99 - 99 seta',
        'part prep? 99 - 99 seta prep? loc? subpart',
        'part prep? 99 loc? seta',
        'part prep? 99 adj+ seta',
    ],
)


@spacy.registry.misc(SETA_COUNT.on_match)
def seta_count(ent):
    """Enrich the entity."""
    data = {}
    parts = []
    counts = []
    both = False
    low_high = False
    for token in ent:
        label = token._.cached_label
        if label == 'body_part':
            body_part = token._.data.get('body_part', token.lower_)
            parts.append(REPLACE.get(body_part, body_part))
        elif label == 'cheta':
            parts.append('seta')
        elif label == 'subpart':
            parts.append(REPLACE.get(token.lower_, token.lower_))
        elif label == 'part_loc':
            parts.append(REPLACE.get(token.lower_, token.lower_))
        elif re.match(INT_RE, token.text):
            counts.append(to_positive_int(token.text))
        elif token.text in DASH:
            low_high = True
        elif token.lower_ in BOTH:
            both = True
        elif token.lower_ in MISSING:
            data['missing'] = True

    data['part'] = ' '.join(parts)

    if both:
        counts.append(counts[0])

    if len(counts) > 1 and low_high:
        data['count_low'] = min(counts)
        data['count_high'] = max(counts)
    elif len(counts) > 1:
        data['count_side_1'] = counts[0]
        data['count_side_2'] = counts[1]
    elif len(counts) == 1:
        data['count'] = counts[0]
    else:
        data['count'] = 0

    ent._.data = data
