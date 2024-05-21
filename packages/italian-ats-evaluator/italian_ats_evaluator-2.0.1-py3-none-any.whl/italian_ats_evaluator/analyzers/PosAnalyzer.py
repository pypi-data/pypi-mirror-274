from typing import List

from spacy.tokens import Doc

POS_MAP = {
    "X": "other",
    "NOUN": "nouns",
    "AUX": "verbs",
    "VERB": "verbs",
    "NUM": "number",
    "SYM": "symbols",
    "ADV": "adverbs",
    "DET": "articles",
    "PART": "particle",
    "PRON": "pronouns",
    "ADJ": "adjectives",
    "ADP": "prepositions",
    "INTJ": "interjection",
    "PROPN": "proper_nouns",
    "PUNCT": "punctuations",
    "CCONJ": "coordinating_conjunction",
    "SCONJ": "subordinating_conjunction",
}


class PosAnalyzer:
    other: List[str] = []
    nouns: List[str] = []
    verbs: List[str] = []
    number: List[str] = []
    symbols: List[str] = []
    adverbs: List[str] = []
    articles: List[str] = []
    particle: List[str] = []
    pronouns: List[str] = []
    adjectives: List[str] = []
    prepositions: List[str] = []
    proper_nouns: List[str] = []
    interjection: List[str] = []
    punctuations: List[str] = []
    coordinating_conjunction: List[str] = []
    subordinating_conjunction: List[str] = []

    def __init__(self, processed_text: Doc):
        for token in processed_text:
            if token.pos_ in POS_MAP:
                getattr(self, POS_MAP[token.pos_]).append(token.text)

        self.n_other = len(self.other)
        self.n_nouns = len(self.nouns)
        self.n_verbs = len(self.verbs)
        self.n_number = len(self.number)
        self.n_symbols = len(self.symbols)
        self.n_adverbs = len(self.adverbs)
        self.n_articles = len(self.articles)
        self.n_pronouns = len(self.pronouns)
        self.n_adjectives = len(self.adjectives)
        self.n_prepositions = len(self.prepositions)
        self.n_proper_nouns = len(self.proper_nouns)
        self.n_punctuations = len(self.punctuations)
        self.n_coordinating_conjunction = len(self.coordinating_conjunction)
        self.n_subordinating_conjunction = len(self.subordinating_conjunction)
