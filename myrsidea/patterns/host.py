"""Extract host annotations annotations."""

import spacy
from traiter.patterns.matcher_patterns import MatcherPatterns

from myrsidea.pylib.const import REPLACE

HOST_SPECIES = MatcherPatterns(
    'host_species',
    on_match='myrsidea.host_species.v1',
    patterns=[[{'ENT_TYPE': 'aves'}]],
)


HOST_COMMON_NAME = MatcherPatterns(
    'host_common_name',
    on_match='myrsidea.host_common_name.v1',
    patterns=[[{'ENT_TYPE': 'common_name'}]],
)


@spacy.registry.misc(HOST_SPECIES.on_match)
def host_species(ent):
    """Enrich a trait match."""
    data = {}

    text = ent.text.lower()
    data['host_species'] = REPLACE.get(text, text)

    ent._.data = data


@spacy.registry.misc(HOST_COMMON_NAME.on_match)
def host_common_name(ent):
    """Enrich a trait match."""
    data = {}

    text = ent.text.lower()
    data['host_common_name'] = REPLACE.get(text, text)

    ent._.data = data
