"""Create a trait pipeline."""

import spacy
from traiter.patterns.matcher_patterns import (
    add_ruler_patterns, patterns_to_dispatch)
from traiter.pipes.add_entity_data import ADD_ENTITY_DATA
from traiter.pipes.cache import CACHE_LABEL
# from traiter.pipes.debug import debug_tokens
from traiter.pipes.sentence import SENTENCE
from traiter.tokenizer_util import append_abbrevs, append_tokenizer_regexes

from myrsidea.patterns.body_part import BODY_PART
from myrsidea.pylib.const import ABBREVS, TERMS

GROUPERS = [BODY_PART]
MATCHERS = []


def pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])

    append_tokenizer_regexes(nlp)
    append_abbrevs(nlp, ABBREVS)

    # Add a set of pipes to identify phrases and patterns as base-level traits
    config = {'phrase_matcher_attr': 'LOWER'}
    term_ruler = nlp.add_pipe(
        'entity_ruler', name='term_ruler', config=config, before='parser')
    term_ruler.add_patterns(TERMS.for_entity_ruler())
    nlp.add_pipe('merge_entities', name='term_merger')
    nlp.add_pipe(CACHE_LABEL, name='term_cache')

    # Sentence parsing should happen early but it may depend on terms
    nlp.add_pipe(SENTENCE, before='parser', config={'automatic': ['heading']})

    # debug_tokens(nlp)

    # Add a set of pipes to group terms into larger traits
    config = {'overwrite_ents': True}
    group_ruler = nlp.add_pipe('entity_ruler', name='group_ruler', config=config)
    add_ruler_patterns(group_ruler, GROUPERS)

    # nlp.add_pipe(CACHE_LABEL, name='group_cache')
    # nlp.add_pipe('merge_entities', name='group_merger')

    # Add a pipe to group tokens into larger traits
    # config = {'overwrite_ents': True}
    # match_ruler = nlp.add_pipe('entity_ruler', name='match_ruler', config=config)
    # add_ruler_patterns(match_ruler, MATCHERS)

    # debug_tokens(nlp)

    config = {'dispatch': patterns_to_dispatch(GROUPERS + MATCHERS)}
    nlp.add_pipe(ADD_ENTITY_DATA, config=config)

    # Remove unused entities
    # nlp.add_pipe(CLEANUP, config={'entities': FORGET})

    # config = {'patterns': as_dict(PART_LINKER, SEX_LINKER, SUBPART_LINKER)}
    # nlp.add_pipe(DEPENDENCY, name='part_linker', config=config)

    return nlp
