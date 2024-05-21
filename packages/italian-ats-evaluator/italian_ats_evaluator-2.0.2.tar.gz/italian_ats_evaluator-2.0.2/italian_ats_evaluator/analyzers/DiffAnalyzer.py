from typing import List

import editdistance

from .BasicAnalyzer import BasicAnalyzer
from ..utils import nlp_utils


class DiffAnalyzer:
    editdistance: int = 0

    added_tokens: List[str] = []
    deleted_tokens: List[str] = []
    added_vdb_tokens: List[str] = []
    deleted_vdb_tokens: List[str] = []

    n_added_tokens: int = 0
    n_deleted_tokens: int = 0
    n_added_vdb_tokens: int = 0
    n_deleted_vdb_tokens: int = 0

    def __init__(self, reference_basic: BasicAnalyzer, simplified_basic: BasicAnalyzer):
        self.editdistance = editdistance.eval(
            ''.join(reference_basic.chars).lower(),
            ''.join(simplified_basic.chars).lower()
        )

        for token, lemma in zip(simplified_basic.tokens, simplified_basic.lemmas):
            if token not in reference_basic.tokens:
                self.added_tokens.append(token)
                if nlp_utils.is_vdb(lemma):
                    self.added_vdb_tokens.append(token)

        for token, lemma in zip(reference_basic.tokens, reference_basic.lemmas):
            if token not in simplified_basic.tokens:
                self.deleted_tokens.append(token)
                if nlp_utils.is_vdb(lemma):
                    self.deleted_vdb_tokens.append(token)

        self.n_added_tokens = len(self.added_tokens)
        self.n_deleted_tokens = len(self.deleted_tokens)
        self.n_added_vdb_tokens = len(self.added_vdb_tokens)
        self.n_deleted_vdb_tokens = len(self.deleted_vdb_tokens)
