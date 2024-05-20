"""Contains domain and container and utility classes to parse read the corpus.

"""
__author__ = 'Paul Landes'

from typing import Tuple
from dataclasses import dataclass, field
import logging
import sys
from io import TextIOBase
from pathlib import Path
import pandas as pd
from zensols.nlp import (
    FeatureDocument, WhiteSpaceTokenizerFeatureDocumentParser
)
from zensols.dataframe import ResourceFeatureDataframeStash
from zensols.deepnlp.classify import LabeledFeatureDocument

logger = logging.getLogger(__name__)


@dataclass
class SentimentFeatureDocument(LabeledFeatureDocument):
    """A feature document that contains the topic (i.e. subject) and emotion
    (i.e. joy, fear, etc) of the corresponding sentence(s).  This document
    usually has one sentence per the corpus, but can have more if the language
    parser chunks it as such.

    """
    topic: str = field(default='none')
    """The subject of the review (i.e. project, instruction, general, etc).
    Default to ``none`` for predictions.

    """
    emotion: str = field(default='none')
    """The emotion of the reveiw (i.e. joy, fear, surpise, etc).  Default to
    ``none`` for predictions.

    """
    def __post_init__(self):
        super().__post_init__()
        # the corpus contains a sentence for each row/data point, so copy this
        # to all sentences (see class docs)
        for sent in self.sents:
            sent.topic = self.topic
            sent.emotion = self.emotion

    @property
    def is_prediction(self) -> bool:
        """Whether the document has a prediction."""
        return self.label is None

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout):
        self._write_line('text:', depth, writer)
        self._write_line(self.text, depth + 1, writer)
        if self.is_prediction:
            pred_str: str = {
                '+': 'positive',
                '-': 'negative',
                'n': 'neutral'
            }[self.pred]
            self._write_line(f'prediction: {pred_str}', depth, writer)
            self._write_line('logits:', depth, writer)
            self._write_object(self.softmax_logit, depth + 1, writer)
        else:
            self._write_line(f'topic: {self.topic}', depth + 1, writer)
            self._write_line(f'emotion: {self.emotion}', depth + 1, writer)

    def __str__(self) -> str:
        ss = FeatureDocument.__str__(self)
        if self.is_prediction:
            ss = f'({self.pred}): {ss}'
        return ss


@dataclass
class SentimentDataframeStash(ResourceFeatureDataframeStash):
    """Create the dataframe by reading the sentiment sentences from the corpus
    files.

    """
    lang: str = field()
    """The corpus language."""

    labels: Tuple[str] = field()
    """The labels of the classification, which are::

      * ``+``: positive sentiment
      * ``-``: negative sentiment
      * ``n``: neutral sentiment

    """
    def _get_dataframe(self) -> pd.DataFrame:
        self.installer()
        corp_dir: Path = self.installer.get_singleton_path()
        corp_file: Path = corp_dir / f'{self.lang}.csv'
        return pd.read_csv(corp_file)


class SentimentFeatureDocumentParser(WhiteSpaceTokenizerFeatureDocumentParser):
    """A white space tokenizer that sets all the parameters of the spaCy
    tokenizer to simplify the configuration.

    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.__dict__.update(kwargs)
