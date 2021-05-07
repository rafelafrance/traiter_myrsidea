"""Create a trait pipeline."""

import spacy

from traiter.pipes.debug import DEBUG_ENTITIES, DEBUG_TOKENS

DEBUG_COUNT = 0  # Used to rename debug pipes


def pipeline():
    """Setup the pipeline for extracting traits."""
    nlp = spacy.load('en_core_web_sm', exclude=['ner', 'lemmatizer'])

    return nlp


def debug_tokens(nlp, message='', **kwargs):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    nlp.add_pipe(
        DEBUG_TOKENS,
        name=f'tokens_{DEBUG_COUNT}',
        config=config,
        **kwargs,
    )


def debug_ents(nlp, message='', **kwargs):
    """Add pipes for debugging."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    config = {'message': message}
    nlp.add_pipe(
        DEBUG_ENTITIES,
        name=f'entities_{DEBUG_COUNT}',
        config=config,
        **kwargs,
    )
