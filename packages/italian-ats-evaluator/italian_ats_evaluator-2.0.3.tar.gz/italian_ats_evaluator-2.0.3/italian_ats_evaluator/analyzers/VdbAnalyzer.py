from typing import List

from .BasicAnalyzer import BasicAnalyzer
from ..utils import nlp_utils


class VdbAnalyzer:
    vdb_tokens: List[str] = []
    vdb_fo_tokens: List[str] = []
    vdb_au_tokens: List[str] = []
    vdb_ad_tokens: List[str] = []

    n_vdb_tokens: int = 0
    n_vdb_fo_tokens: int = 0
    n_vdb_au_tokens: int = 0
    n_vdb_ad_tokens: int = 0

    def __init__(self, basic_analyzer: BasicAnalyzer):
        for lemma in basic_analyzer.lemmas:
            if nlp_utils.is_vdb(lemma):
                self.vdb_tokens.append(lemma)
            if nlp_utils.is_vdb_fo(lemma):
                self.vdb_fo_tokens.append(lemma)
            if nlp_utils.is_vdb_au(lemma):
                self.vdb_au_tokens.append(lemma)
            if nlp_utils.is_vdb_ad(lemma):
                self.vdb_ad_tokens.append(lemma)
