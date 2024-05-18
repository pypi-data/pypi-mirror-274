import spacy

from .analysis.basic_analysis import do_basic_analysis
from .analysis.diff_analysis import do_token_diff_analysis, do_char_diff_analysis
from .analysis.pos_analysis import do_pos_analysis
from .analysis.readability_analysis import do_readability_analysis
from .analysis.similarity_analysis import do_similarity_analysis
from .analysis.vdb_analysis import do_vdb_analysis

try:
    nlp = spacy.load("it_core_news_lg")
except OSError:
    spacy.cli.download("it_core_news_lg")
    nlp = spacy.load("it_core_news_lg")


def analyze_text(text):
    text = text.strip()
    text = text.replace("\r\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    text_processed = nlp(text)

    # open("output.html", "w").write(spacy.displacy.render(text_processed.sents, style="dep", page=True))

    overall = do_basic_analysis(text_processed)
    pos, verbs = do_pos_analysis(text_processed)
    readability = do_readability_analysis(overall, pos)
    vdb = do_vdb_analysis(overall["lemmas"])

    data = {
        "overall": overall,
        "readability": readability,
        "pos": pos,
        "verbs": verbs,
        "vdb": vdb
    }

    stats = {
        "overall": {k: len(v) for k, v in overall.items()},
        "readability": readability,
        "pos": {k: len(v) for k, v in pos.items()},
        "pos_percentage": {k: len(v) / len(overall["tokens_all"]) * 100 for k, v in pos.items()},
        "verbs": {k: len(v) for k, v in verbs.items()},
        "verbs_percentage": {k: len(v) / len(pos["verbs"]) * 100 for k, v in verbs.items()},
        "vdb": {k: len(v) for k, v in vdb.items()},
        "vdb_percentage": {k: len(v) / len(overall["lemmas"]) * 100 for k, v in vdb.items()}
    }
    return text_processed, data, stats


def comparison(ref_text, simplified_text):
    ref_text_processed1, ref_data, ref_stats = analyze_text(ref_text)
    text_processed2, simplified_data, simplified_stats = analyze_text(simplified_text)

    similarity = do_similarity_analysis(ref_text, simplified_text)
    token_diff = do_token_diff_analysis(ref_data["overall"], simplified_data["overall"])
    char_diff = do_char_diff_analysis(ref_data["overall"], simplified_data["overall"])

    comparison_data = {
        "similarity": similarity,
        "token_diff": token_diff,
        "char_diff": char_diff
    }

    comparison_stats = {
        "similarity": similarity,
        "char_diff": char_diff,
        "token_diff": {k: len(v) for k, v in token_diff.items()},
        "char_diff_saled": {k: v / len(ref_data["overall"]["chars"]) * 100 for k, v in char_diff.items()},
        "token_diff_scaled": {k: len(v) / len(ref_data["overall"]["tokens"]) * 100 for k, v in token_diff.items()},
    }

    return ref_data, ref_stats, simplified_data, simplified_stats, comparison_data, comparison_stats
