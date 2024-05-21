import spacy
import pyphen
import pkgutil

dic = pyphen.Pyphen(lang='it')

italian_vdb_fo = {a for a in pkgutil.get_data('italian_ats_evaluator', 'nvdb/FO.txt').decode('utf-8').split('\r\n')}
italian_vdb_au = {a for a in pkgutil.get_data('italian_ats_evaluator', 'nvdb/AU.txt').decode('utf-8').split('\r\n')}
italian_vdb_ad = {a for a in pkgutil.get_data('italian_ats_evaluator', 'nvdb/AD.txt').decode('utf-8').split('\r\n')}
italian_vdb = italian_vdb_fo.union(italian_vdb_au).union(italian_vdb_ad)


def get_model() -> spacy.language.Language:
    try:
        return spacy.load("it_core_news_lg")
    except OSError:
        spacy.cli.download("it_core_news_lg")
        return spacy.load("it_core_news_lg")


def clean_text(text: str) -> str:
    text = text.strip()
    text = text.replace("\r\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    return " ".join(text.split())


def eval_syllables(token: str):
    return dic.inserted(token).split('-')


def is_vdb(lemma: str):
    return lemma in italian_vdb


def is_vdb_fo(lemma: str):
    return lemma in italian_vdb_fo


def is_vdb_au(lemma: str):
    return lemma in italian_vdb_au


def is_vdb_ad(lemma: str):
    return lemma in italian_vdb_ad