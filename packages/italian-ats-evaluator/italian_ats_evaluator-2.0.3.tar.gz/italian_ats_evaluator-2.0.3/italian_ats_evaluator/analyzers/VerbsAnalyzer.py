from typing import List

from spacy.tokens import Doc


class VerbsAnalyzer:
    active_verbs: List[str] = []
    passive_verbs: List[str] = []

    n_active_verbs: int = 0
    n_passive_verbs: int = 0

    def __init__(self, processed_text: Doc):
        for token in processed_text:
            if token.pos_ == "VERB" or token.pos_ == "AUX":
                if token.dep_ == "aux" and "aux:pass" in [c.dep_ for c in token.head.children]:
                    self.passive_verbs.append(token.text)
                elif token.dep_ == "aux:pass" and token.head.pos_ == "VERB":
                    self.passive_verbs.append(token.text)
                elif token.pos_ == "VERB" and "aux:pass" in [c.dep_ for c in token.children]:
                    self.passive_verbs.append(token.text)
                else:
                    self.active_verbs.append(token.text)

        self.n_active_verbs = len(self.active_verbs)
        self.n_passive_verbs = len(self.passive_verbs)
