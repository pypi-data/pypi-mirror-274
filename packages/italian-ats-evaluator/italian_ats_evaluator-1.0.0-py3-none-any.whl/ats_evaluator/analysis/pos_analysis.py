from spacy.tokens import Doc

POS_MAP = {
    "X": "other",
    "NOUN": "nouns",
    "NUM": "number",
    "SYM": "symbols",
    "ADV": "adverbs",
    "DET": "articles",
    "PRON": "pronouns",
    "ADJ": "adjectives",
    "ADP": "prepositions",
    "PROPN": "proper_nouns",
    "PUNCT": "punctuations",
    "CCONJ": "coordinating_conjunction",
    "SCONJ": "subordinating_conjunction",
    # "VERB": "verbs",
    # "AUX": "verbs"
}


def do_pos_analysis(processed_text: Doc):
    _pos_distribution = {
        "other": [],
        "nouns": [],
        "number": [],
        "symbols": [],
        "adverbs": [],
        "articles": [],
        "pronouns": [],
        "adjectives": [],
        "prepositions": [],
        "proper_nouns": [],
        "punctuations": [],
        "coordinating_conjunction": [],
        "subordinating_conjunction": [],
        "verbs": []
    }
    _verbs_distribution = {
        "active_verbs": [],
        "passive_verbs": []
    }
    for token in processed_text:
        if token.pos_ in POS_MAP:
            _pos_distribution[POS_MAP[token.pos_]].append(token.text)

        if token.pos_ == "VERB" or token.pos_ == "AUX":
            _pos_distribution["verbs"].append(token.text)
            if token.dep_ == "aux" and "aux:pass" in [c.dep_ for c in token.head.children]:
                _verbs_distribution["passive_verbs"].append(token.text)
            elif token.dep_ == "aux:pass" and token.head.pos_ == "VERB":
                _verbs_distribution["passive_verbs"].append(token.text)
            elif token.pos_ == "VERB" and "aux:pass" in [c.dep_ for c in token.children]:
                _verbs_distribution["passive_verbs"].append(token.text)
            else:
                _verbs_distribution["active_verbs"].append(token.text)
    return _pos_distribution, _verbs_distribution
