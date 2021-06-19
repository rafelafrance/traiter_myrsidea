"""Extract body part annotations."""

import re

import spacy
from traiter.const import COMMA
from traiter.patterns.matcher_patterns import MatcherPatterns

from myrsidea.pylib.const import COMMON_PATTERNS, CONJ, MISSING, REPLACE

JOINER = CONJ + COMMA

MISSING_RE = '|'.join([fr'\b{m}\b' for m in MISSING])
MISSING_RE = re.compile(MISSING_RE, flags=re.IGNORECASE)

BODY_PART = MatcherPatterns(
    'body_part',
    on_match='myrsidea.body_part.v1',
    decoder=COMMON_PATTERNS | {
        'seg': {'ENT_TYPE': 'segmented'},
        'ord': {'ENT_TYPE': {'IN': ['ordinal', 'number_word']}},
    },
    patterns=[
        'part+',
        'part_loc+ part+',
        # 'missing? any_part* part',
        # 'part+ ord -? ord',
        # 'part+ 99? -? 99',
        # 'part+ ord?',
        # 'part+ 99?',
        # 'part+ ord -? seg',
        # 'part+ 99 -? seg',
        # 'ord? -? seg? part+',
        # '99 - seg part+',
    ],
)


@spacy.registry.misc(BODY_PART.on_match)
def body_part(ent):
    """Enrich a body part span."""
    data = {}

    parts = [REPLACE.get(t.lower_, t.lower_) for t in ent]

    text = ' '.join(parts)

    if MISSING_RE.search(ent.text.lower()) is not None:
        data['missing'] = True

    data['body_part'] = text

    ent._.data = data
