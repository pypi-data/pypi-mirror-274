import pyphen
from spacy.tokens import Doc

dic = pyphen.Pyphen(lang='it')


def eval_syllables(token: str):
    return dic.inserted(token).split('-')


def do_basic_analysis(processed_text: Doc):
    overall = {
        "tokens": [],
        "tokens_all": [],
        "chars": [],
        "chars_all": [],
        "syllables": [],
        "words": set(),
        "lemmas": [],
        "unique_lemmas": set(),
        "sentences": list(processed_text.sents),
    }

    for token in processed_text:
        overall["tokens_all"].append(token.text)
        overall["chars_all"].extend([c for c in token.text])

        if not token.is_punct:
            overall["tokens"].append(token.text)
            overall["chars"].extend([c for c in token.text])
            overall["syllables"].extend(eval_syllables(token.text))
            overall["words"].add(token.text)
            overall["lemmas"].append(token.lemma_)
            overall["unique_lemmas"].add(token.lemma_)

    overall["words"] = list(overall["words"])
    overall["unique_lemmas"] = list(overall["unique_lemmas"])
    return overall
