import spacy


def get_model() -> spacy.language.Language:
    try:
        return spacy.load("it_core_news_lg")
    except OSError:
        spacy.cli.download("it_core_news_lg")
        return spacy.load("it_core_news_lg")
