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
    "PRON": "pronouns",
    "PART": "particles",
    "ADJ": "adjectives",
    "ADP": "prepositions",
    "PROPN": "proper_nouns",
    "PUNCT": "punctuations",
    "INTJ": "interjections",
    "CCONJ": "coordinating_conjunctions",
    "SCONJ": "subordinating_conjunctions",
}


class PosAnalyzer:
    other: List[str] = []
    nouns: List[str] = []
    verbs: List[str] = []
    number: List[str] = []
    symbols: List[str] = []
    adverbs: List[str] = []
    articles: List[str] = []
    pronouns: List[str] = []
    particles: List[str] = []
    adjectives: List[str] = []
    prepositions: List[str] = []
    proper_nouns: List[str] = []
    punctuations: List[str] = []
    interjections: List[str] = []
    coordinating_conjunctions: List[str] = []
    subordinating_conjunctions: List[str] = []

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
        self.n_particles = len(self.particles)
        self.n_adjectives = len(self.adjectives)
        self.n_prepositions = len(self.prepositions)
        self.n_proper_nouns = len(self.proper_nouns)
        self.n_punctuations = len(self.punctuations)
        self.n_interjections = len(self.interjections)
        self.n_coordinating_conjunctions = len(self.coordinating_conjunctions)
        self.n_subordinating_conjunctions = len(self.subordinating_conjunctions)
