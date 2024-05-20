"""Pretraining and sentiment student to instructor review sentiment corpora and
analysis.

"""
__author__ = 'Paul Landes'

from typing import List, Tuple, Any
from dataclasses import dataclass
import logging
from pathlib import Path
from zensols.util.time import time
from zensols.install import Installer
from zensols.deepnlp.cli import NLPClassifyPackedModelApplication

logger = logging.getLogger(__name__)


@dataclass
class Application(NLPClassifyPackedModelApplication):
    """Classifies sentiment in Albanian.

    """
    CLASS_INSPECTOR = {}

    def predict_csv(self, text_or_file: str) -> Path:
        """Create predictions from a newline separated file of sentences.

        :param text_or_file: newline delimited file of sentences or a sentence

        """
        import pandas as pd
        from . import SentimentFeatureDocument

        sents: Tuple[str] = text_or_file,
        path = Path(text_or_file)
        if path.is_file():
            with open(path) as f:
                sents = tuple(map(str.strip, f.readlines()))
            out_file = path.parent / f'{path.stem}.csv'
        else:
            out_file = Path('predictions.csv')
        rows: List[Tuple[Any, ...]] = []
        with time(f'predicted {len(sents)} sentences'):
            doc: SentimentFeatureDocument
            for doc in self.predict(sents):
                rows.append((doc.pred, doc.text))
        df = pd.DataFrame(rows, columns='prediction text'.split())
        df.to_csv(out_file)
        logger.info(f'wrote: {out_file}')

    def install_corpus(self) -> Path:
        """Install the sentiment corpus."""
        logging.getLogger('zensols.install').setLevel(logging.INFO)
        installer: Installer = self.facade.config_factory('feature_installer')
        corp_path: Path = installer.get_singleton_path()
        installer.install()
        if logger.isEnabledFor(logging.INFO):
            logger.info(f'sentiment corpus location: {corp_path}')
        return corp_path
